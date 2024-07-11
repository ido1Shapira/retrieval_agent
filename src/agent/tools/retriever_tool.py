from typing import Any

from langchain_core.tools import BaseTool
from langchain_experimental.tools import PythonAstREPLTool
from pydantic.v1 import BaseModel


class RetrieverInputs(BaseModel):
    input: dict[str, str]


class RetrieverTool(BaseTool):
    name = "retriever_tool"
    description = """A tool that can retrieve data from a table by executing Python code and return the result.
        It accepts one input: input. The input must be in the following format:
        {
            "code": "The python code to execute"
        }
        This tool is useful for executing Python code and providing the result.
    """
    args_schema = RetrieverInputs

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        try:
            python_tool = PythonAstREPLTool()
            result = python_tool.invoke(kwargs['code'])
            return f"Observation: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
