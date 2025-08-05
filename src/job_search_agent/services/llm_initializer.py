from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from langchain_community.agent_toolkits import FileManagementToolkit

import os


def init_agent_executor_from_config(config, memory, system_prompt):

    # define tools available for the llm ai agent
    search = TavilySearch(max_results=1) 
    filetools = FileManagementToolkit(root_dir=os.getcwd(), selected_tools=["write_file"]).get_tools()

    file_write_tool= filetools[0]

    tools = [search, file_write_tool] # Saving every tool in a list for agent reference

    model = init_chat_model(config.llm_model, model_provider=config.model_provider, api_key=config.croq_api_key)

    return create_react_agent(
    model,
    tools,
    checkpointer=memory,
    max_iterations=3,
    prompt= system_prompt)
