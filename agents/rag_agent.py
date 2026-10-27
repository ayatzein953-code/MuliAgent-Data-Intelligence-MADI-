import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class RAGAgent:
    def init(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        # استخدام نماذج تضمين خفيفة ومجانية ومحلية
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
    def get_retriever(self):
        """
        إعداد وربط قاعدة البيانات المتجهة ChromaDB للاسترجاع
        """
        if os.path.exists(self.persist_directory):
            vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            return vectorstore.as_retriever(search_kwargs={"k": 3})
        return None

    def search_knowledge_base(self, query: str) -> str:
        """
        أداة بحث يقوم من خلالها الـ Agent باسترجاع النصوص ذات الصلة من قاعدة المعرفة.
        """
        retriever = self.get_retriever()
        
        if not retriever:
            return "تنبيه: لا توجد قاعدة بيانات متجهة (ChromaDB) مخزنة حتى الآن. يرجى إضافة مستندات أولاً."
        
        try:
            # البحث عن المستندات الأكثر صلة بالسؤال
            docs = retriever.invoke(query)
            
            if not docs:
                return "لم يتم العثور على معلومات مطابقة في قاعدة المعرفة."
            
            # تجميع النصوص المسترجعة
            context = "\n\n".join([doc.page_content for doc in docs])
            
            report = f"""
            [تقرير Research & RAG Agent]
            - تم العثور على {len(docs)} مقاطع ذات صلة بالاستعلام: "{query}"
            
            - السياق المسترجع (Context):
            {context}
            """
            return report
            
        except Exception as e:
            return f"حدث خطأ أثناء البحث في قاعدة المعرفة: {str(e)}"
