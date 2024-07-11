import streamlit as st

from src.agent.schema_agent import SchemaAgent
from src.ui.enums.character import Character
from src.ui.enums.statis_strings import StaticStrings


class InteractionChat:
    def __init__(self):
        st.title(StaticStrings.TITLE)
        st.header(StaticStrings.AGENT_DESCRIPTION, divider='rainbow')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        self.agent = SchemaAgent()

    def on_user_input(self):
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
                    response = self.agent.run(user_input=user_question)
                    st.write(response)

            st.session_state.messages.append((user_question, response))
