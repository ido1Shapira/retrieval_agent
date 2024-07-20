import unittest
from typing import List, Dict, Any

from tests.test_agent import CommonAgentTest


class TestOneDataTypeQueries(unittest.TestCase, CommonAgentTest):
    Q2A: List[Dict[str, Any]] = [
        {
            "input": "who is the best student?",
            "answer": "Hank Miller",
            "condition": lambda expected, output: str(expected) in output
        },
        {
            "input": "who are the parents of students that have difficulty with Chemistry?",
            "answer": ['Emily Brown', 'Jane Smith'],
            "condition": lambda expected, output: all(name in output for name in expected)
        }
    ]

    def test(self):
        return self.test_query_agent(assert_function=self.assertTrue)


if __name__ == '__main__':
    unittest.main()
