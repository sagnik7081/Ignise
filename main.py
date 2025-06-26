import streamlit as st
import time
from datetime import datetime
from dotenv import load_dotenv
from database import init_db, create_user, verify_user, save_conversation, get_user_conversations, get_conversation_messages
from ai_assistant import AIAssistant
from ui_components import (
    render_auth_page, 
    render_chat_interface, 
    render_sidebar,
    apply_custom_css,
    show_typing_animation
)
from file_handler import handle_file_upload

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    # Initialize database
    init_db()
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'current_conversation_id' not in st.session_state:
        st.session_state.current_conversation_id = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()
    
    # Authentication Flow
    if not st.session_state.authenticated:
        render_auth_page()
    else:
        # Main Chat Interface
        render_chat_interface()

def handle_user_input():
    """Handle user input and generate AI response"""
    if st.session_state.user_input and st.session_state.user_input.strip():
        user_message = st.session_state.user_input.strip()
        
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user", 
            "content": user_message,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Show typing animation
        with st.spinner("🤖 AI is thinking..."):
            time.sleep(1)  # Simulate processing time
            
            # Generate AI response
            ai_response = st.session_state.ai_assistant.generate_response(
                user_message, 
                st.session_state.messages
            )
            
            # Add AI response to chat
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
        
        # Save conversation to database
        if st.session_state.current_conversation_id:
            save_conversation(
                st.session_state.current_conversation_id,
                st.session_state.username,
                user_message,
                ai_response
            )
        
        # Clear input
        st.session_state.user_input = ""
        st.rerun()

def start_new_conversation():
    """Start a new conversation"""
    st.session_state.current_conversation_id = f"conv_{int(time.time())}"
    st.session_state.messages = []
    st.rerun()

def load_conversation(conv_id):
    """Load a specific conversation"""
    st.session_state.current_conversation_id = conv_id
    messages = get_conversation_messages(conv_id)
    st.session_state.messages = messages
    st.rerun()

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.current_conversation_id = None
    st.session_state.messages = []
    st.rerun()

if __name__ == "__main__":
    main()