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

def render_page():
    # Check if user is authenticated and is admin
    if not st.session_state.get('authenticated', False):
        st.warning("Please login to access this page.")
        return

    if st.session_state.get('user_role') != 'admin':
        st.error("Access denied. This page is only available for administrators.")
        return

    # Get the selected conversation from session state
    selected_conv = st.session_state.get('selected_conversation')
    if not selected_conv:
        st.error("No conversation selected. Please go back to the Admin Dashboard.")
        return

    st.title(f"Conversation with {selected_conv['user_id']} 💬")
    st.write(f"Last updated: {selected_conv['last_updated']}")

    # Create a container with grey background for the conversation
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;'>
    """, unsafe_allow_html=True)

    # Create a chat-like display
    for message in selected_conv['messages']:
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

    # Add a back button
    if st.button("Back to Admin Dashboard"):
        st.switch_page("pages/5_Admin_Dashboard.py")

if __name__ == "__main__":
    st.set_page_config(
        page_title="View Conversation",
        page_icon="💬",
        layout="wide"
    )
    render_page() 