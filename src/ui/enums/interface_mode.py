from typing import Dict, Type

from src.ui.interaction_chat import AInteractionChat
from src.ui.streamlit_chat import StreamlitChat
from src.ui.terminal_chat import TerminalChat

mode_to_interface: Dict[str, Type[AInteractionChat]] = {
    'terminal': TerminalChat,
    'streamlit': StreamlitChat,
}
