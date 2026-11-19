"""Offline model of praktor Telegram upload path construction, CVE-2026-62331.

Pre (github.com/mtzanidakis/praktor < 0.9.1) concatenates the
attacker-controlled document filename into `uploads/<timestamp>_<name>`
(c3731eed:L75, c3731eed:L84) and writes it with `path.Join("/vol",
filePath)` and no escape check (c3731eed:L55-56). `path.Join` collapses
`../` sequences.

The fix, commit c3731eeda01c0b3ec1dbd13cccd5a147c3182141 (v0.9.1), does
two things:

- `path.Base` on the filename at both Telegram upload sites
  (c3731eed:L76, c3731eed:L85), so directory components never enter
  `volumePath`.
- `WriteVolumeBytes` rejects a path that is not `/vol` and does not have
  the prefix `/vol/` after Join (c3731eed:L59-62).

Nothing here talks to Telegram, Docker, or a filesystem. Path arithmetic
follows Go's `path` package (slash-separated), checked against a table
taken from `path.Base` / `path.Join` on Go 1.x.
"""
from __future__ import annotations

import posixpath

PRE_RULE = "c3731eed:L75;c3731eed:L84;c3731eed:L55-56"
POST_RULE = "c3731eed:L76;c3731eed:L85;c3731eed:L59-62"
VERSIONS = ("pre", "post")
VOL_ROOT = "/vol"
UPLOADS_PREFIX = "/vol/uploads/"
DEFAULT_TS = 123


def go_path_base(p: str) -> str:
    """Go `path.Base` (slash-separated)."""
    if p == "":
        return "."
    if p.replace("/", "") == "":
        return "/"
    p = p.rstrip("/")
    i = p.rfind("/")
    return p[i + 1:] if i >= 0 else p


def go_path_join(elem_a: str, elem_b: str) -> str:
    """Go `path.Join` of two elements: join then Clean.

    For the slash-only relative names used in this model, Clean matches
    `posixpath.normpath`.
    """
    return posixpath.normpath(posixpath.join(elem_a, elem_b))


def trim_prefix(s: str, prefix: str) -> str:
    """Go `strings.TrimPrefix` (only one copy, only at the start)."""
    if s.startswith(prefix):
        return s[len(prefix):]
    return s


def telegram_volume_path(filename: str, version: str, timestamp: int = DEFAULT_TS) -> str:
    if version == "pre":
        name = filename  # c3731eed:L75, c3731eed:L84
    elif version == "post":
        name = go_path_base(filename)  # c3731eed:L76, c3731eed:L85
    else:
        raise ValueError(version)
    return f"uploads/{int(timestamp)}_{name}"


def write_volume_bytes(file_path: str, version: str) -> dict:
    cleaned = go_path_join(VOL_ROOT, file_path)
    if version == "post":
        if cleaned != VOL_ROOT and not cleaned.startswith(VOL_ROOT + "/"):
            # c3731eed:L59-62
            return {
                "ok": False,
                "cleaned": cleaned,
                "target": None,
                "error": "escapes volume root",
            }
        target = trim_prefix(cleaned, "/")  # c3731eed:L63
    elif version == "pre":
        target = trim_prefix(cleaned, "/")  # c3731eed:L55-56
    else:
        raise ValueError(version)
    return {"ok": True, "cleaned": cleaned, "target": target, "error": None}


def classify_landing(landing: str) -> str:
    if landing == "/vol/uploads" or landing.startswith(UPLOADS_PREFIX):
        return "IN_UPLOADS"
    if landing == VOL_ROOT or landing.startswith(VOL_ROOT + "/"):
        return "IN_VOLUME"
    return "ESCAPES_VOLUME"


def analyze(
    version: str,
    filename: str,
    site: str = "telegram",
    timestamp: int = DEFAULT_TS,
) -> dict:
    """site=telegram: Base (post) then WriteVolumeBytes.
    site=write: WriteVolumeBytes only (the defense-in-depth gate).
    """
    if site == "telegram":
        volume_path = telegram_volume_path(filename, version, timestamp)
        wr = write_volume_bytes(volume_path, version)
    elif site == "write":
        volume_path = filename
        wr = write_volume_bytes(filename, version)
    else:
        raise ValueError(site)
    if wr["ok"]:
        landing = "/" + wr["target"]
        outcome = classify_landing(landing)
    else:
        landing = None
        outcome = "REJECTED"
    return {
        "outcome": outcome,
        "volume_path": volume_path,
        "cleaned": wr["cleaned"],
        "target": wr["target"],
        "landing": landing,
        "error": wr["error"],
        "rule": PRE_RULE if version == "pre" else POST_RULE,
        "site": site,
    }
