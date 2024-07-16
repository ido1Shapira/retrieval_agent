import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.language_models import BaseLLM
from langchain_core.tools import BaseTool

from src.agent.llm_client import LLMClient
from src.agent.prompt import prompt
from src.agent.tools.retriever_tool import RetrieverTool
from src.agent.tools.schema_detector_tool import SchemaDetectorTool
from src.logger import get_logger

# Setting up the api key
load_dotenv()
API_KEY: str | None = os.environ.get('GOOGLE_API_KEY', None)


class Agent:
    def __init__(self,
                 model_name: str,
                 project_root_path: str,
                 api_key: str = API_KEY,
                 temperature: float = 0.5,
                 verbose: bool = True,
                 max_iterations: int = 10):
        llm: BaseLLM = LLMClient(temperature=temperature,
                                 api_key=api_key,
                                 model_name=model_name)

        tools: List[BaseTool] = [RetrieverTool(), SchemaDetectorTool(project_root_path)]
        agent = create_structured_chat_agent(llm, tools, prompt)

        self.agent_executor = AgentExecutor(agent=agent,
                                            tools=tools,
                                            verbose=verbose,
                                            handle_parsing_errors=True,
                                            max_iterations=max_iterations)
        self.logger = get_logger(__name__)

    def run(self, user_input: str) -> str:
        self.logger.info(f"Invoking agent with input: {user_input}")
        response = self.agent_executor.invoke({
            "input": user_input,
        })
        agent_output = response["output"]
        return agent_output


def get_agent(config) -> Agent:
    return Agent(model_name=config['Agent']['model_name'],
                 project_root_path=config['Application']['base_path'],
                 temperature=config['Agent']['temperature'],
                 verbose=config['Agent']['verbose'],
                 max_iterations=config['Agent']['max_iterations'])
