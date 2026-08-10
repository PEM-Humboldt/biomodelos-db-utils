# Biomodelos DB utils

Utilitarios para BioModelos

Accede aquí la documentación de los comandos: [bm-db-utils](https://pem-humboldt.github.io/biomodelos-db-utils/)
## Prerrequisitos
* [Python](https://www.python.org/downloads/) (v. 3.10+)
* [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). Se recomienda instalar miniconda debido a que es más liviano.
* Librerías del sistema de GDAL (se instala usando Conda)
 

## Instalación

Para el SO **Windows**, todo se debe ejecutar adentro de la terminal de Conda.

1. Clonar el repositorio

    ```
    git clone https://github.com/PEM-Humboldt/biomodelos-db-utils.git
    ```

1. Instalar dependencias del ambiente del repositorio desde la raíz del proyecto:

    ```
    conda env create --file condaenv.yml
    ```

1. Activar el ambiente recién restaurado:

    ```
    conda activate bm-db-utils
    ```

1. Instalar la herramienta:

    ```
    pip install -e .
    ```

A partir de este momento tendrá disponible el comando `bmdbutils`, el cual en el caso del **OS Windows** debe ser ejecutado desde la terminal de Conda.

Para desactivar el comando es necesario desactivar ambiente:

    ```
    conda deactivate
    ```

En futuras ocasiones cuando desee usar la herramienta, primero debe activar el ambiente de conda (`conda activate bm-db-utils`), en **linux** esto se puede hacer desde cualquier terminal, pero en **windows** se debe ejecutar adentro de la terminal de conda o miniconda.

## Cómo contribuir

### Configuración del entorno de desarrollo

Para configurar este ambiente es necesario tener instalado Conda.

En primer lugar, es necesario clonar este repositorio localmente. Para esto, ejecute:

    ```
    git clone https://github.com/PEM-Humboldt/biomodelos-db-utils.git
    ```

Luego, ubíquese dentro del directorio del proyecto:

    ```
    cd biomodelos-db-utils
    ```

y restaure el ambiente de conda:

    ```
    conda env create --file dev.yml
    ```

después, active el ambiente recién restaurado

    ```
    conda activate bm-db-utils
    ```

e instale el resto de dependencias necesarias:

    ```
    pip install -e .
    ```

### Revision y formato de estilos para el código
Para hacer formateo de estilos automático se utiliza el paquete black, el cual se encuentra incuído adentro del ambiente. Al ejecutarlo se tendran en cuenta las configuraciones de estilo definidas en el archivo [pyproject.toml](https://github.com/PEM-Humboldt/biomodelos-db-utils/blob/master/pyproject.toml).

Ejecute el siguiente comando desde la raiz del repositorio para formatear todos los archivos que se encuentren adentro de la carpeta bmdbutils.

```
black bmdbutils
```

También se puede formatear cada archivo de forma individual.

```
black <nombre archivo>
```

### Tips
En caso de necesitar agregar nuevas dependencias, ejecute:

```
poetry add <dependencia>
poetry update
```

Para ejecutar bmdbutils sin tener que instalar como usuario final ejecute
```
poetry run bmdbutils
```

Es recomendable familiarizarse con la documentación de [poetry](https://python-poetry.org/docs/) y de [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html).

## Documentación

La documentación para la línea de comandos fue realizada con [MkDocs](https://www.mkdocs.org/). Los siguientes comandos deben ser ejecutados dentro del ambiente previamente configurado.

```sh
# Configuración de ambiente de desarrollo 
# 1. Instalación de librerías
pip install mkdocs mkdocs-macros-plugin mkdocs-gen-files mkdocs-literate-nav mkdocs-cinder
# 2. Reiniciar ambiente de conda
conda deactivate
conda activate bm-db-utils
# 3. Desplegar página en ambiente local (Ingresar a: http://127.0.0.1:8000/)
mkdocs serve

# Despliegue a Github Pages de producción
# 1. Generar documentación
mkdocs build
# 2. Desplegar página en github pages
mkdocs gh-deploy
```
