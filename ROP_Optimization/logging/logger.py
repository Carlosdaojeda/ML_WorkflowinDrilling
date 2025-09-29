import logging
import os
from datetime import datetime

# Define log directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log file path
LOG_FILE = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()  # also print to console
    ]
)

# 👇 este es el objeto que debes exportar
logger = logging.getLogger("ROP_Optimization")
