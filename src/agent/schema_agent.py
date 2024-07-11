import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool
from langchain_experimental.tools import PythonAstREPLTool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from src.agent.prompt import prompt

# Setting up the api key
load_dotenv()
API_KEY: str | None = os.environ.get('GOOGLE_API_KEY', None)


class AgentInput(BaseModel):
    input: str
    chat_history: List[BaseMessage]


class SchemaAgent:
    def __init__(self,
                 temperature: float = 0.5,
                 model_name: str = 'gemini-1.5-flash'):
        llm: BaseChatModel = ChatGoogleGenerativeAI(temperature=temperature,
                                                    google_api_key=API_KEY,
                                                    model=model_name)

        tools: List[BaseTool] = [PythonAstREPLTool(), self.__get_schema_tool]
        agent = create_structured_chat_agent(llm, tools, prompt)

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        self.agent_executor = AgentExecutor(agent=agent,
                                            tools=tools,
                                            verbose=True,
                                            handle_parsing_errors=True,
                                            memory=self.memory,
                                            max_iterations=10)

    def run(self, user_input: str) -> str:
        chat_history = self.memory.buffer_as_messages
        response = self.agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history,
        })
        agent_output = response["output"]
        return agent_output

    @staticmethod
    @tool("schema_detector_tool")
    def __get_schema_tool(query: str) -> str:
        """
        Useful tool when you need help to determine the schema of your data based on a given query. It is
        particularly useful when you need to understand the structure of your data, such as the fields and data types.

        It accepts one input: user_input.

        This tool will return the schema of the data or in case it does not figure out the schema it would return that it had failed.
        """
        if 'student' in query:
            schema_path = os.path.join(os.getcwd(), 'data/students_schema.json')
            with open(schema_path, 'r') as file:
                return file.read()
        else:
            return "Observation: The tool failed to figure out the schema."
