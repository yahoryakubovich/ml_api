from loguru import logger

logger.add(
    "file.log", rotation="1 week", level="INFO", format="{time} {level} {message}", backtrace=True, diagnose=True
)
