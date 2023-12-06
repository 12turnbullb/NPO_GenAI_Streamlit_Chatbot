import streamlit as st

def chat_history():
    # This function simulates a chat history. You can replace it with your own data.
    history = [
        {'sender': 'User', 'message': 'Hi there!'},
        {'sender': 'Bot', 'message': 'Hello! How can I help you today?'},
        {'sender': 'User', 'message': 'I have a question about Streamlit.'},
        {'sender': 'Bot', 'message': 'Sure, go ahead and ask your question.'},
    ]
    return history

def main():
    st.title("Chat Conversation with History")

    # Get chat history
    history = chat_history()

    # Display chat history
    for entry in history:
        if entry['sender'] == 'User':
            st.text_input("You:", entry['message'], key=entry['message'])
        else:
            st.text_area("Bot:", entry['message'], key=entry['message'], height=80)

    # Input box for the user to send new messages
    user_message = st.text_input("Type your message here:", "")

    # Button to send the user's message
    if st.button("Send"):
        if user_message:
            # Add the user's message to the chat history
            history.append({'sender': 'User', 'message': user_message})

            # Simulate a bot response (replace this with actual bot logic)
            bot_response = "I'm a bot. I don't have a real response, but I can pretend!"
            history.append({'sender': 'Bot', 'message': bot_response})

    # Save the updated chat history
    st.session_state.chat_history = history

if __name__ == "__main__":
    main()
