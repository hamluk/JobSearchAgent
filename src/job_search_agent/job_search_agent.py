from groq import RateLimitError
from langchain_tavily import TavilySearch
from config import Config
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from markdown_writer import markdown_writer

import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

retryable_errors = (RateLimitError, TimeoutError, Exception)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=5),
    retry=retry_if_exception_type(retryable_errors)
)
def run_agent_with_backoff(agent_executor, input_message, memoryConfig, streamMode, streamDelay=2):
    for step in agent_executor.stream({"messages": [input_message]}, memoryConfig, stream_mode=streamMode):
        step["messages"][-1].pretty_print()
        time.sleep(streamDelay)

config = Config()

memory = MemorySaver()
memoryConfig = {"configurable": {"thread_id": "abc123"}}

search = TavilySearch(max_results=1) 


tools = [search, markdown_writer] # Saving every tool in a list for agent reference

model = init_chat_model(config.llm_model, model_provider=config.model_provider, api_key=config.croq_api_key)

agent_executor = create_react_agent(model, tools, checkpointer=memory, max_iterations=3)

query = "Create a markdown document with the current weather in San Francisco."

input_message = {"role": "user", "content": query}
run_agent_with_backoff(agent_executor, input_message, memoryConfig, "values")
