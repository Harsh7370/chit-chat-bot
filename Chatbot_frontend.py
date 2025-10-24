import streamlit as st
from backend import get_response  # Import the function from your backend file

# --- Page Configuration ---
st.set_page_config(
    page_title="ChitChat",
    page_icon="💬",
    layout="centered"
)

# --- Sidebar for Model Selection ---
with st.sidebar:
    st.header("Model Selection")
    
    # List of models you have downloaded
    model_options = ["llama2", "mistral", "llama3:8b", "codellama", "llama3:latest"]
    
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = model_options[0] # Default

    # Create the selectbox
    selected_model = st.selectbox(
        "Choose a model:",
        model_options,
        key="selected_model" # Bind to session_state
    )
    st.caption("Run `ollama list` in your terminal to see your available models.")

# --- Page Title and Description ---
st.title("💬 ChitChat")
st.caption("A chat interface for local Ollama models.")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey there! How can I help you today?"}
    ]

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle User Input ---
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display bot response
    with st.chat_message("assistant"):
        
        # --- MODIFIED SECTION ---
        # Add a spinner to show "Thinking..." before the stream begins
        with st.spinner("Thinking..."):
            # Call the backend function, which returns a generator
            response_generator = get_response(prompt, model=st.session_state.selected_model)
            
            # Use st.write_stream to display the streaming response
            full_response = st.write_stream(response_generator)
        # --- END OF MODIFICATION ---
            
    # Add the *full* bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})