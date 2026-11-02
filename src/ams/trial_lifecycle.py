"""One private evidence boundary for each owned adapter lifetime."""
from contextlib import contextmanager


def _cause(error):
    if error is None:return None
    value={'errorClass':type(error).__name__,'reason':str(error)}
    if error.__cause__ is not None:
        value['causedBy']={'errorClass':type(error.__cause__).__name__,'reason':str(error.__cause__)}
    return value


@contextmanager
def lifetime(adapter,create,snapshot):
    """Acquire, execute and close before normal return; cancellation always wins.

    Snapshot evidence before diagnostic IO, which may itself fail or interrupt.
    All causes stay private; callers receive an original exception, never a grade.
    """
    stream=None;body=None;cleanup=None;diagnostic=None
    try:
        stream=create()
        yield stream
    except BaseException as error:
        body=error
    evidence=snapshot()
    if stream is not None:
        try:stream.close()
        except BaseException as error:cleanup=error
    if body is None and cleanup is None:return
    failures={'body':_cause(body),'cleanup':_cause(cleanup),'diagnostic':None}
    adapter.last_failure={**evidence,'diagnostic':None,'failures':failures}
    primary=body if body is not None else cleanup
    if stream is not None and hasattr(stream,'failure_diagnostic'):
        try:adapter.last_failure['diagnostic']=stream.failure_diagnostic(type(primary).__name__,str(primary))
        except BaseException as error:
            diagnostic=error
            failures['diagnostic']=_cause(error)
    errors=[error for error in (body,cleanup,diagnostic)if error is not None]
    chosen=next((error for error in errors if isinstance(error,KeyboardInterrupt)),primary)
    other=next((error for error in errors if error is not chosen),None)
    if other is not None:raise chosen from other
    raise chosen
