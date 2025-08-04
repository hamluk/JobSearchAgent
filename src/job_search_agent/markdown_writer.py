from langchain_core.tools import tool

@tool
def markdown_writer(**kwargs: str):
    """
    Function to create a markdown document.
    This function is a placeholder and should be implemented with actual logic.
    """

    data_lines = []
    
    for key, value in kwargs.items():
        data_lines.append(f"{key}: {value}")


    output_text = "\n".join(data_lines)

    print(output_text)

    return "Markdown document created successfully."