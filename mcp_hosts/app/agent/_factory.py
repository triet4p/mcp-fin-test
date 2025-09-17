"""
Agent factory module for the MCP Financial Agent.

This module creates and configures the LangChain agent that serves as the
core of the financial assistant. It sets up the agent with tools, prompts,
and memory management to handle financial queries.
"""
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import app.core.config as cfg
from app.llms import llm_client
from app.clients.tools_discovery import discover_tools
from app.prompts.loader import load_prompt
from app.memory import get_chat_message_history

# Load the system prompt that defines the agent's behavior
SYSTEM_PROMPT = load_prompt(cfg.SYSTEM_PROMPT_ID, cfg.PROMPT_FILE)

# Define the prompt template that structures the conversation
# This template includes system instructions, chat history, user input, and agent scratchpad
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name='chat_history'),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name='agent_scratchpad')
])

# Initialize all available tools for the agent by discovering them from the registry
tools = discover_tools()

# Create the agent using LangChain's tool calling agent
# This agent can understand when to use tools and how to use them properly
agent = create_tool_calling_agent(llm_client, tools, prompt)

# Create the agent executor which handles the agent's execution loop
# The executor manages the interaction between the agent, tools, and memory
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

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
    # Retrieve or create chat history for this session
    chat_history = get_chat_message_history(session_id)

    # Invoke the agent with the user's message and chat history
    result = agent_executor.invoke({
        "input": user_message,
        "chat_history": chat_history.messages,
    })

    # Update chat history with the new interaction
    chat_history.add_user_message(user_message)
    chat_history.add_ai_message(result["output"])
    
    return {"response": result["output"]}
