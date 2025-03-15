import logging
import os
from datetime import datetime

logFile = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logsPath = os.path.join(os.getcwd(),"logs",logFile)

os.makedirs(logsPath,exist_ok=True)

logFilePath = os.path.join(logsPath,logFile)

logging.basicConfig(
    filename = logFilePath,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO

)


