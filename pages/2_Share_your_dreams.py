import streamlit as st
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
import os

# The rest of your existing functions...
def run_flow(message: str, agent_name: str = "User_1", history: list = None) -> dict:
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

def add_to_history(role: str, content: str, user: str = None):
    """Add a message to the conversation history."""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user
    }
    
    st.session_state.conversation_history.append(message)

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

# Continue with your existing code...
# LangFlow connection settings
BASE_API_URL = "http://34.59.108.214:7860/"
FLOW_ID = "75b5f45c-e41d-4ba4-86a1-9539e3928056"
APPLICATION_TOKEN = os.environ.get("OPENAI_API_KEY")
ENDPOINT = "75b5f45c-e41d-4ba4-86a1-9539e3928056"  # The endpoint name of the flow

# Initialize session state for conversation memory and user tracking
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []


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

# User input
message = st.text_area("Message", placeholder="Ask something...")

if st.button("Send"):
    if not message.strip():
        st.error("Please enter a message")
        # return ????
    
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
            
            # Force a rerun to update the display
            st.rerun()
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.error("Response: " + str(response) if 'response' in locals() else "No response received")
        

# Display conversation history
display_conversation()
