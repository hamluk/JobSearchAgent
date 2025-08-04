from groq import RateLimitError
from langchain_tavily import TavilySearch
from config import Config
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
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

system_prompt = ChatPromptTemplate([
    ("system", 
     """
        You are an intelligent assistant that helps users research online topics and produce structured markdown summaries.

        Your workflow is:
        1. Use `tavily_search` to gather factual information.
        3. Pass the information to `convert_to_markdown` by using the 'data' argument.

        DO NOT call `convert_to_markdown` before relevant information has been found.
        DO NOT fabricate answers — rely on search results.
        Only call one tool at a time.

        When the user asks a question, follow this pattern:
        - Think about what needs to be searched.
        - Use the search tool with a specific query.
        - Send that search result to `convert_to_markdown`.

        Be concise, accurate, and markdown-ready in your formatting.
    """),
    ("user", "{messages}")
    ]
)

agent_executor = create_react_agent(
    model,
    tools,
    checkpointer=memory,
    max_iterations=3,
    prompt= system_prompt)

query = "Create a markdown document with the current weather in San Francisco."

input_message = {"role": "user", "content": query}
run_agent_with_backoff(agent_executor, input_message, memoryConfig, "values")
