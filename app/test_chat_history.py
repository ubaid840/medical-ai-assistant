from database import initialize_database
from chat_history import create_session, save_message, get_messages

initialize_database()

session = create_session("Test Chat")

save_message(session, "user", "Hello AI")
save_message(session, "assistant", "Hello! How can I help you?")

messages = get_messages(session)

for msg in messages:
    print(msg["role"], ":", msg["message"])