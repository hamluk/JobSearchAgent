from dotenv import load_dotenv
from langchain_tavily import TavilySearch
import os

load_dotenv()

langsmith_tracing = os.getenv("LANGSMITH_TRACING")
langsmih_api_key = os.getenv("LANGSMITH_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

search = TavilySearch(max_results=2)
search_results = search.invoke("Software Engineer remote jobs in Australia")
print(search_results)

tools = [search] # Saving every tool in a list for later reference