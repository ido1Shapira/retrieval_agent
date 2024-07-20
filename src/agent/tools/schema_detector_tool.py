import os
from typing import Any, Dict

from langchain_core.tools import BaseTool
from pydantic import BaseModel


class Pattern(BaseModel):
    match_condition: bool
    schema_name: str


class SchemaDetectorTool(BaseTool):
    name = "schema_detector_tool"
    description = """
        Useful tool when you need help to determine the schema of your data based on a given query. It is
        particularly useful when you need to understand the structure of your data, such as the fields and data types.

        It accepts one input: user_input.

        This tool will returns the schema of the data or in case it does not figure out the schema it would return that it had failed.
    """
    project_root_path: str = None
    output_template = """Tool found {schemas_number} schemas:
    {schemas}
    """

    def __init__(self, project_root_path: str):
        super().__init__()
        self.project_root_path = project_root_path

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        query: str = args[0]
        all_patterns: Dict[str, Pattern] = {
            'students_schema': Pattern(
                match_condition='student' in query or 'grade' in query,
                schema_name='students_schema.json'
            ),
            'parents_students_schema': Pattern(
                match_condition='parent' in query,
                schema_name='parents_students_schema.json'
            ),
            'lessons_schema': Pattern(
                match_condition='lesson' in query,
                schema_name='lessons_schema.json'
            )
        }
        match_counter = 0
        match_schemas = []
        for pattern in all_patterns:
            if all_patterns[pattern].match_condition:
                match_counter += 1
                match_schemas.append(f"{match_counter})\n{self.__get_schema(all_patterns[pattern].schema_name)}")

        if match_counter > 0:
            return self.output_template.format(schemas_number=match_counter, schemas="\n\n".join(match_schemas))
        else:
            return "Observation: The tool failed to figure out the schema."

    def __get_schema(self, path):
        schema_path = os.path.join(self.project_root_path, 'data/schemas', path)
        with open(schema_path, 'r') as file:
            return file.read()
