from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import app.core.config as cfg

class MemoryRetriever:
    """
    Sử dụng vector search để truy xuất những phần liên quan nhất từ lịch sử chat.
    Nó không lưu trữ trạng thái lâu dài.
    """
    def __init__(self, top_k: int = 5):
        # Khởi tạo model embedding một lần duy nhất. 
        # Model này khá nhẹ và có thể tái sử dụng.
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=cfg.EMBEDDING_MODEL
        )
        self.top_k = top_k
        print("INFO:     MemoryRetriever initialized with HuggingFace embeddings.")

    def retrieve(self, message: HumanMessage, history: List[BaseMessage]) -> List[BaseMessage]:
        """
        Nhận vào câu hỏi hiện tại và toàn bộ lịch sử, trả về các tin nhắn liên quan nhất.
        """
        if not history:
            return [] # Trả về list rỗng nếu không có lịch sử

        # 1. Chuyển đổi lịch sử thành các 'Documents' mà vector store có thể hiểu
        # Chúng ta sẽ nối cặp câu hỏi-trả lời lại với nhau để giữ ngữ cảnh
        docs = []
        for i in range(0, len(history), 2):
            if i + 1 < len(history) and isinstance(history[i], HumanMessage) and isinstance(history[i+1], AIMessage):
                combined_content = f"User asked: {history[i].content}\nAI answered: {history[i+1].content}"
                docs.append(Document(page_content=combined_content))
        
        if not docs:
            return []

        # 2. Xây dựng một vector store Chroma tạm thời trong bộ nhớ RAM
        try:
            vector_store = Chroma.from_documents(
                documents=docs, 
                embedding=self.embedding_model
            )
        except Exception as e:
            print(f"ERROR:    Could not create in-memory Chroma store: {e}")
            return []

        # 3. Thực hiện tìm kiếm tương đồng
        print(f"DEBUG:    Searching relevant history for query: '{message.content}'")
        results = vector_store.similarity_search(message.content, k=self.top_k)
        
        # 4. Chuyển đổi kết quả tìm kiếm trở lại thành BaseMessage
        # (Sử dụng AIMessage hoặc một loại message tùy chỉnh để biểu thị đây là context)
        from langchain_core.messages import SystemMessage
        retrieved_messages = [SystemMessage(content=f"[Context from past conversation]:\n{doc.page_content}") for doc in results]

        return retrieved_messages