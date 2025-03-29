import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Example Visit - Silicon Valley Visit Planner",
    page_icon="🗺️",
    layout="wide"
)

# Check authentication
if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page.")
    st.stop()

st.title("Example Silicon Valley Visit 🗺️")

# Example Visit Timeline
st.header("A Week in Silicon Valley")

# Pre-Visit Planning
st.subheader("Pre-Visit Planning (2-3 months before)")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### Research & Preparation
    - Research companies to visit
    - Connect with local contacts
    - Book accommodations
    - Plan transportation
    """)
with col2:
    st.markdown("""
    ### Logistics
    - Apply for necessary visas
    - Book flights
    - Arrange transportation from airport
    - Set up mobile phone plan
    """)

# During Visit
st.subheader("During Your Visit (1 week)")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    ### Day 1-2: Arrival & Orientation
    - Arrive at SFO
    - Check into accommodation
    - Visit Computer History Museum
    - Explore downtown Palo Alto
    """)
with col2:
    st.markdown("""
    ### Day 3-4: Company Visits
    - Google Campus tour
    - Apple Park Visitor Center
    - Stanford University tour
    - Networking event
    """)
with col3:
    st.markdown("""
    ### Day 5-7: Immersion
    - Y Combinator HQ visit
    - Meet with startup founders
    - Visit local incubators
    - Cultural activities
    """)

# Post-Visit
st.subheader("Post-Visit Impact")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### Immediate Actions
    - Follow up with contacts
    - Document learnings
    - Share experiences
    - Plan next steps
    """)
with col2:
    st.markdown("""
    ### Long-term Impact
    - Project development
    - Network building
    - Knowledge application
    - Community engagement
    """)

# Tips and Recommendations
st.header("Tips & Recommendations")
st.markdown("""
### Best Practices
1. **Networking**
   - Attend local meetups
   - Connect on LinkedIn
   - Follow up promptly

2. **Planning**
   - Book company visits early
   - Plan for traffic
   - Consider public transport

3. **Experience**
   - Document everything
   - Take photos
   - Keep a journal

4. **Follow-up**
   - Send thank you notes
   - Share your experience
   - Stay connected
""")

# Add some example images
try:
    col1, col2 = st.columns(2)
    with col1:
        st.image("assets/google_campus.jpg", caption="Google Campus", use_container_width=True)
    with col2:
        st.image("assets/apple_park.jpg", caption="Apple Park", use_container_width=True)
except:
    st.info("Images will be displayed here when available.") 