from langchain_core.tools import tool
from pydantic import BaseModel, Field

from utils.markdown import to_markdown

class MarkdownInput(BaseModel):
    data: str = Field(description="The full content to convert into markdown format.")

@tool("convert_to_markdown", args_schema=MarkdownInput, return_direct=True)
def markdown_writer(data: str) -> str:
    """
    Converts plain text into a well-formatted markdown document.
    Use this tool **only after gathering all needed information** (e.g. via web search).
    """

    if not data.strip():
        return "Error: No data provided to convert. Please pass the missing text in the 'data' parameter to convert."

    output_text = to_markdown(data)

    return f"Markdown document created successfully\n {output_text}"