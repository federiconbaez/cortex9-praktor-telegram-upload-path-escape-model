# cortex9-praktor-telegram-upload-path-escape-model

Modelo offline e inerte de **CVE-2026-62331** (GHSA-48v2-6jcm-fc99,
CWE-22). Antes de **0.9.1**, praktor concatenaba el nombre de archivo
de un documento de Telegram en `uploads/<timestamp>_<nombre>`
(c3731eed:L75, c3731eed:L84) y lo escribía con `path.Join("/vol",
filePath)` sin comprobar si escapaba (c3731eed:L55-56). Un nombre como
`../../../NOTES.md` resolvía en la raíz del volumen del agente.

El fix, commit `c3731eeda01c0b3ec1dbd13cccd5a147c3182141` (en **0.9.1**),
aplica `path.Base` en los dos sitios de subida (c3731eed:L76,
c3731eed:L85) y rechaza cualquier ruta de `WriteVolumeBytes` que
escape `/vol` después del Join (c3731eed:L59-62). Ver
[evidence/fix-in-0.9.1.md](evidence/fix-in-0.9.1.md).

Inglés: [README.md](README.md). Ejercicios: [PRACTICE.md](PRACTICE.md).

## Citas de líneas

Cada cita tiene la forma `<tag>:L<n>` o `<tag>:L<n>-<m>`: la línea real de
`cat -n` del diff oficial del fix. El diff **no** está en este repo;
`sources/diffs.tsv` lo identifica y `citations.tsv` guarda el SHA-256 de
cada rango. Sin `C9_DIFF` (como en CI) el chequeo de contenido es un
**skip** explícito.

## Uso

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/derive_expected.py | diff - fixtures/expected.tsv
python3 scripts/gen_results.py /tmp/r && diff -r results /tmp/r
```

Un modelo no es un hallazgo. Ver [LIMITATIONS.md](LIMITATIONS.md) y
[SOURCES.md](SOURCES.md). Licencia: Apache-2.0.
