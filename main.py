import os

from dotenv import load_dotenv

from src.agent.schema_agent import SchemaAgent
from src.ui.interface import InteractionChat


def main(use_gui: bool):
    if use_gui:
        interface = InteractionChat()
        interface.on_user_input()
    else:
        agent = SchemaAgent()
        user_input = "how many students got 'A' in Mathematics?"

        response = agent.run(user_input=user_input)
        print(response)


if __name__ == "__main__":
    load_dotenv()
    USE_GUI: bool = eval(os.environ.get('USE_GUI', False))
    main(USE_GUI)
