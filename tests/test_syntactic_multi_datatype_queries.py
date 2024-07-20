import unittest
from typing import Any, Dict, List

from tests.test_agent import CommonAgentTest


class TestMultiDataTypeQueries(unittest.TestCase, CommonAgentTest):
    Q2A: List[Dict[str, Any]] = [
        {
            "input": "what are the names of the parents that there children got higher than 90 in Mathematics?",
            "answer": ["Emily Brown", "Michael Johnson"],
            "condition": lambda expected, output: all(name in output for name in expected)
        },
        {
            "input": "what is the number of male parents that at least one of their children got under than 60 in Physics?",
            "answer": 1,
            "condition": lambda expected, output: str(expected) in output
        }
    ]

    def test(self):
        return self.test_query_agent(assert_function=self.assertTrue)


if __name__ == '__main__':
    unittest.main()
