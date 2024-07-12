import os
import unittest
from typing import List, Dict, Any

from src.agent.agent import get_agent, Agent
from src.utils import read_config


class TestOneDataTypeQueries(unittest.TestCase):
    base_path: str = 'C:/Users/Ido/Desktop/Projects/schema_agent'
    config: Dict[str, Any] = read_config(os.path.join(base_path, 'config.ini'))
    agent: Agent = get_agent(config)

    Q2A: List[Dict[str, Any]] = [
        {
            "input": "how many students got 'A' in Mathematics?",
            "answer": "2",
            "condition": lambda expected, output: expected in output
        },
        {
            "input": "who are the only students that got 'A' in Mathematics?",
            "answer": ['John Doe', 'Jane Smith'],
            "condition": lambda expected, output: all(name in output for name in expected)
        }
    ]

    def test_query_agent(self):
        for example in self.Q2A:
            response = self.agent.run(user_input=example['input'])
            self.assertTrue(example['condition'](example['answer'], response),
                            msg=f"expected: {example['answer']} be in agent response but response is: {response}")


if __name__ == '__main__':
    unittest.main()
