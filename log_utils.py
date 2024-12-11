import os
import logging
from config import LOG_FOLDER

# 确保日志文件夹存在
os.makedirs(LOG_FOLDER, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    """
    Set up a logger with the specified name, log file, and log level.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_path = os.path.join(LOG_FOLDER, log_file)

    # 设置文件处理器并显式指定 UTF-8 编码
    handler = logging.FileHandler(log_path, encoding='utf-8')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加 handler
    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger

def log_execution(logger):
    """
    Decorator to log the execution of a function while preserving exceptions and stack trace.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f"Entering function: {func.__name__} with args: {args}, kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Exiting function: {func.__name__} successfully with result: {result}")
                return result
            except Exception as e:
                logger.error(f"Error in function: {func.__name__} with args: {args}, kwargs: {kwargs}. Exception: {e}", exc_info=True)
                raise
        return wrapper
    return decorator
