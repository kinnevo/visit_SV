import sqlite3
import json
from datetime import datetime

def update_conversations():
    """Update the user_id in existing conversations to match the authenticated user."""
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    
    # Get all conversations
    c.execute('SELECT id, user_id, conversation_data, last_updated FROM conversations')
    results = c.fetchall()
    
    for conv_id, old_user_id, conversation_data, last_updated in results:
        try:
            messages = json.loads(conversation_data)
            # Get the username from the first user message
            for message in messages:
                if message['role'] == 'user':
                    username = message.get('username', old_user_id)
                    # Update the user_id in the database
                    c.execute('UPDATE conversations SET user_id = ? WHERE id = ?', (username, conv_id))
                    print(f"Updated conversation {conv_id} from {old_user_id} to {username}")
                    break
        except json.JSONDecodeError:
            print(f"Error processing conversation {conv_id}")
            continue
    
    conn.commit()
    conn.close()
    print("Update completed!")

if __name__ == "__main__":
    update_conversations() 