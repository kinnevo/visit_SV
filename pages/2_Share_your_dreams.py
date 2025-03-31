import streamlit as st
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
import os
from database import init_db, save_conversation, get_conversation, get_user_sessions
from typing import List, Optional
import uuid

# The rest of your existing functions...
def run_flow(message: str, agent_name: str = "User_1", history: Optional[List[dict]] = None) -> dict:
    """
    Run the LangFlow with the given message and conversation history.
    
    Args:
        message: The current user message
        agent_name: The name of the user to use
        history: Optional list of previous conversation messages
    
    Returns:
        The response from LangFlow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT}"
    
    # Include conversation history if available
    if history and len(history) > 0:
        # Format history in the way LangFlow expects it
        formatted_history = json.dumps(history)
        
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
            "conversation_history": formatted_history,
            "user": agent_name,  # Pass the user name to LangFlow
            "session_id": agent_name
        }
    else:
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
            "user": agent_name,  # Pass the user name to LangFlow
            "session_id": agent_name
        }

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()
       
        return response_data
    except Exception as e:
        raise e

def add_to_history(role: str, content: str, user: Optional[str] = None):
    """Add a message to the conversation history and save to database."""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user
    }
    
    st.session_state.conversation_history.append(message)
    
    # Save updated conversation to database
    username = st.session_state.get('username')
    if not username:
        st.error("User not authenticated")
        return
    session_id = st.session_state.get('session_id', str(uuid.uuid4()))
    save_conversation(username, session_id, st.session_state.conversation_history)

def display_conversation():
    """Display the conversation history in the Streamlit UI."""
    # Create scrollable container
    scroll_container = st.container()
    
    # Wrap the messages in an expander to create scrollable area
    with scroll_container:
        st.markdown("""
            <style>
                .stMarkdown {
                    max-height: 400px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    padding: 10px;
                    border-radius: 5px;
                }
            </style>
        """, unsafe_allow_html=True)
        
        chat_container = st.empty()
        chat_content = ""
        
        # Build message content
        for message in st.session_state.conversation_history:
            if message["role"] == "user":
                chat_content += f"<div style='color: orange'><b>You</b>: {message['content']}</div><br>"
            else:
                chat_content += f"<div><b>Assistant:</b> {message['content']}</div><br>"
        
        # Display all messages in the container
        chat_container.markdown(chat_content, unsafe_allow_html=True)

  
    # Apply styling based on status
    def color_status(val):
        if val == "Active":
            return "background-color: #FFEB3B"  # Yellow
        elif val == "Completed":
            return "background-color: #4CAF50"  # Green
        elif val == "Failed":
            return "background-color: #F44336"  # Red
        else:
            return ""
    
    # Apply styling based on full exploration
    def color_exploration(val):
        if val == "Yes":
            return "background-color: #4CAF50"  # Green
        else:
            return ""



# Load environment variables
load_dotenv()

# Initialize database
init_db()

# LangFlow connection settings
BASE_API_URL = os.environ.get("BASE_API_URL")
FLOW_ID = os.environ.get("FLOW_ID")
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")
ENDPOINT = os.environ.get("ENDPOINT")  # The endpoint name of the flow

# Initialize session state for conversation memory and user tracking
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Load existing conversation from database
username = st.session_state.get('username')
if not username:
    st.error("User not authenticated")
    st.stop()
st.session_state.conversation_history = get_conversation(username, st.session_state.session_id)

st.set_page_config(
    page_title="Interactive Chat - Silicon Valley Visit Planner",
    page_icon="💬",
    layout="wide"
)

# Check authentication
if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page.")
    st.stop()

st.title("Interactive Visit Planning Chat 💬")

# Add session management UI
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("Current Session")
    st.write(f"Session ID: {st.session_state.session_id[:8]}...")

with col2:
    if st.button("New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.conversation_history = []
        st.rerun()

# Display user's previous sessions
st.subheader("Your Previous Sessions")
sessions = get_user_sessions(username)
if sessions:
    for session in sessions:
        st.write(f"Session: {session['session_id'][:8]}... (Last updated: {session['last_updated']})")
else:
    st.write("No previous sessions found.")

# User input
message = st.text_area("Message", placeholder="Ask something...")

if st.button("Send"):
    if not message.strip():
        st.error("Please enter a message")
    
    # Add user message to history
    add_to_history("user", message)
    
    try:
        with st.spinner(f"Running flow with ..."):
            # Pass the conversation history to LangFlow with the selected user
            response = run_flow(
                message,
                history=st.session_state.conversation_history[:-1]  # Exclude the current message
            )
            
            # Extract the response text
            response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            
            # Add bot response to history with user info
            add_to_history("assistant", response_text)
            
            # Save conversation to database with session ID
            save_conversation(username, st.session_state.session_id, st.session_state.conversation_history)
            
            # Force a rerun to update the display
            st.rerun()
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.error("Response: " + str(response) if 'response' in locals() else "No response received")

# Display conversation history
display_conversation()
