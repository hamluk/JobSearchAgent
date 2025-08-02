from config import Config
from langchain.chat_models import init_chat_model
from web_search_agent import WebSearchTool

config = Config()

search = WebSearchTool(max_results=1)
tools = [search] # Saving every tool in a list for later reference

model = init_chat_model(config.llm_model, model_provider=config.model_provider, api_key=config.croq_api_key)
model_with_tools = model.bind_tools(tools)

response = model_with_tools.invoke([{"role": "user", "content": "What remote jobs for Software Engineers in Australia are available?"}])

print(f"Mesage content: {response.text()}\n")
print(f"Tool calls: {response.tool_calls}")
