"""Committed application paths from the project's single manifest (ADR-000Y)."""
from dataclasses import dataclass
import json
from pathlib import PurePosixPath
import re

from .grill_board.answers import AnswerRefused, committed_entry, sha256
from .page_approvals import APPROVALS, CARDS

MANIFEST = 'workbench/manifest.json'  # The Workbench's bootstrap location.


def safe_relative(value):
    return (isinstance(value, str) and 0 < len(value) <= 240
            and all(re.fullmatch(r'[A-Za-z0-9._-]+', part) and part.casefold() not in {'.', '..', '.git'}
                    for part in value.split('/')))


def safe_voice_path(value):
    return (safe_relative(value) and PurePosixPath(value).parent == PurePosixPath(CARDS).parent
            and value.endswith('.md') and value.casefold() != APPROVALS.casefold())


@dataclass(frozen=True)
class FeedbackPaths:
    voice: str
    private: str
    manifest_sha: str
    inventory: str | None


def feedback_paths(root, rev='HEAD'):
    entry = committed_entry(root, MANIFEST, rev)
    try:
        if entry is None:
            raise ValueError
        declared = json.loads(entry[1])['pageReview']
        if (not isinstance(declared, dict) or not {'voice', 'privateFeedback'} <= set(declared)
                or not set(declared) <= {'voice', 'privateFeedback', 'inventory'}
                or not safe_voice_path(declared['voice']) or not safe_relative(declared['privateFeedback'])
                or declared['voice'].startswith(declared['privateFeedback'] + '/')):
            raise ValueError
        inventory = declared.get('inventory')
        if inventory is not None and (not safe_relative(inventory) or not inventory.endswith('.json')
                or any(part.startswith('.') for part in inventory.split('/'))
                or inventory == MANIFEST or inventory.startswith(declared['privateFeedback'] + '/')):
            raise ValueError
    except (KeyError, TypeError, ValueError, UnicodeDecodeError):
        raise AnswerRefused('The committed manifest needs safe pageReview voice and privateFeedback paths; keep your note.') from None
    return FeedbackPaths(declared['voice'], declared['privateFeedback'], sha256(entry[1]), inventory)
