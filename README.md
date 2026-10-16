Fastapi Python Example for UNLa SL

## Instalation

- Open Powershell/Bash/Terminal and navigate to project folder.
- Run `python -m venv .venv` for creating venv.
- Run `.venv/Scripts/activate` for activating venv on Windows.
- Run `pip install -r requirements.txt` for installing libraries from requirements file.
- Run `fastapi run` for running app at localhost and default port (8000).
- Open browser and go to [localhost:8000/docs](localhost:8000/docs) for swagger documentation.

// Para crear un entorno virtual<br>
python -m venv .venv
python3.12 -m venv .venv

// Para activar entorno virtual<br>
source .venv/bin/activate

// Para desactivar entorno virtual<br>
deactivate

// Para ejecutar un archivo, por ejemplo:<br>
python ventas.py

// Para abrir el archivo de base de datos SQLite Browser (DB Browser for SQLite<br>
sqlitebrowser ventas.db

// Instalar FastApi standard en proyecto y sqlalchemy<br>
pip install "fastapi[standard]" pip install sqlalchemy

// Guarda en un archivo todas las dependecias que estan instaladas en el proyecto<br>
pip freeze > requirements.txt

// Para activar la app y ir viendo el proceso/errores de ejecución cuando se programa<br>
fastapi dev app.py

uvicorn app:app --reload
