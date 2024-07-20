import unittest
from typing import List, Dict, Any

from tests.test_agent import CommonAgentTest


class TestOneDataTypeQueries(unittest.TestCase, CommonAgentTest):
    Q2A: List[Dict[str, Any]] = [
        {
            "input": "how many students got higher than 90 in Mathematics?",
            "answer": 2,
            "condition": lambda expected, output: str(expected) in output
        },
        {
            "input": "who are the only students got higher than 90 in Mathematics?",
            "answer": ['John Doe', 'Jane Smith'],
            "condition": lambda expected, output: all(name in output for name in expected)
        },
        {
            "input": "what is the average age of the students who got under 60 in Physics?",
            "answer": 22,
            "condition": lambda expected, output: str(expected) in output
        }
    ]

    def test(self):
        return self.test_query_agent(assert_function=self.assertTrue)


if __name__ == '__main__':
    unittest.main()
