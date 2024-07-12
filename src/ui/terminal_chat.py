from src.logger import get_logger
from src.ui.enums.statis_strings import StaticStrings
from src.ui.interaction_chat import AInteractionChat


class TerminalChat(AInteractionChat):
    logger = get_logger(__name__)

    def run(self):
        while user_input := input(f'{StaticStrings.USER_INPUT_PLACEHOLDER}:\n'):
            if (user_input.lower() == 'exit' or
                    user_input.lower() == 'q'):
                break
            if user_input is None or user_input == '':
                continue

            response = self.get_agent_response(user_input)
            self.logger.info(response)
