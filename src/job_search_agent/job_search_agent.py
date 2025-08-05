from config import Config
from services.llm_initializer import init_agent_executor_from_config
from services.agent_interface import call_llm_agent_no_retry, call_llm_agent_with_retry
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from prompts.prompts import filetool_agent_prompt


# load configuration
config = Config()
memory = MemorySaver()
memoryConfig = {"configurable": {"thread_id": "abc123"}}

system_prompt = ChatPromptTemplate([
    ("system", 
     filetool_agent_prompt),
    ("user", "{messages}")
    ]
)

# creaet executor for the ai agent
agent_executor = init_agent_executor_from_config(config=config, memory=memory, system_prompt=system_prompt)
call_llm_agent = call_llm_agent_with_retry if config.llm_agent_retry_enabled else call_llm_agent_no_retry

# define query to send to the agent
query = "Create a file with a text that consists of 50 words."
input_message = {"role": "user", "content": query}

# invoke the agent
call_llm_agent(agent_executor, input_message, memoryConfig, "values")
