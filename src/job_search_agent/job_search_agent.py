from config import Config
from job_search_agent.web_search_agent import WebSearchTool

config = Config()

print(config.runtime_env)

search = WebSearchTool(config)
print(search.searchWeb("Software Engineer remote jobs in Australia"))

tools = [search] # Saving every tool in a list for later reference