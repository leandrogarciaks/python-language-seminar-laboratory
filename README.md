// Para crear un entorno virtual
python -m venv .venv
python3.12 -m venv .venv

// Para activar entorno virtual
source .venv/bin/activate

// Para desactivar entorno virtual
deactivate

// Para ejecutar un archivo, por ejemplo:
python ventas.py

// Para abrir el archivo de base de datos SQLite Browser (DB Browser for SQLite
sqlitebrowser ventas.db

// Instalar FastApi standard en proyecto y sqlalchemy
pip install "fastapi[standard]"
pip install sqlalchemy

// Guarda en un archivo todas las dependecias que estan instaladas en el proyecto
pip freeze > requirements.txt

// Para activar la app y ir viendo el proceso/errores de ejecución cuando se programa
fastapi dev app.py

z// CONSULTAS

1- El intelligente no funciona o tengo que hacer algo para activar eso? cada vez que coloco Column no lo importa automaticamente, o el ForeignKey, .query.all(), .query.get() como activar el intelligente

2-
