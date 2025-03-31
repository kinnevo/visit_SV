import streamlit as st

st.set_page_config(
    page_title="Popup Example",
    page_icon="👋",
    layout="wide"
)

# Check if user is authenticated
if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page.")
    st.stop()

# Initialize session state for popup visibility
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False

st.title("Popup Example Page 👋")

# Add a button to show/hide the popup
if st.button("Click me to say hello!", type="primary"):
    st.session_state.show_popup = not st.session_state.show_popup

# Show the popup when button is clicked
if st.session_state.show_popup:
    with st.expander("Hello!", expanded=True):
        st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1>👋 Hello!</h1>
                <p>This is a popup message.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Add a close button
        if st.button("Close"):
            st.session_state.show_popup = False
            st.rerun() 