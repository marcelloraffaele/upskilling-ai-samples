import streamlit as st
import ai_util as aiutil

def send_message(prompt):
    print("System message:", st.session_state.systemMessage, ", User input:", prompt, ", Model:", st.session_state.model_choice)
    st.session_state.chatMessages.append({"role": "user", "content": prompt})
    response = call(st.session_state.systemMessage, st.session_state.chatMessages, st.session_state.model_choice)
    st.session_state.chatMessages.append({"role": "assistant", "content": response})

    for message in st.session_state.chatMessages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def call(sm, cm, model_choice):
    messageList = []
    messageList.append({"role": "system", "content": sm})
    for m in cm:
        messageList.append(m)
    
    # Use the selected model type
    if model_choice == "DeepSeek":
        model_type = aiutil.ModelType.DEEPSEEK
    elif model_choice == "Phi":
        model_type = aiutil.ModelType.PHI
    else:
        model_type = aiutil.ModelType.OPENAI
    res = aiutil.completion(messageList, model_type)
    return res

# Set up the Streamlit app
st.title("AI Chat")

# Initialize session state for messages
if "systemMessage" not in st.session_state:
    st.session_state.systemMessage = "You are a helpful assistant"

if "chatMessages" not in st.session_state:
    st.session_state.chatMessages = []

if "model_choice" not in st.session_state:
    st.session_state.model_choice = "OpenAI"

# UI Controls sidebar
with st.sidebar:
    # Model selection
    model_choice = st.selectbox(
        "Select AI Model",
        ["OpenAI", "DeepSeek", "Phi"],
        index=0,  # Set OpenAI (index 0) as default
        key="model_select"
    )
    if model_choice != st.session_state.model_choice:
        st.session_state.model_choice = model_choice

    # Create text area with a different key and update systemMessage when changed
    system_message_input = st.text_area("System message", value=st.session_state.systemMessage, key="system_message_input")
    if system_message_input != st.session_state.systemMessage:
        st.session_state.systemMessage = system_message_input

    # Reset button for clearing conversation
    if st.button("Reset Conversation"):
        st.session_state.chatMessages = []
        st.rerun()  # Rerun the app to refresh the UI

if prompt := st.chat_input():
    send_message(prompt)