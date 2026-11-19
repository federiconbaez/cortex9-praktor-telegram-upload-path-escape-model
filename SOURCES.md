# Sources

Line citations: see "Line citations" below. The official fix diff is
not copied into this repo; `sources/diffs.tsv` names it.

| Source | URL | Used for | SHA-256 |
|---|---|---|---|
| Commit c3731eeda01c0b3ec1dbd13cccd5a147c3182141 (v0.9.1) as `CVE-2026-62331_praktor_c3731eeda01c.diff` | https://github.com/mtzanidakis/praktor/commit/c3731eeda01c0b3ec1dbd13cccd5a147c3182141 | pre c3731eed:L55-56, c3731eed:L75, c3731eed:L84; post c3731eed:L59-62, c3731eed:L76, c3731eed:L85 | d2075c6f2000517ee13ae828367203464b27ac8fb287cc96515a18f11a52cffd |
| GHSA-48v2-6jcm-fc99 | https://github.com/advisories/GHSA-48v2-6jcm-fc99 | affected <=0.9.0, patched 0.9.1, CWE-22 | fetched 2026-11-19 via `https://api.github.com/advisories/GHSA-48v2-6jcm-fc99` |
| Vendor advisory | https://github.com/mtzanidakis/praktor/security/advisories/GHSA-48v2-6jcm-fc99 | same; describes `path.Base` and the `/vol` prefix check | same advisory family |
| cve.org (PUBLISHED) | https://www.cve.org/CVERecord?id=CVE-2026-62331 | PUBLISHED; CWE-22; <0.9.1; same commit | fetched 2026-11-19 via `https://cveawg.mitre.org/api/cve/CVE-2026-62331` |
| NVD (Deferred) | https://nvd.nist.gov/vuln/detail/CVE-2026-62331 | CVE exists; Deferred; CWE-22; affected <0.9.1 | fetched 2026-11-19 via `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-62331` |

No instruction directed at this agent was found in those pages or in the
diff; language about stored instruction injection is ordinary advisory
text and was treated as data.

## Line citations (diff not in this repo)

Every line citation has the form `<tag>:L<n>` or `<tag>:L<n>-<m>`: the real
`cat -n` line(s) of the official fix diff. The diff is **not** included in
this repo; `sources/diffs.tsv` names it:

- `c3731eed` → `CVE-2026-62331_praktor_c3731eeda01c.diff`, SHA-256 `d2075c6f2000517ee13ae828367203464b27ac8fb287cc96515a18f11a52cffd`,
  https://github.com/mtzanidakis/praktor/commit/c3731eeda01c0b3ec1dbd13cccd5a147c3182141.diff

`citations.tsv` is the single table of cited ranges; for each range it
stores the SHA-256 of the cited text (lines `start`..`end` of the diff
exactly as stored, joined with `\n`, no final newline, UTF-8; shell:
`sed -n "${start},${end}p" "$C9_DIFF" | head -c -1 | sha256sum`).

```sh
curl -fsSL -o /tmp/CVE-2026-62331_praktor_c3731eeda01c.diff https://github.com/mtzanidakis/praktor/commit/c3731eeda01c0b3ec1dbd13cccd5a147c3182141.diff
sha256sum /tmp/CVE-2026-62331_praktor_c3731eeda01c.diff   # must be d2075c6f2000517ee13ae828367203464b27ac8fb287cc96515a18f11a52cffd
C9_DIFF=/tmp/CVE-2026-62331_praktor_c3731eeda01c.diff PYTHONPATH=src python3 -m unittest -v tests.test_citations
```

Without `C9_DIFF` (as in CI) `tests/test_citations.py` checks the table
format, that every citation in the repo is in the table and that none lacks
a tag, and reports the content check as an explicit **skip**.
