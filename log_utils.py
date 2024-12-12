import os
import logging
from config import LOG_FOLDER

# 确保日志文件夹存在
os.makedirs(LOG_FOLDER, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    """
    设置日志记录器，优化日志格式和可读性
    """
    # 自定义格式，添加缩进和分隔符以提高可读性
    formatter = logging.Formatter(
        '\n%(asctime)s [%(levelname)s] %(name)s\n'
        '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
        '%(message)s\n'
    )
    
    log_path = os.path.join(LOG_FOLDER, log_file)
    handler = logging.FileHandler(log_path, encoding='utf-8')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.hasHandlers():
        logger.addHandler(handler)
    
    return logger

def truncate_long_text(text, max_length=500):
    """
    截断过长的文本内容，保留关键信息
    """
    if len(text) <= max_length:
        return text
    return f"{text[:max_length]}... (truncated, total length: {len(text)} chars)"

def format_function_args(args, kwargs):
    """
    格式化函数参数，提高可读性
    """
    args_str = ', '.join(repr(truncate_long_text(str(arg))) for arg in args)
    kwargs_str = ', '.join(f"{k}={repr(truncate_long_text(str(v)))}" for k, v in kwargs.items())
    return f"Args: [{args_str}]\nKwargs: {{{kwargs_str}}}" if kwargs_str else f"Args: [{args_str}]"

def log_execution(logger):
    """
    优化的函数执行日志装饰器
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 函数开始执行的日志
            logger.info(
                f"Function: {func.__name__}\n"
                f"{'─' * 40}\n"
                f"{format_function_args(args, kwargs)}"
            )
            
            try:
                result = func(*args, **kwargs)
                # 函数成功执行的日志
                logger.info(
                    f"Success: {func.__name__}\n"
                    f"{'─' * 40}\n"
                    f"Result: {truncate_long_text(str(result))}"
                )
                return result
            except Exception as e:
                # 错误日志
                logger.error(
                    f"Error in {func.__name__}\n"
                    f"{'─' * 40}\n"
                    f"Error Type: {type(e).__name__}\n"
                    f"Error Message: {str(e)}",
                    exc_info=True
                )
                raise
        return wrapper
    return decorator
