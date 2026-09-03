# Game Store

Una aplicación web sencilla desarrollada con **Flask** que expone endpoints con información básica de una tienda de videojuegos.

## Descripción

El proyecto implementa un servidor web utilizando Flask.

## Requisitos

* Python 3.13
* Flask

## Instalación

1. Clona o descarga el proyecto.
```bash
git clone https://github.com/braulioceb/game-store-api.git
```

2. Opcionalmente, crea un entorno virtual:

```bash
python -m venv .venv/game-store-api
```

3. Activa el entorno virtual.

En Linux/macOS:

```bash
source .venv/game-store-api/bin/activate
```

En Windows:

```bash
.venv\game-store-api\Scripts\activate
```

En gitbash:

```bash
source .venv/game-store-api/Scripts/activate
```

4. Instala Flask:

```bash
pip install -r requirements.yml
```

4. Configuración de las variables de ambiente:

cambiar el nombre del archivo .env-example a .env y colocar las variables de ambiente correspondiente a la base de datos, como se muestra en el siguiente ejemplo:


```
DRIVER="MySQL ODBC 8.2 Unicode Driver"
SERVER=127.0.0.1
DATABASE=game-store
USER=root
PORT=3306
PWD=contraseña
```


## Ejecución

Ejecuta la aplicación con:

```bash
python app.py
```

## Detalles Ejecución

Por defecto, Flask iniciará el servidor en:

```text
http://127.0.0.1:5000/
```

También puedes acceder desde:

```text
http://localhost:5000/
```

Por defecto, el modo debug está habilitado 

```text
debug = True
```

## Estructura del proyecto

```text
game-store/
├── db                    # codigos de la base de datos
    ├── conn.py           # codigos para administrar la conexion a la base de datos
    └── utils.py          # db utils
├── .env-example          # archivo ejemplo para configuracion del ambiente
├── .gitignore            # archivos ignorados por git
├── app.py                # codigo de la app
├── info.md               # información de la app
├── README.md             # documentación de la info
└── requirements.yml      # ambiente de ejecución
```

## Tecnologías

* **Python**
* **Flask**
* **HTML**
* **ODBC**
* **Pandas**

## Endpoints

Listado de endpoints de la aplicación:

GET - "/" - Devuelve la página principal del proyecto.

GET - "/reports" - Devuelve la página general de reportes de Game Store.

GET - "/reports/sales" - Devuelve la página de reportes de ventas.

GET - "/reports/sales/<fecha>" - Devuelve la página html del reporte de ventas correspondiente a la fecha indicada mediante el parámetro de ruta <fecha>.

GET - "/reports/sales/hist" - Devuelve la página html del reporte de ventas historico. 

GET - "/api/reports/sales/hist" - Devuelve la informacion del reporte de ventas historico.

## Desarrollo

La aplicación utiliza Flask para crear el servidor web y definir las rutas mediante decoradores. 

Puede consultarse el nombre y el mapeo de endpoints de la app ejecutando el siguiente comando:

```bash
python info.py
```

> **Nota:** El modo `debug` debe utilizarse únicamente durante el desarrollo y no en un entorno de producción.

## Licencia

Este proyecto es un ejemplo educativo y puede utilizarse y modificarse libremente con fines de aprendizaje.