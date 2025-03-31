import streamlit as st
import requests
import json

"""
st.set_page_config(
    page_title="Interactive Chat - Silicon Valley Visit Planner",
    page_icon="💬",
    layout="wide"
)
"""

# Check authentication
if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page.")
    st.stop()

st.title("Interactive Visit Planning Chat 💬")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about planning your Silicon Valley visit..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Langflow
    try:
        # Replace with your Langflow API endpoint
        response = requests.post(
            "http://34.59.108.214:7860/api/v1/run/75b5f45c-e41d-4ba4-86a1-9539e3928056",
            json={
                "message": prompt,
                "history": st.session_state.messages
            }
        )
        response_data = response.json()
        assistant_message = response_data.get("response", "I apologize, but I'm having trouble connecting to the chat service.")
    except Exception as e:
        assistant_message = f"I apologize, but I'm having trouble connecting to the chat service. Error: {str(e)}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)

# Sidebar with chat controls
with st.sidebar:
    st.header("Chat Controls")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Chat stage selector
    st.subheader("Chat Stage")
    chat_stage = st.selectbox(
        "Select the stage you want to discuss:",
        ["Pre-Visit Planning", "During Visit", "Post-Visit Impact"]
    )
    
    # Tips based on selected stage
    st.subheader("Tips for " + chat_stage)
    if chat_stage == "Pre-Visit Planning":
        st.markdown("""
        - Research companies you want to visit
        - Plan your itinerary
        - Book accommodations early
        - Consider transportation options
        """)
    elif chat_stage == "During Visit":
        st.markdown("""
        - Keep track of your schedule
        - Network effectively
        - Document your experiences
        - Stay flexible with plans
        """)
    else:
        st.markdown("""
        - Follow up with contacts
        - Document learnings
        - Share experiences
        - Plan next steps
        """) 