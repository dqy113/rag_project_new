import os
import fitz
from docx import Document
from pptx import Presentation


def load_document(file_path):
    """
    根据文件类型自动读取文档
    返回格式：
    [
        {
            "content": "...",
            "source": "xxx.pdf",
            "page": 1
        }
    ]
    """
    suffix = os.path.splitext(file_path)[1].lower()

    if suffix == ".pdf":
        return read_pdf(file_path)

    elif suffix == ".txt":
        return read_txt(file_path)

    elif suffix == ".docx":
        return read_docx(file_path)

    elif suffix == ".pptx":
        return read_pptx(file_path)

    else:
        raise ValueError(f"暂不支持文件类型：{suffix}")


# ==========================
# PDF
# ==========================
def read_pdf(file_path):

    doc_list = []

    doc = fitz.open(file_path)

    for page_num, page in enumerate(doc):

        text = page.get_text().strip()

        if text:

            doc_list.append({
                "content": text,
                "source": os.path.basename(file_path),
                "page": page_num + 1
            })

    doc.close()

    return doc_list


# ==========================
# TXT
# ==========================
def read_txt(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return [{
        "content": text,
        "source": os.path.basename(file_path),
        "page": 1
    }]


# ==========================
# DOCX
# ==========================
def read_docx(file_path):

    doc = Document(file_path)

    text = "\n".join(
        p.text for p in doc.paragraphs
        if p.text.strip()
    )

    return [{
        "content": text,
        "source": os.path.basename(file_path),
        "page": 1
    }]


# ==========================
# PPTX
# ==========================
def read_pptx(file_path):

    prs = Presentation(file_path)

    doc_list = []

    for index, slide in enumerate(prs.slides):

        text = ""

        for shape in slide.shapes:

            if hasattr(shape, "text"):
                text += shape.text + "\n"

        if text.strip():

            doc_list.append({
                "content": text,
                "source": os.path.basename(file_path),
                "page": index + 1
            })

    return doc_list