from langchain_tavily import TavilySearch
import json

class WebSearchTool:
    def __init__(self, config):
        self.search = TavilySearch(max_results=2)
        self.config = config

    def searchWeb(self, query) -> str:
        search_results = None

        if self.config.runtime_env == "prod":
            search_results = self.search.invoke(query) 

        elif self.config.runtime_env == "dev":
            try:
                with open(self.config.web_search_test_data_file, "r") as file:
                    search_results = str(json.load(file))
            except FileNotFoundError:
                print("Test data file not found. Make sure to not set runtime_env to 'dev' or provide test data file")
                

        return search_results if search_results else "No results found!"