import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain.pydantic_v1 import BaseModel
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agent.prompt import prompt
from src.agent.tools.retriever_tool import RetrieverTool
from src.agent.tools.schema_detector_tool import SchemaDetectorTool
from src.logger import get_logger

# Setting up the api key
load_dotenv()
API_KEY: str | None = os.environ.get('GOOGLE_API_KEY', None)


class AgentInput(BaseModel):
    input: str
    chat_history: List[BaseMessage]


class Agent:
    def __init__(self,
                 model_name: str,
                 project_root_path: str,
                 api_key: str = API_KEY,
                 temperature: float = 0.5,
                 verbose: bool = True,
                 max_iterations: int = 10):
        llm: BaseChatModel = ChatGoogleGenerativeAI(temperature=temperature,
                                                    google_api_key=api_key,
                                                    model=model_name)

        tools: List[BaseTool] = [RetrieverTool(), SchemaDetectorTool(project_root_path)]
        agent = create_structured_chat_agent(llm, tools, prompt)

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        self.agent_executor = AgentExecutor(agent=agent,
                                            tools=tools,
                                            verbose=verbose,
                                            handle_parsing_errors=True,
                                            memory=self.memory,
                                            max_iterations=max_iterations)
        self.logger = get_logger(__name__)

    def run(self, user_input: str) -> str:
        chat_history = self.memory.buffer_as_messages
        self.logger.info(f"Chat history: {chat_history}")
        self.logger.info(f"Invoking agent with input: {user_input}")
        response = self.agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history,
        })
        agent_output = response["output"]
        return agent_output


def get_agent(config) -> Agent:
    return Agent(model_name=config['Agent']['model_name'],
                 project_root_path=config['Application']['base_path'],
                 temperature=config['Agent']['temperature'],
                 verbose=config['Agent']['verbose'],
                 max_iterations=config['Agent']['max_iterations'])
