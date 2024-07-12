import os
from typing import Any

from langchain_core.tools import BaseTool

from src.utils import project_root_path


class SchemaDetectorTool(BaseTool):
    name = "schema_detector_tool"
    description = """
        Useful tool when you need help to determine the schema of your data based on a given query. It is
        particularly useful when you need to understand the structure of your data, such as the fields and data types.

        It accepts one input: user_input.

        This tool will return the schema of the data or in case it does not figure out the schema it would return that it had failed.
    """
    project_root_path: str = None

    def __init__(self, project_root_path: str):
        super().__init__()
        self.project_root_path = project_root_path

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        query: str = args[0]
        if 'student' in query:
            schema_path = os.path.join(self.project_root_path, 'data/students_schema.json')
            with open(schema_path, 'r') as file:
                return file.read()
        else:
            return "Observation: The tool failed to figure out the schema."
