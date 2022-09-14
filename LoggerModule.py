import logging
import os

# Logging formatter
formatLOG = "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(message)s"

# Directory to store log files
if not os.path.exists("logs"):
    os.mkdir("logs")

# Setting Basic configuration for log file
logging.basicConfig(
    format=formatLOG,
    filename=os.path.join(os.getcwd(), "logs/log_file.log"),
    level=logging.INFO,
    filemode='a'
)

logs = logging.getLogger()