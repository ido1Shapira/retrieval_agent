import os
import unittest
from typing import Any, Dict, List

from src.agent.agent import get_agent, Agent
from src.utils import read_config


class TestMultiDataTypeQueries(unittest.TestCase):
    base_path: str = 'C:/Users/Ido/Desktop/Projects/schema_agent'
    config: Dict[str, Any] = read_config(os.path.join(base_path, 'config.ini'))
    agent: Agent = get_agent(config)

    Q2A: List[Dict[str, Any]] = [
        {
            "input": "what are the names of the parents that there children got 'A' in Mathematics?",
            "answer": ["Emily Brown", "Michael Johnson"],
            "condition": lambda expected, output: all(name in output for name in expected)
        },
        {
            "input": "what is the number of male parents that at least one of their children got 'C' in History?",
            "answer": 1,
            "condition": lambda expected, output: str(expected) in output
        }
    ]

    def test_query_agent(self):
        for example in self.Q2A:
            response = self.agent.run(user_input=example['input'])
            self.assertTrue(example['condition'](example['answer'], response),
                            msg=f"expected: {example['answer']} be in agent response but response is: {response}")


if __name__ == '__main__':
    unittest.main()
