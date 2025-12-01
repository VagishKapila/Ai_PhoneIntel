from uvicorn import run
from uvicorn_config import CONFIG

if __name__ == "__main__":
    run("fastapi_app.main:app", **CONFIG)