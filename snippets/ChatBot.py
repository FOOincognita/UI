import streamlit as st

# Initialize chat history if it doesn't exist
if 'history' not in st.session_state:
    st.session_state['history'] = []

def send_message():
    user_input = st.session_state.user_input  # Get current user input
    if user_input:  # If there's an input
        # Add user input to history
        st.session_state.history.append(f"You: {user_input}")
        # Here, insert the logic to get the chatbot's response. Replace placeholder below.
        chatbot_response = "Chatbot response..."  # This should be your actual chatbot response
        st.session_state.history.append(f"Chatbot: {chatbot_response}")
        # Clear the input box
        st.session_state.user_input = ""

# Chat interface
st.title("Simple AI Chatbot")
# Text input box. Automatically sends the message when the Enter key is pressed.
user_input = st.text_input("Your question", key="user_input", on_change=send_message)

# Display the chat history
for idx, message in enumerate(st.session_state.history):
    st.text_area("", value=message, height=75, key=f"msg_{idx}")
