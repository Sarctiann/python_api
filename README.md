# Proyecto Final - API

![banner](README/bootcamp3.png)

- ### [classroom](https://classroom.google.com/c/Njk3OTE0NjEwMDI2)
- ### [Requerimentos de aplicación](README/AppRequirements.md)

---

## Instrucciones (lazy version, para usuarios de VSCode)

1. Abrir la previsualización de este archivo para continuar:

   - `[CTRL] + [SHIFT] + [V]` (Windows/linux) o `[CMD] + [SHIFT] + [V]` (Mac)

1. Poné [buena música](https://youtu.be/n7_cjH8SlHI?si=JRRArISSHXEaiekr&t=530)
   y volvé.
1. [Instalar Python 3.12](https://www.python.org/downloads/)
1. Instalar poetry (global):

   - `pip install poetry` (windows) o `pipx install poetry` (linux/mac)

1. Configurar poetry:

   - `poetry config virtualenvs.in-project true`

1. Crear el `venv` e instalar las dependencias:

   - `poetry install`

1. Abrir el directorio de lproyecto en VSCode.
1. Configurá las variables de entorno seteando los valores de
   [`.env.example`](.env.example) en un nuevo archivo con el nombre `.env`.

1. En VSCode seleccionar el interprete correspondiente:

   - `[CTRL] + [SHIFT] + [P]` (Windows/linux) o `[CMD] + [SHIFT] + [P]` (Mac)
     tipear: _Python: Select Interpreter_ y seleccionar el que se corresponde con
     el entorno creado por `poetry`

   > Alternativa: Revisar la barrar de estado (la que está en la base de la
   > ventana de VSCode), si abrimos un archivo Python (ej. `main.py`) deberíamos ver
   > el interprete seleccionado en esta barra. y podemos cambiarlo clcikando ahí.

1. Ahora si abrimos una terminar integrada de VSCode el entorno viertual debería
   activarse automaticamente.

   - (Pero por si acaso, se puede activar manualmente
     con `poetry shell`).

1. Corremos nuestro server:

   - `fastapi dev`

1. Como debería decir la la consola, visitá
   [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

---

## Para hacer pruebas

De regalo tenemos declarado a `ptpython` como dependencia de desarrollo. PTPython
es un interprete de python mucho mas amigable y configurable. Como ejemplo pueden
probar lo siguiente:

1. abran una terminal (asegurense de que el entorno virtual está activado)
1. ejecuten `ptpython`

   - Ahora estamos en REPL de python

   1. `from pprint import pprint`
   1. `from api.config import db`
   1. `pprint(list(db.products.find()), indent=4)`

      - El verdadero beneficio está en la ayuda que nos va a ofrecer ptpython cuando
        tipeamos nuestros scripts.

   1. para salir `quit()` or `exit()` (igual que en el interprete común)

---

---

### TODO:

- Modificar los scripts
  - seed_database
  - drop_collections
- Actualizar los servicios
  - incluir el aggregate
  - cambiar str -> ObjectId
  - revisar los métodos
- Proteger los endpoints
  - HTTPExceptions
