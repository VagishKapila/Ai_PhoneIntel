# uvicorn_config.py

import multiprocessing

# Number of workers for production (optional)
workers = max(1, multiprocessing.cpu_count() - 1)

CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True,
    "reload_exclude": [
        "venv/*",
        "**/*.pyc",
        "*/site-packages/*"
    ],
    "workers": 1,   # Always 1 for reload mode
}