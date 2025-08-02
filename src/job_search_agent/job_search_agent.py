from config import Config
from langchain.chat_models import init_chat_model
from web_search_agent import WebSearchTool

config = Config()

search = WebSearchTool(config)
tools = [search] # Saving every tool in a list for later reference

model = init_chat_model(config.llm_model, model_provider=config.model_provider, api_key=config.croq_api_key)

response = model.invoke([{"role": "user", "content": "Hi, what can you do for me?"}])
print(response.text())
