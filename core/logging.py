import logging, pathlib
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

LOG_DIR = pathlib.Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

def get_logger():
    logger = logging.getLogger("lab_router")
    logger.setLevel(logging.INFO)
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')

    fh = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger

logger = get_logger()
