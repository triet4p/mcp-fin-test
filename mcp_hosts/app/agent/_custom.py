from typing import Callable, List
from langchain.agents import AgentExecutor
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain_core.load import dumps, loads
from langchain_core.caches import BaseCache
from langchain_core.outputs import Generation
from app.memory.retriever import MemoryRetriever

class SemanticMemoryAndCacheAgentExecutor:
    def __init__(self,
                 base_agent_exec: AgentExecutor,
                 chat_history_getter: Callable[[str], BaseChatMessageHistory],
                 memory_retriever: MemoryRetriever,
                 agent_cache: BaseCache
                 ):
        self.base_agent_exec = base_agent_exec
        self.chat_history_getter = chat_history_getter
        self.memory_retriever = memory_retriever
        self.agent_cache = agent_cache
        
    def _create_cache_key(self, message: HumanMessage, retrieved_history: List[BaseMessage]) -> str:
        """Tạo một prompt 'sạch' và ổn định để dùng làm key cho cache."""
        context = "\n".join([m.content for m in retrieved_history])
        return f"Context:\n{context}\n\nUser Question:\n{message.content}"
    
    def invoke(self, input_str: str, session_id: str):    
        human_message = HumanMessage(content=input_str)
        
        # 1. Lấy lịch sử chat đầy đủ (cho việc cập nhật và truy xuất)
        chat_history = self.chat_history_getter(session_id)
        print(f'INFO: Successfully get {len(chat_history.messages)} history.')
        
        # 2. Dùng Retriever để lấy ngữ cảnh liên quan
        retrieved_memory = self.memory_retriever.retrieve(human_message, chat_history.messages)
        print(f'INFO: Successfully retrieved memory with {len(retrieved_memory)}')
        
        # 3. Tạo cache key và kiểm tra cache
        cache_key = self._create_cache_key(human_message, retrieved_memory)
        # `llm_string` không quan trọng với cache tùy chỉnh của chúng ta, có thể để trống
        cached_result = self.agent_cache.lookup(cache_key, "")
        print(f'INFO: CACHE RESULTS: {len(cached_result) if cached_result else 0}')
        
        if cached_result:
            # Deserialize kết quả từ cache và trả về
            return loads(cached_result[0].text)

        # 4. Nếu cache miss, thực thi Agent
        result = self.base_agent_exec.invoke({
            "input": input_str,
            # Prompt của bạn cần được sửa để dùng key này
            "retrieved_chat_history": retrieved_memory, 
        })

        # 5. Cập nhật cache và history
        # Serialize kết quả thành chuỗi để lưu vào cache
        self.agent_cache.update(cache_key, "", [Generation(text=dumps(result))])

        # Cập nhật chat history lâu dài
        chat_history.add_messages([human_message, AIMessage(content=result["output"])])
        
        return result