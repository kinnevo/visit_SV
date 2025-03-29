import streamlit as st
import json
from datetime import datetime

st.set_page_config(
    page_title="Community - Silicon Valley Visit Planner",
    page_icon="👥",
    layout="wide"
)

# Check authentication
if not st.session_state.get('authenticated', False):
    st.warning("Please login to access this page.")
    st.stop()

st.title("Silicon Valley Visit Community 👥")

# Initialize community data
if 'community_posts' not in st.session_state:
    st.session_state.community_posts = []

def load_community_posts():
    try:
        with open('community_posts.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_community_posts(posts):
    with open('community_posts.json', 'w') as f:
        json.dump(posts, f)

# Load existing posts
st.session_state.community_posts = load_community_posts()

# Create new post
with st.expander("Create New Post"):
    st.subheader("Share Your Experience")
    post_title = st.text_input("Title")
    post_content = st.text_area("Content")
    post_category = st.selectbox(
        "Category",
        ["Pre-Visit Planning", "During Visit", "Post-Visit Impact", "General Discussion"]
    )
    
    if st.button("Post"):
        if post_title and post_content:
            new_post = {
                "title": post_title,
                "content": post_content,
                "category": post_category,
                "author": st.session_state.username,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.community_posts.append(new_post)
            save_community_posts(st.session_state.community_posts)
            st.success("Post created successfully!")
            st.rerun()
        else:
            st.error("Please fill in both title and content.")

# Display posts
st.header("Community Posts")

# Filter posts by category
category_filter = st.selectbox(
    "Filter by Category",
    ["All"] + list(set(post["category"] for post in st.session_state.community_posts))
)

# Display filtered posts
for post in reversed(st.session_state.community_posts):
    if category_filter == "All" or post["category"] == category_filter:
        with st.container():
            st.markdown(f"### {post['title']}")
            st.markdown(f"**Category:** {post['category']}")
            st.markdown(f"**Posted by:** {post['author']} on {post['date']}")
            st.markdown(post['content'])
            st.markdown("---")

# Community statistics
st.sidebar.header("Community Statistics")
total_posts = len(st.session_state.community_posts)
st.sidebar.metric("Total Posts", total_posts)

# Categories breakdown
categories = {}
for post in st.session_state.community_posts:
    categories[post['category']] = categories.get(post['category'], 0) + 1

st.sidebar.subheader("Posts by Category")
for category, count in categories.items():
    st.sidebar.metric(category, count)

# Community guidelines
st.sidebar.header("Community Guidelines")
st.sidebar.markdown("""
1. Be respectful and professional
2. Share authentic experiences
3. Provide helpful information
4. Follow posting categories
5. Report inappropriate content
""") 