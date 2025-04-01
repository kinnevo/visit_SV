import streamlit as st
import sqlite3
import json
from datetime import datetime
import pandas as pd
import io

def get_conversation_by_id(conv_id):
    """Retrieve a conversation by its ID from the database."""
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    
    # Get conversation by ID
    c.execute('SELECT user_id, conversation_data, last_updated FROM conversations WHERE id = ?', (conv_id,))
    result = c.fetchone()
    
    conn.close()
    
    if result:
        user_id, conversation_data, last_updated = result
        try:
            messages = json.loads(conversation_data)
            return {
                'id': conv_id,
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

    # Get the conversation ID from session state
    conv_id = st.session_state.get('selected_conversation_id')

    # Display conversation information in a more organized way
    st.markdown(f"""
        <div style='background-color: #2b2b2b; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <h2>Conversation ID: {conv_id} with {selected_conv['user_id']} 💬</h2>
            <p>Last updated: {selected_conv['last_updated']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Add refresh and download buttons in a row
    col1, col2 = st.columns([1, 6])
    with col1:
        # Get the current conversation ID from session state
        current_conv_id = st.session_state.get('selected_conversation_id')
        if st.button(f"🔄 Refresh Conversation ID: {current_conv_id}"):
            # Reload the conversation data from database using the conversation ID
            refreshed_conv = get_conversation_by_id(current_conv_id)
            if refreshed_conv:
                st.session_state.selected_conversation = refreshed_conv
                st.rerun()
    with col2:
        # Create DataFrame for the conversation
        messages_data = []
        for msg in selected_conv['messages']:
            messages_data.append({
                'Timestamp': msg.get('timestamp', 'No timestamp'),
                'Role': msg['role'],
                'Content': msg['content']
            })
        conv_df = pd.DataFrame(messages_data)
        
        # Create CSV in memory
        csv_buffer = io.StringIO()
        conv_df.to_csv(csv_buffer, index=False)
        csv_str = csv_buffer.getvalue()
        
        # Create download button
        st.download_button(
            label="📥 Download Conversation",
            data=csv_str,
            file_name=f"conversation_{selected_conv['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download conversation as CSV"
        )

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