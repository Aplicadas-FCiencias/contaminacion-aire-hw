# Análisis de datos de contaminación de la CDMX

## Descarga de información

Para descargar la información vamos a hacerlo usando `curl`

```bash
$ cd 00-data/raw
$ curl -O -k --ciphers 'DEFAULT:!DH' https://aire.cdmx.gob.mx/descargas/Opendata/anuales_horarios_gz/contaminantes_2025.csv.gz
```
