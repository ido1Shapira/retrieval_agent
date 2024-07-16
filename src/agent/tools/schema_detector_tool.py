import os
from typing import Any

from langchain_core.tools import BaseTool


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
    {schema}
    """

    def __init__(self, project_root_path: str):
        super().__init__()
        self.project_root_path = project_root_path

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        query: str = args[0]
        match_students_schema = 'student' in query or 'grade' in query
        match_parents_schema = 'parent' in query
        if match_students_schema and match_parents_schema:
            two_schemas = f"""1) {self.__get_schema('data/schemas/students_schema.json')}\n\n 2) {self.__get_schema('data/schemas/parents_students_schema.json')}"""
            return self.output_template.format(schemas_number=2, schema=two_schemas)
        elif match_students_schema:
            return self.output_template.format(schemas_number=1,
                                               schema=self.__get_schema('data/schemas/students_schema.json'))
        elif match_parents_schema:
            return self.output_template.format(schemas_number=1,
                                               schema=self.__get_schema('data/schemas/parents_students_schema.json'))
        else:
            return "Observation: The tool failed to figure out the schema."

    def __get_schema(self, path):
        schema_path = os.path.join(self.project_root_path, path)
        with open(schema_path, 'r') as file:
            return file.read()
