from langchain_core.chat_history import InMemoryChatMessageHistory

from utils.user_profile import (
    get_user_profile,
    update_user_profile
)



chat_sessions = {}



def get_chat_history(session_id):

    if session_id not in chat_sessions:

        chat_sessions[session_id] = (
            InMemoryChatMessageHistory()
        )

    return chat_sessions[session_id]