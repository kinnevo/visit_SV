import streamlit as st
import sqlite3
import json
from datetime import datetime
import pandas as pd
import io

def get_all_conversations():
    """Retrieve all conversations from the database."""
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    
    # Get all conversations for admin view
    c.execute('SELECT id, user_id, conversation_data, last_updated FROM conversations')
    results = c.fetchall()
    
    conn.close()
    
    conversations = []
    for id, user_id, conversation_data, last_updated in results:
        try:
            messages = json.loads(conversation_data)
            conversations.append({
                'id': id,
                'user_id': user_id,
                'messages': messages,
                'last_updated': last_updated
            })
        except json.JSONDecodeError:
            continue
    
    return conversations

st.set_page_config(
    page_title="Admin Dashboard - Conversation History",
    page_icon="🔍",
    layout="wide"
)

# Check if user is authenticated and is admin
if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page.")
    st.stop()

if st.session_state.get('user_role') != 'admin':
    st.error("Access denied. This page is only available for administrators.")
    st.stop()

st.title("Admin Dashboard - Conversation History 🔍")

# Get all conversations
conversations = get_all_conversations()

if not conversations:
    st.info("No conversations found in the database.")
else:
    # Initialize session state for active tab if not exists
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Conversation List"
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Conversation List", "Detailed View"])
    
    with tab1:
        # Create a summary table
        summary_data = []
        for conv in conversations:
            user_id = conv['user_id']
            message_count = len(conv['messages'])
            last_updated = conv['last_updated']
            
            # Get the last message
            last_message = conv['messages'][-1]['content'] if conv['messages'] else "No messages"
            last_message = last_message[:100] + "..." if len(last_message) > 100 else last_message
            
            summary_data.append({
                'ID': conv['id'],
                'User ID': user_id,
                'Message Count': message_count,
                'Last Updated': last_updated,
                'Last Message': last_message
            })
        
        df = pd.DataFrame(summary_data)
        
        # Display the dataframe with clickable links
        for idx, row in df.iterrows():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 1, 2, 3, 1, 1])
            with col1:
                st.write(row['ID'])
            with col2:
                st.write(row['User ID'])
            with col3:
                st.write(row['Message Count'])
            with col4:
                st.write(row['Last Updated'])
            with col5:
                st.write(row['Last Message'])
            with col6:
                if st.button('View', key=f'view_{idx}'):
                    st.session_state.selected_conversation = conversations[idx]
                    st.session_state.selected_conversation_id = row['ID']
                    st.switch_page("pages/6_View_Conversation.py")
            with col7:
                # Create DataFrame for the conversation
                messages_data = []
                for msg in conversations[idx]['messages']:
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
                    label="📥",
                    data=csv_str,
                    file_name=f"conversation_{row['User ID']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    help="Download conversation as CSV",
                    key=f'download_{idx}'
                )
    
    with tab2:
        # Allow selecting a specific conversation to view
        selected_user = st.selectbox(
            "Select a user to view their conversation:",
            options=[conv['user_id'] for conv in conversations],
            key='selected_user',
            index=([conv['user_id'] for conv in conversations].index(st.session_state.get('selected_user', conversations[0]['user_id'])))
        )
        
        # Display the selected conversation
        selected_conv = next((conv for conv in conversations if conv['user_id'] == selected_user), None)
        
        if selected_conv:
            st.markdown(f"""
                <div style='background-color: #2b2b2b; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                    <h2 style='color: white; margin: 0;'>Conversation with {selected_user}</h2>
                    <p style='color: #cccccc; margin: 5px 0 0 0;'>Last updated: {selected_conv['last_updated']}</p>
                </div>
            """, unsafe_allow_html=True)
            
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