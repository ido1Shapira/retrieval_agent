from typing import Any, Dict

import streamlit as st

from src.ui.enums.character import Character
from src.ui.enums.statis_strings import StaticStrings
from src.ui.interaction_chat import AInteractionChat


class StreamlitChat(AInteractionChat):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        st.title(StaticStrings.TITLE)
        st.header(StaticStrings.AGENT_DESCRIPTION, divider='rainbow')

        if "messages" not in st.session_state:
            st.session_state.messages = []

    def run(self):
        for message in st.session_state.messages:
            with st.chat_message(Character.user):
                st.markdown(message[0])
            with st.chat_message(Character.assistant):
                st.markdown(message[1])

        if user_question := st.chat_input(StaticStrings.USER_INPUT_PLACEHOLDER):
            with st.chat_message(Character.user):
                st.markdown(user_question)

        if user_question is not None and user_question != "":
            with st.chat_message(Character.assistant):
                with st.spinner(text=StaticStrings.IN_PROGRESS):
                    response = self.get_agent_response(user_question)
                    st.write(response)

            st.session_state.messages.append((user_question, response))
