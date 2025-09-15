from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import app.core.config as cfg
from app.llms import llm_client
from app.tools import get_all_tools
from app.prompts.loader import load_prompt
from app.memory import get_chat_message_history

SYSTEM_PROMPT = load_prompt(cfg.SYSTEM_PROMPT_ID, cfg.PROMPT_FILE)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name='chat_history'),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name='agent_scratchpad')
])

tools = get_all_tools()

agent = create_tool_calling_agent(llm_client, tools, prompt)

agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               verbose=True,
                               handle_parsing_errors=True)

def get_agent_response(session_id: str, user_message: str) -> dict:
    """
    Xử lý logic chính: lấy lịch sử chat, gọi agent, cập nhật lịch sử.
    """
    chat_history = get_chat_message_history(session_id)

    result = agent_executor.invoke({
        "input": user_message,
        "chat_history": chat_history.messages,
    })

    chat_history.add_user_message(user_message)
    chat_history.add_ai_message(result["output"])
    
    return {"response": result["output"]}
