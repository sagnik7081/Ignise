import streamlit as st
import time
from database import create_user, verify_user, get_user_conversations
from file_handler import handle_file_upload

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Chat messages styling */
    .user-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        margin-left: 20%;
        color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        animation: slideInRight 0.3s ease-out;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        margin-right: 20%;
        color: #333;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 8px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        animation: pulse 0.6s infinite;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 12px 16px;
    }
    
    /* Avatar styling */
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 18px;
        margin-right: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .user-avatar:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    /* Conversation item styling */
    .conversation-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
    }
    
    .conversation-item:hover {
        background: rgba(255, 255, 255, 0.2);
        border-left: 3px solid #4facfe;
        transform: translateX(5px);
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 10px;
        color: #999;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

def render_auth_page():
    """Render authentication page"""
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🤖 Ignise</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-bottom: 3rem;'> Ask Boldly. Learn Brilliantly</p>", unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "✨ Register"])
        
        with tab1:
            st.markdown("### Welcome back! 😊")
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_btn = st.form_submit_button("Login 🚀", use_container_width=True)
                
                if login_btn:
                    if username and password:
                        success, message = verify_user(username, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.success(message)
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please fill in all fields! 📝")
        
        with tab2:
            st.markdown("### Join us today! 🎉")
            with st.form("register_form"):
                new_username = st.text_input("Choose Username", placeholder="Pick a unique username")
                new_password = st.text_input("Create Password", type="password", placeholder="Create a secure password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                register_btn = st.form_submit_button("Register ✨", use_container_width=True)
                
                if register_btn:
                    if new_username and new_password and confirm_password:
                        if new_password == confirm_password:
                            success, message = create_user(new_username, new_password)
                            if success:
                                st.success(message)
                                st.info("You can now login with your credentials! 🎯")
                            else:
                                st.error(message)
                        else:
                            st.error("Passwords don't match! 🔒")
                    else:
                        st.warning("Please fill in all fields! 📝")

def render_sidebar():
    """Render sidebar with chat history and user options"""
    with st.sidebar:
        # User info and controls
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 20px;'>
            <div class='user-avatar'>{st.session_state.username[0].upper()}</div>
            <div>
                <strong>{st.session_state.username}</strong><br>
                <small>Online 🟢</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Switch User", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
        
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.username = ""
                st.rerun()
        
        st.divider()
        
        # New Chat Button
        if st.button("✨ New Chat", use_container_width=True, type="primary"):
            st.session_state.current_conversation_id = f"conv_{int(time.time())}"
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("### 💬 Chat History")
        
        # Load and display conversations
        conversations = get_user_conversations(st.session_state.username)
        
        if conversations:
            for conv in conversations:
                # Create clickable conversation item
                if st.button(
                    f"📝 {conv['title'][:30]}{'...' if len(conv['title']) > 30 else ''}",
                    key=f"conv_{conv['id']}",
                    use_container_width=True,
                    help=f"Last updated: {conv['updated_at']}"
                ):
                    st.session_state.current_conversation_id = conv['id']
                    # Load conversation messages would be handled here
                    st.rerun()
        else:
            st.markdown("*No conversations yet*")
            st.markdown("Start chatting to see your history! 🎯")

def render_chat_interface():
    """Render main chat interface"""
    # Render sidebar
    render_sidebar()
    
    # Main chat area
    st.markdown("## 🤖 Ignise")
    
    # File upload section
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("*Upload documents, ask questions, or just chat!* ✨")
    with col2:
        uploaded_file = st.file_uploader(
            "📎 Upload File", 
            type=['txt', 'pdf', 'docx', 'csv'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            result = handle_file_upload(uploaded_file)
            if result:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result,
                    "timestamp": time.strftime("%H:%M")
                })
                st.rerun()
    
    # Chat messages container
    chat_container = st.container()
    
    # Display messages
    with chat_container:
        if st.session_state.messages:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You</strong> <small>{message.get('timestamp', '')}</small><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="assistant-message">
                        <strong>🤖 AI Assistant</strong> <small>{message.get('timestamp', '')}</small><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Welcome message
            st.markdown(f"""
            <div class="assistant-message">
                <strong>🤖 Ignise</strong><br>
                Hello {st.session_state.username}! 👋✨<br><br>
                Welcome to Ignise — your intelligent AI assistant, always ready to help with:
                <ul>
                    <li>💬 General conversations and questions</li>
                    <li>💻 Programming and coding help</li>
                    <li>📚 Learning and explanations</li>
                    <li>🎨 Creative writing and brainstorming</li>
                    <li>📄 Document analysis (upload files!)</li>
                </ul>
                What would you like to talk about today? 🚀
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Input form
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Message", 
                placeholder="Type your message here... 💭",
                label_visibility="collapsed",
                key="user_input"
            )
        
        with col2:
            send_button = st.form_submit_button("Send 🚀", use_container_width=True)
        
        if send_button and user_input and user_input.strip():
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input.strip(),
                "timestamp": time.strftime("%H:%M")
            })
            
            # Generate AI response
            with st.spinner("🤖 Thinking..."):
                time.sleep(1)  # Simulate processing
                ai_response = st.session_state.ai_assistant.generate_response(
                    user_input.strip(),
                    st.session_state.messages
                )
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": time.strftime("%H:%M")
                })
            
            # Save to database if conversation exists
            if st.session_state.current_conversation_id:
                from database import save_conversation
                save_conversation(
                    st.session_state.current_conversation_id,
                    st.session_state.username,
                    user_input.strip(),
                    ai_response
                )
            
            st.rerun()

def show_typing_animation():
    """Show typing animation"""
    st.markdown("""
    <div class="typing-indicator">
        🤖 AI is typing
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2)