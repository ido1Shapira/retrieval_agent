import os
from typing import Dict, Any, List, NamedTuple

from src.agent.agent import get_agent, Agent
from src.utils import read_config


class CommonAgentTest(NamedTuple):
    Q2A: List[Dict[str, Any]]
    base_path: str = 'C:/Users/Ido/Desktop/Projects/schema_agent'
    config: Dict[str, Any] = read_config(os.path.join(base_path, 'config.ini'))
    agent: Agent = get_agent(config)

    def test_query_agent(self, assert_function=None):
        if not assert_function or not self.Q2A:
            return

        for example in self.Q2A:
            response = self.agent.run(user_input=example['input'])
            assert_function(example['condition'](example['answer'], response),
                            msg=f"expected: {example['answer']} be in agent response but response is: {response}")
