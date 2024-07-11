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

# Setting up the api key
load_dotenv()
API_KEY: str | None = os.environ.get('GOOGLE_API_KEY', None)


class AgentInput(BaseModel):
    input: str
    chat_history: List[BaseMessage]


class Agent:
    def __init__(self,
                 temperature: float = 0.5,
                 model_name: str = 'gemini-1.5-flash'):
        llm: BaseChatModel = ChatGoogleGenerativeAI(temperature=temperature,
                                                    google_api_key=API_KEY,
                                                    model=model_name)

        tools: List[BaseTool] = [RetrieverTool(), SchemaDetectorTool()]
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
