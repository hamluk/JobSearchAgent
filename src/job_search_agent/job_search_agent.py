from langchain_tavily import TavilySearch
from config import Config
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

config = Config()

memory = MemorySaver()
memoryConfig = {"configurable": {"thread_id": "abc123"}}

search = TavilySearch(max_results=1) 
tools = [search] # Saving every tool in a list for later reference

model = init_chat_model(config.llm_model, model_provider=config.model_provider, api_key=config.croq_api_key)

agent_executor = create_react_agent(model, tools, checkpointer=memory, max_iterations=2)

query = "What remote job applications are available for a Software Engineer in Australia?"

input_message = {"role": "user", "content": query}
for step in agent_executor.stream({"messages": [input_message]}, memoryConfig, stream_mode="values"):
    step["messages"][-1].pretty_print()
