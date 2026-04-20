# 📊 Análisis de Contaminación Atmosférica CDMX

### Implementación de la NOM-172-SEMARNAT-2023

## 🎯 Objetivo del Proyecto

Este repositorio contiene herramientas para procesar y analizar los datos de calidad del aire de la Ciudad de México. El enfoque principal es la asignación y cálculo de los valores del índice **AIRE y SALUD**, bajo los lineamientos técnicos de la **NOM-172-SEMARNAT-2023**.

Los datos se obtienen directamente del sistema oficial de [Monitoreo de Calidad del Aire de la CDMX](https://www.aire.cdmx.gob.mx/).

## 🛠️ Metodología de Procesamiento

1.  **Adquisición:** Descarga automatizada de series históricas horarias.
2.  **Limpieza:** Tratamiento de valores nulos y normalización de unidades.
3.  **Cálculo de Índice:** Aplicación de algoritmos de clasificación basados en la normativa vigente para contaminantes como $PM_{10}$, $PM_{2.5}$, $PM_{CO}$, $O_3$, $NO$, $NO_2$, $NO_X$, $SO_2$ y $CO$.

## 📥 Obtención de Datos

Para mantener la reproducibilidad, se recomienda organizar los archivos fuente en un directorio local. Puedes utilizar el siguiente flujo de comandos para descargar los datos más recientes:

```bash
# Crear estructura de carpetas
mkdir -p 00-data/raw
cd 00-data/raw

# Descargar datos horarios del 2025
# Nota: Se especifican ciphers para aceptar los certificados del servidor de aire
curl -O -k --ciphers 'DEFAULT:!DH' https://aire.cdmx.gob.mx/descargas/Opendata/anuales_horarios_gz/contaminantes_2025.csv.gz
```

## 🏗️ Estructura del Repositorio

  * `00-data/`: Almacenamiento de datos crudos (`raw`) y procesados.
  * `01-scripts/`: Scripts de procesamiento de datos.
  * `src/`: Paquete de utilidades para análisis de contaminación.
  * `98-tests/`: Tests para las funciones del paquete `src/contaminacion/data/transform.py`.

## 📝 Tarea

El objetivo de este desarrollo es dejar una tarea práctica basada en procesar información anual de contaminantes atmosféricos para calcular el índice de Aire y Salud que define la **NOM-172-SEMARNAT-2023**.

La tarea consiste en escribir el cuerpo de las siguientes funciones:

- `transform.mean_8h_co` (30 puntos)
- `transform.calcular_promedio_movil_ponderado` (30 puntos)
- `transform.asigna_indice_aire_salud` (30 puntos)

**Total:** 90 puntos.
