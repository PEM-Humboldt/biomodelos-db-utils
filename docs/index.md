# Biomodelos DB Utils

**Biomodelos DB Utils** es una herramienta de línea de comandos (CLI) que actúa como conjunto de utilitarios para la plataforma **BioModelos**, facilitando tareas de configuración, validación, carga y consulta de información.

## Características principales

- Configuración de servicios utilizados por Biomodelos, incluyendo:
  - API
  - Base de datos PostgreSQL
  - Base de datos MongoDB
  - GeoServer
- Validación y carga de modelos `.tif` en GeoServer.
- Validación, corrección y carga de registros desde archivos CSV.
- Consulta de variables ecológicas, ediciones y calificaciones asociadas a especies.
- Obtención de estadísticas históricas de uso de la plataforma (usuarios, modelos, descargas y grupos).
- Validación de archivos CSV y modelos antes de su carga.

## Requisitos previos

- Acceso a los servicios de Biomodelos (API, bases de datos y GeoServer), ya sea en entorno local o de producción.
- Credenciales válidas para los servicios que se desean configurar o consultar.

## Instalación y ejecución

👉 Para instalar la herramienta, se recomienda seguir los pasos descritos en el [repositorio oficial del proyecto](https://github.com/PEM-Humboldt/biomodelos-db-utils).

Su ejecución se realiza a partir del comando `bmdbutils`, y como paso inicial es necesario configurar la base de datos de [Postgres](setup.md), [Mongo](mongo.md) y el [GeoServer](geoserver.md). Esta configuración es obligatoria si se trabaja desde un ambiente local o de pruebas, puesto que las configuraciones por defecto apuntan a producción. 
 