"""Independent expectations for fixtures/cases.json.

Does not import src/. Rebuilds Go-like path.Base / path.Join with
posixpath and labels landings. Prints fixtures/expected.tsv.
Python 3.10+ standard library only.
"""
from __future__ import annotations

import json
import pathlib
import posixpath

ROOT = pathlib.Path(__file__).resolve().parent.parent
TS_DEFAULT = 123


def base(p: str) -> str:
    if p == "":
        return "."
    if p.replace("/", "") == "":
        return "/"
    p = p.rstrip("/")
    i = p.rfind("/")
    return p[i + 1:] if i >= 0 else p


def join_vol(file_path: str) -> str:
    return posixpath.normpath(posixpath.join("/vol", file_path))


def trim_slash(s: str) -> str:
    return s[1:] if s.startswith("/") else s


def landing_of(cleaned: str) -> str:
    return "/" + trim_slash(cleaned)


def classify(landing: str) -> str:
    if landing == "/vol/uploads" or landing.startswith("/vol/uploads/"):
        return "IN_UPLOADS"
    if landing == "/vol" or landing.startswith("/vol/"):
        return "IN_VOLUME"
    return "ESCAPES_VOLUME"


def decide(case: dict, version: str) -> str:
    name = case["filename"]
    site = case.get("site", "telegram")
    ts = int(case.get("timestamp", TS_DEFAULT))
    if site == "telegram":
        if version == "post":
            name = base(name)
        file_path = f"uploads/{ts}_{name}"
    elif site == "write":
        file_path = name
    else:
        raise ValueError(site)
    cleaned = join_vol(file_path)
    if version == "post" and cleaned != "/vol" and not cleaned.startswith("/vol/"):
        return "REJECTED"
    return classify(landing_of(cleaned))


def main() -> None:
    data = json.loads((ROOT / "fixtures/cases.json").read_text(encoding="utf-8"))
    print("id\tversion\toutcome")
    for case in data["cases"]:
        for ver in ("pre", "post"):
            print(f"{case['id']}\t{ver}\t{decide(case, ver)}")


if __name__ == "__main__":
    main()
