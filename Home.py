import streamlit as st
import os
from PIL import Image
import json

# Set page config
st.set_page_config(
    page_title="Silicon Valley Visit Planner",
    page_icon="🌉",
    layout="wide"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'user'

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

def login(username, password):
    users = load_users()
    if username in users and users[username]['password'] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_role = users[username].get('role', 'user')
        return True
    return False

def register(username, password):
    users = load_users()
    if username in users:
        return False
    # Set default role as 'user', except for 'jazo' which is 'admin'
    role = 'admin' if username == 'jazo' else 'user'
    users[username] = {
        'password': password,
        'role': role
    }
    save_users(users)
    return True

# Main app
st.title("Welcome to Silicon Valley Visit Planner 🌉")


# Sidebar for authentication
with st.sidebar:
    st.header("Authentication")
    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if login(login_username, login_password):
                    st.success("Login successful!")
                else:
                    st.error("Invalid credentials")
        
        with tab2:
            st.subheader("Register")
            reg_username = st.text_input("Username", key="reg_username")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            if st.button("Register"):
                if register(reg_username, reg_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists")
    else:
        st.write(f"Welcome, {st.session_state.username}!")
        st.write(f"Role: {st.session_state.user_role}")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_role = 'user'
            st.rerun()

# Main content
if st.session_state.authenticated:
    # Add a nice header image
    try:
        image = Image.open('assets/sv_header.jpg')
        st.image(image, use_container_width=True)
    except:
        st.write("Welcome to Silicon Valley!")

    st.markdown("""
    ## Your Gateway to Silicon Valley Innovation
    
    Welcome to the Silicon Valley Visit Planner, your comprehensive guide to experiencing the heart of technological innovation. 
    This platform will help you plan, execute, and reflect on your journey through the world's most influential tech ecosystem.
    
    ### What You'll Find Here:
    
    1. **Visit Planning Guide**: Detailed information about planning your trip to Silicon Valley
    2. **Interactive Chat**: Get personalized recommendations and insights about your visit
    3. **Community Access**: Connect with others who have experienced Silicon Valley
    
    ### Your Journey Will Be Structured in Three Stages:
    
    #### 1. Pre-Visit Planning
    - Research and preparation
    - Itinerary planning
    - Company visit arrangements
    - Accommodation and logistics
    
    #### 2. During Your Visit
    - Company tours and meetings
    - Networking events
    - Cultural experiences
    - Local attractions
    
    #### 3. Post-Visit Impact
    - Project development
    - Network building
    - Knowledge application
    - Community engagement
    
    Use the sidebar to navigate through different sections of the app and start planning your Silicon Valley adventure!
    """)
else:
    st.warning("Please login or register to access the full features of the app.") 

    st.markdown("""
    ## Register an account to explore alternatives to visit Silicon Valley
    
    ## Then Login to start a conversation
                
    ## Start a conversation by choosing the option "Share your Dreams" 
    Then type the reason why do you want to visit Silicon Valley and keep a conversation.
    
    """)