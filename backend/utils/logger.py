# backend/utils/logger.py
import os
import sys
from loguru import logger

# 动态获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = os.path.join(BASE_DIR, "data", "logs")

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger():
    """初始化 Loguru 配置"""
    logger.remove()  # 移除默认的控制台输出

    # 1. 终端输出（适合开发时人类阅读，带高亮彩色）
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        enqueue=True
    )

    # 2. 文件输出（记录更详细的 DEBUG 级 RAG 链路信息，并以文本/JSON 混合存储）
    log_file_path = os.path.join(LOG_DIR, "rag_system.log")
    logger.add(
        log_file_path,
        level="DEBUG",
        rotation="20 MB",       # 超过 20MB 自动打包新文件
        retention="7 days",     # 保留 7 天内的日志
        compression="zip",      # 历史日志压缩存储
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        enqueue=True            # 异步安全，防止 Streamlit 多线程并发冲突
    )

# 自动激活配置
setup_logger()

# 导出供其他模块导入
__all__ = ["logger"]