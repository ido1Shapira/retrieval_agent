from typing import Any

from langchain_core.tools import BaseTool
from langchain_experimental.tools import PythonAstREPLTool
from pydantic.v1 import BaseModel


class RetrieverInputs(BaseModel):
    input: dict[str, str]


class RetrieverTool(BaseTool):
    name = "retriever_tool"
    description = """
        Suitable tool to execute only valid python code for retrieving data from tables and other sources. 
        It accepts a single input in the following JSON format:
        {
            "code": "The Python code to execute"
        }
        Upon receiving the input, the tool attempts to execute the provided Python code. 
        If the execution is successful, it returns the result in the following format:
        Observation: $PYTHON_CODE_OUTPUT. 
        In case of an error, the tool will return the error message in the following format:
        Observation: $ERROR_NAME: $ERROR_MESSAGE. 
        Use the error name and error message to fix your python code. You may consider for split the python code into smaller pieces. 
        
        This tool is particularly useful for dynamic data retrieval and processing using Python code.
        Always end the Python code with print command in order to review the results."""
    args_schema = RetrieverInputs
    python_tool = PythonAstREPLTool()

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        result = self.python_tool.invoke(kwargs['code'])
        return f"Observation: {result}."
