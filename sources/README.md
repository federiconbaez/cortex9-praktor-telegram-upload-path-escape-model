# sources/

The official upstream diff behind every line citation is **not** in this
repo. It belongs to mtzanidakis/praktor (Copyright (c) 2026 Manolis
Tzanidakis) and is under that project's license (MIT), not this repo's
Apache-2.0. The commit also adds a `SECURITY.md` that contains a personal
mailbox, which is out of scope for the model, so the verbatim file is
not stored here.

This directory holds `diffs.tsv` (tag, file name, SHA-256 and upstream
URL of the official `.diff`) and `UPSTREAM-LICENSE` (the project's MIT
license, fetched read-only on 2026-11-19 from
https://raw.githubusercontent.com/mtzanidakis/praktor/main/LICENSE,
SHA-256 `63ed0b1f4c500a52ca6fe89eca2f1544f6d17503dbc01a1c3950918e07e1547a`,
also in `SHA256SUMS`).

Fetch the diff read-only and run the content check:

```sh
curl -fsSL -o /tmp/CVE-2026-62331_praktor_c3731eeda01c.diff https://github.com/mtzanidakis/praktor/commit/c3731eeda01c0b3ec1dbd13cccd5a147c3182141.diff
sha256sum /tmp/CVE-2026-62331_praktor_c3731eeda01c.diff   # must be d2075c6f2000517ee13ae828367203464b27ac8fb287cc96515a18f11a52cffd
C9_DIFF=/tmp/CVE-2026-62331_praktor_c3731eeda01c.diff PYTHONPATH=src python3 -m unittest -v tests.test_citations
```

The URL above returned a byte-identical file (same SHA-256) on 2026-11-19.
Range hashes in `../citations.tsv` use this normalisation: lines
`start`..`end` of the diff exactly as stored (no `cat -n` prefix, nothing
stripped), joined with `\n`, no final newline, UTF-8 bytes, SHA-256.
