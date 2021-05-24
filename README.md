# Biomodelos DB utils

Utilitarios para BioModelos

## Prerrequisitos
* [Python](https://www.python.org/downloads/) (v. 3.8+)

## Instalación

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
Para el desarrollo se utiliza `poetry`, un auxiliar de empaquetado y gestor de dependencias. Antes de continuar debe [instalarlo](https://python-poetry.org/docs/#installation).

En primer lugar, es necesario clonar este repositorio localmente. Para esto, ejecute:

```
git clone https://github.com/PEM-Humboldt/biomodelos-db-utils.git
```

Luego, ubíquese dentro de del directorio del proyecto:

```
cd biomodelos-db-utils
```

e instale todas las dependencias necesarias:

```
poetry install
```

El entorno de desarrollo está listo y todas las dependencias necesarias están instaladas. En caso de necesitar agregar nuevas dependencias, ejecute:

```
poetry add <dependencia>
poetry update
```

Es recomendable familiarizarse con la [documentación](https://python-poetry.org/docs/) de `poetry`.
