import streamlit as st
import sqlite3
import json
from datetime import datetime

def get_conversation_by_number(conv_number):
    """Retrieve a conversation by its number from the database."""
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    
    # Get all conversations ordered by last_updated
    c.execute('SELECT user_id, conversation_data, last_updated FROM conversations ORDER BY last_updated DESC')
    results = c.fetchall()
    
    conn.close()
    
    if conv_number <= len(results):
        user_id, conversation_data, last_updated = results[conv_number - 1]
        try:
            messages = json.loads(conversation_data)
            return {
                'user_id': user_id,
                'messages': messages,
                'last_updated': last_updated
            }
        except json.JSONDecodeError:
            return None
    return None

def get_conversation(user_id):
    """Retrieve a specific conversation from the database."""
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    
    # Admin can view any conversation
    c.execute('SELECT conversation_data, last_updated FROM conversations WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    
    conn.close()
    
    if result:
        conversation_data, last_updated = result
        try:
            messages = json.loads(conversation_data)
            return {
                'user_id': user_id,
                'messages': messages,
                'last_updated': last_updated
            }
        except json.JSONDecodeError:
            return None
    return None

st.set_page_config(
    page_title="View Conversation",
    page_icon="💬",
    layout="wide"
)

# Check if user is authenticated and is jazo
if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page.")
    st.stop()

if st.session_state.get('username') != 'jazo':
    st.error("Access denied. This page is only available for administrators.")
    st.stop()

# Get conversation ID or number from URL parameters
if 'conv' not in st.query_params and 'num' not in st.query_params:
    st.error("No conversation selected.")
    st.stop()

conversation = None
if 'num' in st.query_params:
    try:
        conv_number = int(st.query_params['num'])
        conversation = get_conversation_by_number(conv_number)
    except ValueError:
        st.error("Invalid conversation number.")
        st.stop()
else:
    user_id = st.query_params['conv']
    conversation = get_conversation(user_id)

if not conversation:
    st.error("Conversation not found.")
    st.stop()

# Add a button to show/hide the detailed view
if 'show_details' not in st.session_state:
    st.session_state.show_details = False

if st.button("View Conversation Details", type="primary"):
    st.session_state.show_details = not st.session_state.show_details

if st.session_state.show_details:
    with st.expander("Conversation Details", expanded=True):
        st.title(f"Detailed Conversation with {conversation['user_id']}")
        st.write(f"Last updated: {conversation['last_updated']}")
        
        # Display conversation statistics
        total_messages = len(conversation['messages'])
        user_messages = len([m for m in conversation['messages'] if m['role'] == 'user'])
        assistant_messages = len([m for m in conversation['messages'] if m['role'] == 'assistant'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", total_messages)
        with col2:
            st.metric("User Messages", user_messages)
        with col3:
            st.metric("Assistant Messages", assistant_messages)
        
        # Display messages in a more detailed format
        st.subheader("Message Timeline")
        for message in conversation['messages']:
            role = message['role']
            content = message['content']
            timestamp = message.get('timestamp', 'No timestamp')
            
            with st.expander(f"{role.title()} - {timestamp}"):
                st.markdown(content)

st.title(f"Conversation with {conversation['user_id']} 💬")
st.write(f"Last updated: {conversation['last_updated']}")

# Create a container with grey background for the conversation
st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;'>
""", unsafe_allow_html=True)

# Create a chat-like display
for message in conversation['messages']:
    role = message['role']
    content = message['content']
    timestamp = message.get('timestamp', 'No timestamp')
    
    if role == 'user':
        st.markdown(f"""
            <div style='background-color: #e0e0e0; padding: 10px; border-radius: 5px; margin: 5px 0; color: #000000;'>
                <b>User</b> ({timestamp}):<br>
                {content}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='background-color: #e0e0e0; padding: 10px; border-radius: 5px; margin: 5px 0; color: #000000;'>
                <b>Assistant</b> ({timestamp}):<br>
                {content}
            </div>
        """, unsafe_allow_html=True)

# Close the container
st.markdown("</div>", unsafe_allow_html=True) 