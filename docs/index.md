# BioModelos DB Utils (bmdbutils)

**BioModelos DB Utils** es una herramienta de línea de comandos (CLI) que actúa como conjunto de utilitarios para la plataforma **[BioModelos](https://biomodelos.humboldt.org.co/)**, facilitando tareas de configuración, validación, carga y consulta de información.

## Requisitos previos

- Acceso a los servicios de BioModelos (API, bases de datos y GeoServer), ya sea en entorno local o de producción.
- Credenciales válidas para los servicios que se desean configurar o consultar.

## Instalación y ejecución

- Para instalar la herramienta, se recomienda seguir los pasos descritos en el [repositorio oficial del proyecto](https://github.com/PEM-Humboldt/biomodelos-db-utils/#instalaci%C3%B3n).

- La ejecución de la herramienta se realiza a partir del comando `bmdbutils`, y como paso inicial es necesario configurar las conexiones a la base de datos de [Postgres](setup_postgres.md), [MongoDB](setup_mongo.md), la [API](setup_api.md) y el [GeoServer](setup_geoserver.md). Esta configuración inicial es obligatoria, y una vez realizada es almacenada hasta que se quiera reconfigurarla.

## Comandos

Una vez instalada la herramienta, el comando principal es `bmdbutils`, y a partir de este hay 4 comandos principales: `Setup`, `Stats`, `Records` y `Models`, los cuales por si solos no ejecutan nada, para esto cada comando tiene un set de subcomandos de acuerdo a cada funcionalidad.

- `Setup`: Comando general para configurar la conexión a la API, al Geoserver y a las bases de datos PostgreSQL y MongoDB para Biomodelos. Este comando posee una serie de subcomandos para ejecutar las configuraciones necesarias.

    - Subcomandos:
        - [API](setup_api.md).
        - [Geoserver](setup_geoserver.md).
        - [Mongo](setup_mongo.md).
        - [Postgres](setup_postgres.md).

- `Stats`: Comando para realizar consultas relacionadas con estadísticas de uso de BioModelos.

    - Subcomandos:
        - [Downloads](stats_downloads.md).
        - [Groups](stats_groups.md).
        - [Models](stats_models.md).
        - [Users](stats_users.md).

- `Records`: Comando para validar y cargar registros de un archivo CSV a la colección Records de la base de datos MongoDB de BioModelos.

    - Subcomandos:
        - [Validate](records_validate.md).
        - [Upload](records_upload.md).

- `Models`: Comando que permite consultar información sobre ecovariables, ediciones y rating de modelos, además de permitir la carga de metadatos a modelos sobre modelos existentes en la plataforma y cargar modelos al Geoserver.

    - Subcomandos:
        - [Ecovars](models_ecovars.md).
        - [Editions](models_editions.md).
        - [Ratings](models_ratings.md).
        - [Fix_metadata](models_fix_metadata.md).
        - [Geoserver_upsert](models_geoserver_upsert.md).

## Características principales de la herramienta

- Configuración de servicios utilizados por BioModelos, incluyendo:
  - API
  - Base de datos PostgreSQL
  - Base de datos MongoDB
  - GeoServer
- Validación y carga de modelos `.tif` en GeoServer.
- Validación, corrección y carga de registros desde archivos CSV.
- Consulta de variables ecológicas, ediciones y calificaciones asociadas a especies.
- Obtención de estadísticas históricas de uso de la plataforma (usuarios, modelos, descargas y grupos).
- Validación de archivos CSV y modelos antes de su carga.
