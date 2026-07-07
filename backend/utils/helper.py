# backend/utils/helper.py
import os
import hashlib
from datetime import datetime

# ==========================================
# 1. 文件与路径管理工具 (前端上传、后端解析都会用)
# ==========================================

def get_file_extension(filename: str) -> str:
    """获取文件后缀名（统一转小写），用于前端上传时的格式校验"""
    if not filename or '.' not in filename:
        return ""
    return filename.split('.')[-1].lower()


def sanitize_filename(filename: str) -> str:
    """
    清理文件名中的特殊字符，防止拼音、空格或特殊符号导致本地保存或 Chroma 读取时报错
    """
    # 替换掉 Windows/Linux 常见的敏感路径字符
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ', '\t']
    clean_name = filename
    for char in invalid_chars:
        clean_name = clean_name.replace(char, "_")
    return clean_name


# ==========================================
# 2. 安全与唯一哈希计算 (用于给 Document 和 Chunk 生成不重复的 ID)
# ==========================================

def calculate_text_md5(text: str) -> str:
    """
    计算一段文本的 MD5 值。
    【核心用途】：队友写的 Chunk 和 Document 模型都需要一个唯一的 id。
    直接用文本内容算 MD5，如果文本没变，算出来的 ID 就永远不变，能有效防止知识库重复导入！
    """
    if not text:
        return ""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


# ==========================================
# 3. 文本清洗与格式化工具 (用于优化喂给大模型的 Prompt)
# ==========================================

def clean_pdf_text(text: str) -> str:
    """
    清洗从 PDF 中提取出来的原始文本。
    去除多余的空格、密集的换行、特殊页眉页脚乱码，提高大模型阅读上下文的质量。
    """
    if not text:
        return ""
    # 去除首尾空格
    text = text.strip()
    # 把连续的多个换行替换成单个换行
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return "\n".join(lines)


def format_latency(seconds: float) -> str:
    """统一将耗时格式化为人类可读的字符串"""
    if seconds < 1.0:
        return f"{seconds * 1000:.0f} ms"
    return f"{seconds:.2f} s"