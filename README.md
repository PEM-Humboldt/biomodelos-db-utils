# Biomodelos DB utils

Utilitarios para BioModelos

## Prerrequisitos
* [Python](https://www.python.org/downloads/) (v. 3.8+)
* Librerías del sistema de GDAL (si instala usando Conda no es necesario)

## Instalación

### Usando Conda

Por facilidad en la instalación de dependencias del sistema, se recomienda usar [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) para la instalación de la herramienta.

1. Instalar conda
1. Instalar dependencias del ambiente del repositorio:

    ```
    conda env create --file condaenv.yml
    ```
1. Activar el ambiente recién restaurado

    ```
    conda activate bm-db-utils
    ```
1. Instalar la herramienta:

    ```
    pip install git+https://github.com/PEM-Humboldt/biomodelos-db-utils.git#egg=bmdbutils
    ```

En este momento tendrá disponible el comando `bmdbutils`.

En futuras ocasiones cuando desee usar la herramienta primero deberá activar el ambiente de conda (`conda activate bm-db-utils`), podrá hacerlo desde cualquier ubicación.

### Usando Virtualenv

Si lo desea, puede crear un ambiente virtual para trabajar con la herramienta sin afectar su ambiente general, para esto:

> 1. Cree el ambiente:
> `python3 -m venv bmdbutils`
> 2. Active el ambiente:
> `source bmdbutils/bin/activate`

Si está usando una versión de Python >= 3.9, primero instale setuptools versión 58:

```
pip install setuptools==58
```

Puede instalar `bmdbutils` ejecutando el siguiente comando:

```
pip install git+https://github.com/PEM-Humboldt/biomodelos-db-utils.git#egg=bmdbutils
```

Si no tiene `git`, ejecute:

```
pip install --upgrade https://github.com/PEM-Humboldt/biomodelos-db-utils/tarball/master
```

Para asegurarse que bmdbutils haya quedado instalado, ejecute:

```
python -c "import bmdbutils"
```

Si la instalación fue exitosa, el comando correrá sin ningún problema.

## Ejecución

Ejecute el comando `bmdbutils` para ver los subcomandos disponibles y la ayuda de los mismos.
## Cómo contribuir

### Configuración del entorno de desarrollo
Para el desarrollo se requiere [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html), que se encarga de crear el ambiente de desarrollo, instalar dependencias base (para no tener que instalar librerías del sistema operativo) e instalar poetry, gestor de empaquetado y manejador de las demás dependencias.

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
conda env create --file condaenv.yml
```

después, active el ambiente recién restaurado

```
conda activate bm-db-utils
```

e instale el resto de dependencias necesarias:

```
poetry install
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
