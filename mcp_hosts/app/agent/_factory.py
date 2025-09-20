"""
Agent factory module for the MCP Financial Agent.

This module creates and configures the LangChain agent that serves as the
core of the financial assistant. It sets up the agent with tools, prompts,
and memory management to handle financial queries.
"""
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.globals import set_llm_cache, get_llm_cache

import app.core.config as cfg
from app.llms import llm_client
from app.clients.tools_discovery import discover_tools
from app.prompts.loader import load_prompt
from app.cache import get_agent_cache
from app.memory import get_chat_message_history
from app.memory.retriever import MemoryRetriever

from ._custom import SemanticMemoryAndCacheAgentExecutor

# Load the system prompt that defines the agent's behavior
SYSTEM_PROMPT = load_prompt(cfg.SYSTEM_PROMPT_ID, cfg.PROMPT_FILE)

# Define the prompt template that structures the conversation
# This template includes system instructions, chat history, user input, and agent scratchpad
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name='retrieved_chat_history'),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name='agent_scratchpad')
])

# Initialize all available tools for the agent by discovering them from the registry
tools = discover_tools()

set_llm_cache(get_agent_cache())

# Create the agent using LangChain's tool calling agent
# This agent can understand when to use tools and how to use them properly
agent = create_tool_calling_agent(llm_client, tools, prompt)

# Create the agent executor which handles the agent's execution loop
# The executor manages the interaction between the agent, tools, and memory
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    stream_runnable=False
)

final_executor = SemanticMemoryAndCacheAgentExecutor(
    base_agent_exec=agent_executor,
    chat_history_getter=get_chat_message_history,
    memory_retriever=MemoryRetriever(top_k=4),
    agent_cache=get_agent_cache()
)

print(f'INFO: LLM Cache enables: {llm_client.cache}')

def get_agent_response(session_id: str, user_message: str) -> dict:
    """
    Process user messages through the financial agent and return responses.
    
    This function retrieves the chat history for the session, invokes the agent
    with the user's message, and updates the chat history with the interaction.
    
    Args:
        session_id (str): Unique identifier for the conversation session
        user_message (str): The user's input message
        
    Returns:
        dict: Contains the agent's response with the key "response"
    """
    result = final_executor.invoke(user_message, session_id)
    return {"response": result["output"]}