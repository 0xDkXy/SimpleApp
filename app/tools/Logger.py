import os
import time
from loguru import logger


if not os.path.exists(r'./logs'):
    os.mkdir(r'logs')

logPath = os.path.join('./logs', f'{time.strftime("%Y-%m-%d")}.log')
print(logPath)
logger.add(
    logPath, 
    rotation="12:00", 
    retention="5 days",
    enqueue=True,
    format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}'
)
