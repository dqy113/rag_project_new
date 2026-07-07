import os
import fitz

def read_all_pdfs(folder_path):
    doc_list = []
    # 遍历文件夹pdf文件
    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".pdf"):
            print(f"正在读取: {file}")
            file_full_path = os.path.join(folder_path, file)
            doc = fitz.open(file_full_path)
            # 逐页读取，记录文件名、页码
            for page_num, page in enumerate(doc):
                text = page.get_text().strip()
                if len(text) == 0:
                    continue
                # 每一页内容附带来源信息
                doc_list.append({
                    "content": text,
                    "source": file,
                    "page": page_num + 1
                })
            doc.close()
    return doc_list