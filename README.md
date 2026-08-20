# Game Store

Una aplicación web sencilla desarrollada con **Flask** que expone un endpoint HTTP y devuelve una página HTML con información básica de una tienda de videojuegos.

## Descripción

El proyecto implementa un servidor web utilizando Flask. Al acceder al endpoint principal `/`, la aplicación devuelve una página HTML que contiene:

* **Título:** Game Store
* **Descripción:** Video Game Store and entertainment articles

## Requisitos

* Python 3.13
* Flask

## Instalación

1. Clona o descarga el proyecto.

2. Opcionalmente, crea un entorno virtual:

```bash
python -m venv venv/game-store-api
```

3. Activa el entorno virtual.

En Linux/macOS:

```bash
source venv/bin/activate
```

En Windows:

```bash
venv\Scripts\activate
```

4. Instala Flask:

```bash
pip install -r requirements
```

## Ejecución

Ejecuta la aplicación con:

```bash
python app.py
```

Por defecto, Flask iniciará el servidor en:

```text
http://127.0.0.1:5000/
```

También puedes acceder desde:

```text
http://localhost:5000/
```

## Endpoint

### `GET /`

Devuelve una página HTML con la información de la tienda.

**Ejemplo de respuesta:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Game Store</title>
</head>
<body>
    <h1>Game Store</h1>
    <p>Video Game Store and entertainment articles</p>
</body>
</html>
```

## Estructura del proyecto

```text
game-store/
│
├── app.py
└── README.md
```

## Tecnologías

* **Python**
* **Flask**
* **HTML**

## Desarrollo

La aplicación utiliza Flask para crear el servidor web y definir las rutas mediante decoradores. El endpoint `/` responde directamente con contenido HTML.

Para desarrollo, el servidor puede ejecutarse en modo debug modificando `app.py`:

```python
app.run(debug=True)
```

> **Nota:** El modo `debug` debe utilizarse únicamente durante el desarrollo y no en un entorno de producción.

## Licencia

Este proyecto es un ejemplo educativo y puede utilizarse y modificarse libremente con fines de aprendizaje.

