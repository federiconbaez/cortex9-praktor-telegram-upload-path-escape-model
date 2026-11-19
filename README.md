# cortex9-praktor-telegram-upload-path-escape-model

Offline, inert model of **CVE-2026-62331** (GHSA-48v2-6jcm-fc99, CWE-22).
praktor before **0.9.1** concatenated an attacker-controlled Telegram
document filename into `uploads/<timestamp>_<name>` (c3731eed:L75,
c3731eed:L84) and wrote it with `path.Join("/vol", filePath)` and no
escape check (c3731eed:L55-56). A name such as `../../../NOTES.md`
resolved to the root of the agent workspace volume.

The fix, commit `c3731eeda01c0b3ec1dbd13cccd5a147c3182141` (in **0.9.1**
— see [evidence/fix-in-0.9.1.md](evidence/fix-in-0.9.1.md)), applies
`path.Base` at both upload sites (c3731eed:L76, c3731eed:L85) and
rejects any `WriteVolumeBytes` path that escapes `/vol` after Join
(c3731eed:L59-62).

Spanish: [README.es.md](README.es.md). Exercises: [PRACTICE.md](PRACTICE.md).

## The model

- `src/c9praktor/paths.py` rebuilds the Telegram `volumePath` and the
  `WriteVolumeBytes` join/prefix check, using Go `path` semantics.
  **No Telegram, Docker or filesystem I/O.**
- Outcomes: `IN_UPLOADS`, `IN_VOLUME` (inside `/vol` but outside
  `uploads/`), `ESCAPES_VOLUME`, `REJECTED` (post prefix check).

## Differential evidence (`results/summary.csv`)

| Class | n | pre | post |
|---|---|---|---|
| pos (telegram) | 3 | 2 `IN_VOLUME`, 1 `ESCAPES_VOLUME` | 3 `IN_UPLOADS` |
| pos (write) | 2 | 2 `ESCAPES_VOLUME` | 2 `REJECTED` |
| neg | 2 | `IN_UPLOADS` | `IN_UPLOADS` |
| observation | 3 | `IN_UPLOADS` | `IN_UPLOADS` |

`o01`–`o03` are **model observations**, not separate findings. See
[LIMITATIONS.md](LIMITATIONS.md).

## Line citations

Every line citation has the form `<tag>:L<n>` or `<tag>:L<n>-<m>`: the real
`cat -n` line(s) of the official fix diff. The diff is **not** included in
this repo; `sources/diffs.tsv` names it:

- `c3731eed` → `CVE-2026-62331_praktor_c3731eeda01c.diff`, SHA-256 `d2075c6f2000517ee13ae828367203464b27ac8fb287cc96515a18f11a52cffd`,
  https://github.com/mtzanidakis/praktor/commit/c3731eeda01c0b3ec1dbd13cccd5a147c3182141.diff

`citations.tsv` is the single table of cited ranges; for each range it
stores the SHA-256 of the cited text. Without `C9_DIFF` (as in CI) the
content check is an explicit **skip**; with `C9_DIFF` every range hash
is verified.

```sh
curl -fsSL -o /tmp/CVE-2026-62331_praktor_c3731eeda01c.diff https://github.com/mtzanidakis/praktor/commit/c3731eeda01c0b3ec1dbd13cccd5a147c3182141.diff
sha256sum /tmp/CVE-2026-62331_praktor_c3731eeda01c.diff   # must be d2075c6f2000517ee13ae828367203464b27ac8fb287cc96515a18f11a52cffd
C9_DIFF=/tmp/CVE-2026-62331_praktor_c3731eeda01c.diff PYTHONPATH=src python3 -m unittest -v tests.test_citations
```

## Run

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/derive_expected.py | diff - fixtures/expected.tsv
python3 scripts/gen_results.py /tmp/r && diff -r results /tmp/r
```

A model is not a finding. See [LIMITATIONS.md](LIMITATIONS.md) and
[SOURCES.md](SOURCES.md). License: Apache-2.0.
