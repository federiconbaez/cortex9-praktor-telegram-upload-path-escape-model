# Is commit c3731eed in praktor 0.9.1?

Answer: **yes**, according to the primary sources checked on 2026-11-19
(America/Buenos_Aires).

| Source | Result |
|---|---|
| [GHSA-48v2-6jcm-fc99](https://github.com/advisories/GHSA-48v2-6jcm-fc99) (and the vendor advisory) | affected `<= 0.9.0`, patched `0.9.1`; CWE-22; names PR 228 and the commit |
| [cve.org CVE-2026-62331](https://www.cve.org/CVERecord?id=CVE-2026-62331) | PUBLISHED; CWE-22; praktor `< 0.9.1`; references the commit, PR 228 and the v0.9.1 tag |
| [NVD CVE-2026-62331](https://nvd.nist.gov/vuln/detail/CVE-2026-62331) | Deferred; same description and references; CWE-22; affected `< 0.9.1` |
| Commit `c3731eeda01c0b3ec1dbd13cccd5a147c3182141` | merge of PR 228; `path.Base` at both upload sites and the `/vol` prefix check |
| Release | https://github.com/mtzanidakis/praktor/releases/tag/v0.9.1 |

`<= 0.9.0` (GHSA) and `< 0.9.1` (cve.org / NVD) describe the same range.
No git compare API was called for this note.
