import os
from typing import Any, Dict

from src.agent.agent import Agent
from src.ui.interface import InteractionChat
from src.utils import read_config

config: Dict[str, Any] = read_config(os.path.join(os.getcwd(), 'config.ini'))


def main():
    if config['Application']['use_gui']:
        interface = InteractionChat()
        interface.on_user_input()
    else:
        agent = Agent(model_name=config['Agent']['model_name'],
                      temperature=config['Agent']['temperature'],
                      verbose=config['Agent']['verbose'],
                      max_iterations=config['Agent']['max_iterations'])
        user_input = "who are the only students that got 'A' in Mathematics?"
        response = agent.run(user_input=user_input)
        print(response)


if __name__ == "__main__":
    main()
