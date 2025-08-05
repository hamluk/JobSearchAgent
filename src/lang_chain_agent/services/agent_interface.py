import time
from groq import RateLimitError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

retryable_errors = (RateLimitError, TimeoutError, Exception)

def _call_llm_agent_core(agent_executor, input_message, memoryConfig, streamMode, streamDelay=2):
    for step in agent_executor.stream({"messages": [input_message]}, memoryConfig, stream_mode=streamMode):
        step["messages"][-1].pretty_print()
        time.sleep(streamDelay)

@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=2, max=5),
    retry=retry_if_exception_type(retryable_errors)
)
def call_llm_agent_with_retry(*args, **kwargs):
    return _call_llm_agent_core(*args, **kwargs)

def call_llm_agent_no_retry(*args, **kwargs):
    return _call_llm_agent_core(*args, **kwargs)
