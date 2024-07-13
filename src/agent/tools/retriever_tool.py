from typing import Any

from langchain_core.tools import BaseTool
from langchain_experimental.tools import PythonAstREPLTool
from pydantic.v1 import BaseModel


class RetrieverInputs(BaseModel):
    input: dict[str, str]


class RetrieverTool(BaseTool):
    name = "retriever_tool"
    description = """
        A versatile tool designed to execute Python code for retrieving data from tables and other sources. 
        It accepts a single input in the following JSON format:
        {
            "code": "The Python code to execute"
        }
        Upon receiving the input, the tool attempts to execute the provided Python code. 
        If the execution is successful, it returns the result. 
        In case of an error, the tool will return the error message.
        This tool is particularly useful for dynamic data retrieval and processing using Python code.
    """
    args_schema = RetrieverInputs

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        try:
            python_tool = PythonAstREPLTool()
            result = python_tool.invoke(kwargs['code'])
            return f"Observation: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
