import os
import unittest
from typing import Dict, Any

from src.agent.agent import get_agent
from src.utils import read_config


class AgentTestCase(unittest.TestCase):
    base_path = 'C:/Users/Ido/Desktop/Projects/schema_agent'
    config: Dict[str, Any] = read_config(os.path.join(base_path, 'config.ini'))

    Q2A = [
        {
            "input": "how many students got 'A' in Mathematics?",
            "answer": "2",
            "condition": lambda expected, output: expected in output
        },
        {
            "input": "who are the only students that got 'A' in Mathematics?",
            "answer": ['John Doe', 'Jane Smith'],
            "condition": lambda expected, output: all(name in expected for name in expected)
        }
    ]

    agent = get_agent(config)

    def test_agent(self):
        for example in self.Q2A:
            response = self.agent.run(user_input=example['input'])
            self.assertTrue(example['condition'](example['answer'], response))


if __name__ == '__main__':
    unittest.main()
