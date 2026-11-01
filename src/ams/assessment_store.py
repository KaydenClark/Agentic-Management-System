"""Private remote assessment history; never a behavioral trial or public data.

The service key stays in the local environment. HTTP bodies/errors and raw
packets are never printed by this CLI. Readback recomputes canonical results;
it validates supplied qualification structurally, without certifying its truth.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import uuid
from urllib.parse import urlencode

from ams import assessment, keycheck, writer

TABLE = 'rsi_assessments'
RPC = 'ams_append_assessment'
FORMAT = 2
Refused = assessment.Refused


def digest(value):
    return hashlib.sha256(assessment._encoded(value)).hexdigest()


def scorer_digest():
    return hashlib.sha256(Path(assessment.__file__).read_bytes()).hexdigest()


class Store:
    def __init__(self, url, key, http=writer.urllib_http, *, page_size=100):
        assessment.require(type(page_size) is int and 1 <= page_size <= 1000, 'invalid page size')
        self.url, self._key, self.http, self.page_size = url.rstrip('/'), key, http, page_size

    def __repr__(self):
        return 'PrivateAssessmentStore()'

    def _call(self, method, path, payload=None):
        status, body = writer._call(self.http, method, self.url+'/rest/v1/'+path, self._key, payload)
        assessment.require(status is not None and 200 <= status < 300,
                           f'private assessment {method} refused (HTTP {status or "unavailable"}); retry only after readback')
        return body

    def _page(self, *, is_test, after=None, through=None, descending=False):
        query=[('is_test','eq.'+str(is_test).lower()), ('order','id.desc' if descending else 'id.asc'),
               ('limit',1 if descending else self.page_size)]
        if after is not None:query.append(('id','gt.'+str(after)))
        if through is not None:query.append(('id','lte.'+str(through)))
        rows=self._call('GET',TABLE+'?'+urlencode(query))
        assessment.require(isinstance(rows,list), 'malformed private assessment readback')
        return rows

    def rows(self, *, is_test=False):
        assessment.require(type(is_test) is bool,'is_test must be boolean')
        # Global append serialization makes committed IDs monotonic. Capture a
        # high-water mark so later writes cannot shift pagination's snapshot.
        top=self._page(is_test=is_test,descending=True)
        if not top:return []
        end=top[0]['id']; after=0; rows=[]
        while after < end:
            page=self._page(is_test=is_test,after=after,through=end)
            assessment.require(bool(page),'incomplete private assessment snapshot')
            for row in page:
                assessment.require(type(row.get('id')) is int and after < row['id'] <= end,
                                   'unordered private assessment snapshot')
                after=row['id'];rows.append(row)
        self._verify(rows,is_test)
        return rows

    @staticmethod
    def _restore(row):
        # JSONB changes number spelling (and may change Python int/float type).
        # Hash/replay the original canonical TEXT artifact, not that projection.
        raw=row.get('envelope_text')
        assessment.require(isinstance(raw,str) and hashlib.sha256(raw.encode()).hexdigest()==row.get('content_digest'),
                           'assessment content digest mismatch')
        try:
            e=json.loads(raw)
            assessment.require(assessment._encoded(e).decode()==raw,'assessment text is not canonical')
            left=json.loads(raw,parse_float=Decimal,parse_int=Decimal)
            right=json.loads(json.dumps(row.get('envelope')),parse_float=Decimal,parse_int=Decimal)
        except (ValueError,TypeError) as exc:
            raise Refused('malformed assessment artifact') from exc
        def equal(a,b):
            if type(a) is not type(b):return False
            if isinstance(a,dict):return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
            if isinstance(a,list):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
            return a==b
        assessment.require(equal(left,right),'assessment text/projection mismatch')
        row['envelope']=e
        return row

    @classmethod
    def _verify(cls,rows,is_test):
        previous={}
        for row in rows:
            cls._restore(row)
            e=row.get('envelope')
            assessment.require(row.get('format_version')==FORMAT and row.get('scorer_digest')==scorer_digest(),
                               'assessment scorer identity changed; use the recorded reader revision')
            assessment.require(isinstance(e,dict) and isinstance(e.get('packet'),dict),'malformed assessment envelope')
            p=e['packet']
            assessment.require(row.get('is_test') is is_test and row.get('assessment_id')==p.get('assessmentId')
                               and row.get('failure_id')==p.get('failureId') and row.get('attempt')==p.get('attempt'),
                               'assessment row identity mismatch')
            assessment.require(row.get('content_digest')==digest(e), 'assessment content digest mismatch')
            assessment.require(row.get('previous_digest')==previous.get(p['failureId']), 'assessment predecessor mismatch')
            previous[p['failureId']]=row['content_digest']
        assessment.replay([r['envelope'] for r in rows])

    def read(self, *, is_test=False):
        return assessment.replay([r['envelope'] for r in self.rows(is_test=is_test)])

    def append(self, envelope, *, is_test, previous_digest):
        # The importer/replay is the semantic guard; the DB independently guards
        # identities, sequence and stale heads atomically, without reimplementing r1.
        assessment.require(type(is_test) is bool,'is_test must be boolean')
        assessment.require(previous_digest is None or re.fullmatch('[0-9a-f]{64}',previous_digest or ''),
                           'invalid previous digest')
        p=envelope['packet'];assessment._validate(p)
        existing=self.rows(is_test=is_test)
        for old in existing:
            if old['assessment_id']==p['assessmentId']:
                assessment.require(old['envelope']==envelope and old['previous_digest']==previous_digest,
                                   'assessment identity is immutable')
                return old
        history=[r['envelope'] for r in existing if r['failure_id']==p['failureId']]
        assessment.replay(history+[envelope])
        row={'assessment_id':p['assessmentId'],'failure_id':p['failureId'],'attempt':p['attempt'],
             'envelope':envelope,'envelope_text':assessment._encoded(envelope).decode(),'format_version':FORMAT,'scorer_digest':scorer_digest(),
             'content_digest':digest(envelope),'previous_digest':previous_digest,'is_test':is_test}
        saved=self._call('POST','rpc/'+RPC,{'p_row':row})
        assessment.require(isinstance(saved,dict),'malformed append response')
        self._restore(saved)
        assessment.require(isinstance(saved,dict) and all(saved.get(k)==v for k,v in row.items()),
                           'append response differs from submitted assessment')
        return saved

    def import_local(self, folder, *, is_test=False):
        folder=Path(folder)
        assessment.require(not folder.is_symlink() and not (folder/'.record-lock').exists(),
                           'inspect local symlink or interrupted writer before import')
        local=assessment.read_records(folder)  # Validate everything before any remote mutation.
        remote=self.rows(is_test=is_test)
        by_failure={}
        for r in remote:by_failure.setdefault(r['failure_id'],[]).append(r)
        local_groups={}
        for e in local:local_groups.setdefault(e['packet']['failureId'],[]).append(e)
        # Validate every prefix before writing any series. Other remote series
        # are allowed: separate local stores may contribute unrelated failures.
        for fid,items in local_groups.items():
            saved=by_failure.get(fid,[])
            assessment.require(len(saved)<=len(items) and
                               [r['envelope'] for r in saved]==items[:len(saved)],
                               'local/remote history diverged; preserve both and reconcile')
        appended=0
        for fid,items in local_groups.items():
            saved=by_failure.get(fid,[])
            prev=saved[-1]['content_digest'] if saved else None
            for e in items[len(saved):]:
                row=self.append(e,is_test=is_test,previous_digest=prev)
                prev=row['content_digest'];appended+=1
        return appended



def livecheck(settings, publishable, http=writer.urllib_http):
    """Roundtrip only explicitly marked synthetic probes, then remove our chain."""
    marker='assessment-probe-'+uuid.uuid4().hex
    store=Store(settings.url,settings.key,http,page_size=1)
    private=json.loads((keycheck.REPO_ROOT/'evals/assessment-example.json').read_text())
    private.update(assessmentId=marker+'-0',failureId=marker,attempt=0)
    private['measurementMetadata']={'observed':1e20,'negativeZero':-0.0,'nested':[1e308]}
    ok=True
    try:
        with tempfile.TemporaryDirectory(prefix='ams-assessment-probe-') as folder:
            assessment.record(private,folder)
            store.import_local(folder,is_test=True)
            private.update(assessmentId=marker+'-1',attempt=1)
            assessment.record(private,folder)
            store.import_local(folder,is_test=True)
            rows=[r for r in store.rows(is_test=True) if r['failure_id']==marker]
            same=(store.import_local(folder,is_test=True)==0 and len(rows)==2
                  and assessment._encoded([r['envelope'] for r in rows])==assessment._encoded(assessment.read_records(folder)))
            print('private paginated roundtrip/idempotence:', 'yes' if same else 'no');ok &= same
            row=rows[0]
            status,_=writer._call(http,'POST',store.url+'/rest/v1/rpc/'+RPC,settings.key,
                                 {'p_row':{k:v for k,v in row.items() if k not in ('id','recorded_at')}})
            print('atomic duplicate retry:',status);ok &= status==200
            collision={k:v for k,v in row.items() if k not in ('id','recorded_at')}
            collision['content_digest']='0'*64
            status,_=writer._call(http,'POST',store.url+'/rest/v1/rpc/'+RPC,settings.key,{'p_row':collision})
            print('changed identity refused:',status);ok &= status==409
            # Race two valid next attempts at the same DB predecessor. Exactly
            # one may append; the loser must preserve its competing evidence.
            payloads=[]
            for suffix in ('a','b'):
                packet=json.loads(json.dumps(private))
                packet.update(assessmentId=marker+'-2-'+suffix,attempt=2)
                e={'packet':packet,'result':assessment._transition(packet,[r['envelope'] for r in rows])}
                payloads.append(dict(assessment_id=packet['assessmentId'],failure_id=marker,attempt=2,
                                     is_test=True,format_version=FORMAT,scorer_digest=scorer_digest(),
                                     envelope=e,envelope_text=assessment._encoded(e).decode(),content_digest=digest(e),previous_digest=rows[-1]['content_digest']))
            def send(payload):
                return writer._call(http,'POST',store.url+'/rest/v1/rpc/'+RPC,settings.key,{'p_row':payload})[0]
            with ThreadPoolExecutor(max_workers=2) as workers:
                statuses=sorted(workers.map(send,payloads))
            print('concurrent append statuses:',statuses);ok &= statuses==[200,409]
            store.read(is_test=True)
            endpoint=store.url+'/rest/v1/'+TABLE+'?'+urlencode({'failure_id':'eq.'+marker})
            for method,payload in [('GET',None),('POST',collision),('PATCH',{'content_digest':'0'*64}),('DELETE',None)]:
                status,body=writer._call(http,method,endpoint,publishable,payload)
                denied=writer._denied(status,body)
                print('client '+method+' refused:',status);ok &= denied
            status,body=writer._call(http,'POST',store.url+'/rest/v1/rpc/'+RPC,publishable,{'p_row':collision})
            print('client RPC refused:',status);ok &= writer._denied(status,body)
            status,_=writer._call(http,'PATCH',endpoint,settings.key,{'content_digest':'0'*64})
            print('immutable service update refused:',status);ok &= status in (401,403,409)
    finally:
        endpoint=store.url+'/rest/v1/'+TABLE+'?'+urlencode({'failure_id':'eq.'+marker,'is_test':'eq.true'})
        store._call('DELETE',TABLE+'?'+urlencode({'failure_id':'eq.'+marker,'is_test':'eq.true'}))
        remaining=store._call('GET',TABLE+'?'+urlencode({'failure_id':'eq.'+marker,'is_test':'eq.true'}))
        print('cleanup remaining:',len(remaining));ok &= not remaining
    return 0 if ok else 1


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('import');p.add_argument('--store',type=Path,default=Path('.local/assessments'))
    sub.add_parser('livecheck')
    for name in ('import','readcheck'):
        p=p if name=='import' else sub.add_parser(name)
        p.add_argument('--test',action='store_true')
    args=parser.parse_args(argv)
    settings=keycheck.load_settings()
    try:
        assessment.require(settings.key is not None and keycheck.key_format(settings.key) in ('sb_secret','legacy-jwt'),
                           'local service key unavailable or unrecognized')
        if args.command=='livecheck':
            return livecheck(settings,writer.DEFAULT_PUBLISHABLE_KEY)
        store=Store(settings.url,settings.key)
        if args.command=='import':
            print('appended:',store.import_local(args.store,is_test=args.test))
        rows=store.read(is_test=args.test)
        print('verified private assessments:',len(rows))
        print('qualification: supplied evidence only; no behavioral benefit claimed')
        return 0
    except (Refused,OSError,ValueError,TypeError,KeyError):
        # A packet/path/transport message may contain private material. The API
        # raises structured refusals for callers; CLI output stays public-safe.
        print('private assessment operation refused; inspect local inputs and authorized readback',file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
