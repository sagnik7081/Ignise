import sqlite3
import hashlib
import json
from datetime import datetime

DATABASE_NAME = "chatbot.db"

def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Create a new user"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        
        conn.commit()
        conn.close()
        return True, "User created successfully! 🎉"
    except sqlite3.IntegrityError:
        return False, "Username already exists! 😅"
    except Exception as e:
        return False, f"Error creating user: {str(e)}"

def verify_user(username, password):
    """Verify user credentials"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute(
            "SELECT username FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return True, "Login successful! 🚀"
        else:
            return False, "Invalid credentials! 🔒"
    except Exception as e:
        return False, f"Error verifying user: {str(e)}"

def save_conversation(conversation_id, username, user_message, ai_response):
    """Save conversation messages to database"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Check if conversation exists, if not create it
        cursor.execute(
            "SELECT id FROM conversations WHERE id = ?",
            (conversation_id,)
        )
        
        if not cursor.fetchone():
            # Create new conversation with title from first user message
            title = user_message[:50] + "..." if len(user_message) > 50 else user_message
            cursor.execute(
                "INSERT INTO conversations (id, username, title) VALUES (?, ?, ?)",
                (conversation_id, username, title)
            )
        
        # Save user message
        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conversation_id, "user", user_message)
        )
        
        # Save AI response
        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conversation_id, "assistant", ai_response)
        )
        
        # Update conversation timestamp
        cursor.execute(
            "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (conversation_id,)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving conversation: {str(e)}")
        return False

def get_user_conversations(username):
    """Get all conversations for a user"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, title, updated_at FROM conversations WHERE username = ? ORDER BY updated_at DESC",
            (username,)
        )
        
        conversations = cursor.fetchall()
        conn.close()
        
        return [{"id": conv[0], "title": conv[1], "updated_at": conv[2]} for conv in conversations]
    except Exception as e:
        print(f"Error getting conversations: {str(e)}")
        return []

def get_conversation_messages(conversation_id):
    """Get all messages for a conversation"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
            (conversation_id,)
        )
        
        messages = cursor.fetchall()
        conn.close()
        
        return [
            {
                "role": msg[0], 
                "content": msg[1], 
                "timestamp": datetime.fromisoformat(msg[2]).strftime("%H:%M") if msg[2] else ""
            } 
            for msg in messages
        ]
    except Exception as e:
        print(f"Error getting messages: {str(e)}")
        return []