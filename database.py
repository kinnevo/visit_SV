import sqlite3
from datetime import datetime
import json

def init_db():
    """Initialize the SQLite database and create necessary tables."""
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    
    # Create conversations table with session_id
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            conversation_data TEXT NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, session_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_conversation(user_id: str, session_id: str, conversation_history: list):
    """Save or update the conversation history for a user session."""
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    
    # Convert conversation history to JSON string
    conversation_json = json.dumps(conversation_history)
    
    # Check if user session already exists
    c.execute('SELECT id FROM conversations WHERE user_id = ? AND session_id = ?', (user_id, session_id))
    existing = c.fetchone()
    
    if existing:
        # Update existing conversation
        c.execute('''
            UPDATE conversations 
            SET conversation_data = ?, last_updated = CURRENT_TIMESTAMP
            WHERE user_id = ? AND session_id = ?
        ''', (conversation_json, user_id, session_id))
    else:
        # Insert new conversation
        c.execute('''
            INSERT INTO conversations (user_id, session_id, conversation_data)
            VALUES (?, ?, ?)
        ''', (user_id, session_id, conversation_json))
    
    conn.commit()
    conn.close()

def get_conversation(user_id: str, session_id: str) -> list:
    """Retrieve the conversation history for a user session."""
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    
    c.execute('SELECT conversation_data FROM conversations WHERE user_id = ? AND session_id = ?', (user_id, session_id))
    result = c.fetchone()
    
    conn.close()
    
    if result:
        return json.loads(result[0])
    return []

def get_user_sessions(user_id: str) -> list:
    """Get all sessions for a user."""
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    
    c.execute('SELECT session_id, last_updated FROM conversations WHERE user_id = ? ORDER BY last_updated DESC', (user_id,))
    sessions = c.fetchall()
    
    conn.close()
    
    return [{'session_id': session[0], 'last_updated': session[1]} for session in sessions] 