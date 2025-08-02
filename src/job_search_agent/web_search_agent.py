from langchain_tavily import TavilySearch
import json

class WebSearchTool(TavilySearch):
    name: str = "web_search_tool"
    description: str = (
        "A search engine optimized for comprehensive, accurate, and trusted results. "
        "Useful for when you need to answer questions about current events. "
        "It not only retrieves URLs and snippets, but offers advanced search depths, "
        "domain management, time range filters, and image search, this tool delivers "
        "real-time, accurate, and citation-backed results."
        "Input should be a search query."
        "A Wrapper for the Tavily Search Tool to perform web searches. "
        "Its difference is that it reads test data from a file in dev mode instead of making a web search. "
    )

    def invoke(self, config, query):
        search_results = None

        if config.runtime_env == "prod":
            search_results = super().invoke(query) 

        elif config.runtime_env == "dev":
            try:
                with open(config.web_search_test_data_file, "r") as file:
                    search_results = str(json.load(file))
            except FileNotFoundError as e:
                print(e)
                

        return search_results if search_results else "No results found!"