from abc import ABC, abstractmethod
from typing import Dict, Any

from src.agent.agent import get_agent


class AInteractionChat(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.agent = get_agent(config)

    def get_agent_response(self, user_input: str):
        return self.agent.run(user_input=user_input)

    @abstractmethod
    def run(self):
        raise NotImplementedError("Not implemented")
