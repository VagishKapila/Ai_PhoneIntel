import logging

logging.basicConfig(
    filename="shared/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

log = logging.getLogger("assistant")