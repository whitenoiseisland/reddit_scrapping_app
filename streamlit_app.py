import streamlit as st
import praw
import pandas as pd
from datetime import datetime, timedelta

# Hide the fork label, GitHub icon, and app creator avatar
st.set_page_config(
    page_title="Top Posts from a Subreddit",
    page_icon=":shark:",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS to hide the Fork label, GitHub icon, and app creator avatar
hide_style = """
<style>
[data-testid="stToolbarActionButtonLabel"] {
    display: none;
}
[data-testid="stToolbarActionButtonIcon"] {
    display: none;
}
[data-testid="appCreatorAvatar"] {
    display: none;
}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=st.secrets["reddit"]["client_id"],
    client_secret=st.secrets["reddit"]["client_secret"],
    user_agent=st.secrets["reddit"]["user_agent"]
)

st.title("Top Posts from a Subreddit")

# Input for subreddit
subreddit_name = st.text_input("Enter the subreddit name:", "")

if st.button("Fetch and Save Top Posts"):
    st.write(f"Fetching top posts from r/{subreddit_name} in the past 24 hours...")

    subreddit = reddit.subreddit(subreddit_name)
    now = datetime.utcnow()
    past_24_hours = now - timedelta(hours=24)
    top_posts = []

    # Fetch top posts
    for post in subreddit.top(time_filter="day", limit=50):
        if datetime.utcfromtimestamp(post.created_utc) >= past_24_hours:
            top_posts.append({
                "Title": post.title,
                "Score": post.score,
                "URL": post.url,
                "Created": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            })

    # Display posts
    if top_posts:
        st.write("### Top Posts")
        for post in top_posts:
            st.write(f"**{post['Title']}**")
            st.write(f"Score: {post['Score']}")
            st.write(f"URL: {post['URL']}")
            st.write("---")

        # Save to CSV
        df = pd.DataFrame(top_posts)
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "top_posts.csv", "text/csv")
    else:
        st.write("No posts found for the past 24 hours.")
