# Limitations

- **Path arithmetic only.** The model rebuilds the Telegram `volumePath`
  string and the `WriteVolumeBytes` join/prefix check. It does not talk
  to Telegram, Docker, a volume or an agent runtime, and it does not
  model stored-instruction effects. No files are written.
- **Go `path`, not `filepath`.** Joins and `Base` follow the slash-
  separated `path` package used by the fix (c3731eed:L59-62,
  c3731eed:L76, c3731eed:L85). Backslashes are ordinary characters
  (`o03`).
- **The timestamp prefix matters.** On the Telegram path the name is
  `uploads/<timestamp>_<filename>`, so the first `../` of a name like
  `../etc/x` is glued into `123_..` and does **not** escape `uploads/`
  (`o01`). The same raw name passed to `WriteVolumeBytes` does escape
  `/vol` (`p04`). This is a model observation, not a separate finding.
- **`o02`:** Go `path.Base("..")` is `".."`; the post path is still
  `uploads/123_..`, which stays under `uploads/`.
- **Defense in depth.** `path.Base` is what keeps Telegram uploads
  inside `uploads/`. The `/vol` prefix check (c3731eed:L59-62) is the
  second gate, for any caller of `WriteVolumeBytes`.
- The official fix diff is **not** in this repo (it also adds a
  `SECURITY.md` that contains a personal mailbox, which is out of
  scope). `sources/diffs.tsv` has the URL and SHA-256; set `C9_DIFF` to
  verify cited ranges.
- This is not a finding and not an exploit. The synthetic filename
  `NOTES.md` stands in for the workspace-file example in the advisory.
