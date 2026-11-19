# Guía práctica (6 niveles)

Ejercicios **offline**. No se habla con Telegram ni se escribe ningún
archivo. Si quieres ver praktor real, hazlo en un entorno de laboratorio
tuyo.
Respuestas en `tests/test_practice.py`.

Ayuda: `PYTHONPATH=src python3 -c "from c9praktor import paths; print(paths.analyze('pre','../../../NOTES.md'))"`.

**Básico**

1. **Nombre sano.** `ok.txt` en pre. (`IN_UPLOADS`)
2. **Tres `..`.** `../../../NOTES.md` en pre. (`IN_VOLUME` — cae en
   `/vol/NOTES.md`, c3731eed:L55-56)

**Intermedio**

3. **El fix.** Lo mismo en post. (`IN_UPLOADS`, `path.Base`, c3731eed:L76)
4. **Cuatro `..`.** `../../../../NOTES.md` en pre. (`ESCAPES_VOLUME`)

**Avanzado**

5. **La segunda puerta.** `../etc/x` pasado solo a `WriteVolumeBytes`
   (`site=write`): pre `ESCAPES_VOLUME`, post `REJECTED` (c3731eed:L59-62).
6. **Observación o01.** El mismo `../etc/x` en el camino de Telegram
   (con el prefijo `uploads/<ts>_`) no escapa `uploads/`. ¿Por qué?

Más allá: agrega un caso a `fixtures/cases.json` y regenera expected.tsv.
