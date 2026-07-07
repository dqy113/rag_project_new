# backend/service/knowledge_service.py
import os
import json
import shutil
from backend.utils.logger import logger


class KnowledgeService:

    def __init__(self):
        self.data_dir = "data"
        # 🌟 用一个本地 JSON 文件来临时模拟“向量数据库”的注册表
        self.mock_db_path = os.path.join(self.data_dir, "mock_vector_db.json")

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        if not os.path.exists(self.mock_db_path):
            with open(self.mock_db_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _get_mock_db(self):
        """辅助函数：读取模拟数据库"""
        try:
            with open(self.mock_db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_mock_db(self, data):
        """辅助函数：保存模拟数据库"""
        with open(self.mock_db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ==========================
    # 1. 上传文档 接口
    # ==========================
    def upload_document(self, uploaded_file):
        """
        上传新文档（没有向量库情况下的模拟实现）
        """
        try:
            save_path = os.path.join(self.data_dir, uploaded_file.name)

            # 保存物理文件到 data 目录
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # 模拟写入向量库：把文件名登记到 JSON 注册表里
            db = self._get_mock_db()
            if uploaded_file.name not in db:
                db.append(uploaded_file.name)
                self._save_mock_db(db)

            logger.info(f"[Mock Service] 文件 {uploaded_file.name} 上传成功并已模拟向量化。")
            return {
                "success": True,
                "message": f"文档 {uploaded_file.name} 上传并模拟向量化成功！"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"上传失败: {str(e)}"
            }

    # ==========================
    # 2. 删除文档 接口
    # ==========================
    def delete_document(self, filename):
        """
        删除知识库中的文档
        """
        try:
            # 1. 从模拟向量库（JSON）中移除
            db = self._get_mock_db()
            if filename in db:
                db.remove(filename)
                self._save_mock_db(db)

            # 2. 删除 data 目录中的原文件
            file_path = os.path.join(self.data_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

            logger.info(f"[Mock Service] 文件 {filename} 已成功从模拟库与本地删除。")
            return {
                "success": True,
                "message": "删除成功"
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }

    # ==========================
    # 3. 更新文档 接口
    # ==========================
    def update_document(self, uploaded_file):
        """
        更新知识库（先删后复用上传）
        """
        self.delete_document(uploaded_file.name)
        return self.upload_document(uploaded_file)

    # ==========================
    # 4. 获取知识库所有文件 接口
    # ==========================
    def get_document_list(self):
        """
        获取当前模拟向量库里所有已经注册的文件名
        """
        # 直接返回 JSON 里的列表，这样前端下拉菜单就能动态更新了！
        return self._get_mock_db()

    # ==========================
    # 5. 重建知识库（可选）
    # ==========================
    def rebuild_database(self):
        """
        扫描 data 目录下的物理文件，重新同步到模拟数据库中
        """
        try:
            # 扫描 data 目录下真实存在的文件
            files = [f for f in os.listdir(self.data_dir) if f.endswith(('.pdf', '.txt', '.docx', '.pptx'))]

            # 重新写入模拟库
            self._save_mock_db(files)

            logger.info(f"[Mock Service] 模拟知识库重建完成，当前同步文件：{files}")
            return {
                "success": True,
                "message": f"模拟知识库重建完成，共同步 {len(files)} 个文件。"
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }