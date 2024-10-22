from fastapi import FastAPI, Request, Response, Form, HTTPException
from KatamariDB import KatamariMVCC  # Import the provided KatamariMVCC
from KatamariUI import katamari_ui_app, KatamariUI
import time

# Initialize the MVCC store for tweets and comments
tweet_db = KatamariMVCC()
comment_db = KatamariMVCC()

# Navbar and Sidebar configurations
navbar_items = [
    {"label": "Home", "link": "/"},
    {"label": "New Tweet", "link": "/new_tweet"},
]
sidebar_items = [
    {"label": "All Tweets", "link": "/tweets"},
]

# Utility function to begin a transaction for edits
def begin_transaction() -> str:
    return tweet_db.begin_transaction()

# Main timeline page showing all tweets
async def timeline_page_ui(ui: KatamariUI):
    """Render the timeline UI showing all tweets."""
    await ui.add_header("Timeline", level=1)
    tweets = tweet_db.store.keys()  # Get all tweet IDs
    for tweet_id in tweets:
        tweet_data = tweet_db.get(tweet_id, None)
        await ui.text(f"<strong>{tweet_data['username']}:</strong> {tweet_data['content']}")
        await ui.text(f"<a href='/tweet/{tweet_id}'>View Tweet</a> | <a href='/like/{tweet_id}'>Like ({tweet_data['likes']})</a>")
        await ui.text("<hr>")

# View an individual tweet and its comments
async def view_tweet_ui(ui: KatamariUI, tweet_id: str):
    """Render a specific tweet along with its comments."""
    tweet_data = tweet_db.get(tweet_id, None)
    if tweet_data is None:
        raise HTTPException(status_code=404, detail="Tweet not found")

    await ui.add_header(f"{tweet_data['username']}'s Tweet", level=1)
    await ui.text(tweet_data["content"])
    await ui.text(f"Likes: {tweet_data['likes']}")
    await ui.text("<hr>")
    
    await ui.text("Comments:")
    for comment_id in tweet_data.get("comments", []):
        comment_data = comment_db.get(comment_id, None)
        if comment_data:
            await ui.text(f"{comment_data['username']}: {comment_data['content']}")

    await ui.textarea("Add a comment:", "comment")
    await ui.button("Submit Comment", "submit_comment")

# Post a new tweet
async def new_tweet_ui(ui: KatamariUI):
    """Render the form to post a new tweet."""
    await ui.add_header("New Tweet", level=1)
    await ui.input("Username", "username")
    await ui.textarea("What's happening?", "content")
    await ui.button("Tweet", "post_tweet")

# Handle new tweet submission
async def submit_new_tweet(request: Request):
    """Handle the form submission for posting a new tweet."""
    ui_instance = KatamariUI()  # Create a new UI instance
    form_data = await request.form()
    username = form_data.get("username", "Anonymous")
    content = form_data.get("content", "")

    tweet_data = {
        "username": username,
        "content": content,
        "likes": 0,
        "comments": []
    }

    tx_id = begin_transaction()
    tweet_id = f"tweet_{time.time_ns()}"
    tweet_db.put(tweet_id, tweet_data, tx_id)
    tweet_db.commit(tx_id)
    
    await ui_instance.text("Tweet posted!")
    return Response(content=await ui_instance.generate_template(), media_type="text/html")

# Post a comment on a tweet
async def submit_comment(request: Request, tweet_id: str):
    """Handle submitting a comment on a tweet."""
    ui_instance = KatamariUI()  # Create a new UI instance
    form_data = await request.form()
    comment_content = form_data.get("comment", "")
    
    tweet_data = tweet_db.get(tweet_id, None)
    if tweet_data is None:
        raise HTTPException(status_code=404, detail="Tweet not found")

    comment_data = {
        "username": "Anonymous",  # Can be replaced with actual user handling
        "content": comment_content
    }

    tx_id = begin_transaction()
    comment_id = f"comment_{time.time_ns()}"
    comment_db.put(comment_id, comment_data, tx_id)
    tweet_data["comments"].append(comment_id)  # Add the comment to the tweet
    tweet_db.put(tweet_id, tweet_data, tx_id)
    tweet_db.commit(tx_id)

    await ui_instance.text(f"Comment posted on {tweet_id}!")
    return Response(content=await ui_instance.generate_template(), media_type="text/html")

# Like a tweet
async def like_tweet(request: Request, tweet_id: str):
    """Handle liking a tweet."""
    tweet_data = tweet_db.get(tweet_id, None)
    if tweet_data is None:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    tweet_data["likes"] += 1  # Increment likes
    tx_id = begin_transaction()
    tweet_db.put(tweet_id, tweet_data, tx_id)
    tweet_db.commit(tx_id)

    return Response(content="Liked", media_type="text/html")

# Main FastAPI app with KatamariUI
app = katamari_ui_app(
    timeline_page_ui,        # Main timeline function
    navbar_items,            # Navbar configuration
    sidebar_items,           # Sidebar configuration
    custom_css="",           # Optional custom CSS
    show_sidebar=True,       # Show the sidebar
    theme="light",           # Set the theme to light mode
    requires_auth=False,     # No authentication for this app
)

# Route for viewing a tweet
@app.get("/tweet/{tweet_id}", response_class=Response)
async def view_tweet(request: Request, tweet_id: str):
    ui_instance = KatamariUI()
    await view_tweet_ui(ui_instance, tweet_id)
    return Response(content=await ui_instance.generate_template(), media_type="text/html")

# Route for posting a new tweet
@app.get("/new_tweet", response_class=Response)
async def new_tweet(request: Request):
    ui_instance = KatamariUI()
    await new_tweet_ui(ui_instance)
    return Response(content=await ui_instance.generate_template(), media_type="text/html")

@app.post("/new_tweet", response_class=Response)
async def submit_new_tweet_route(request: Request):
    return await submit_new_tweet(request)

# Route for submitting a comment on a tweet
@app.post("/tweet/{tweet_id}/comment", response_class=Response)
async def submit_comment_tweet(request: Request, tweet_id: str):
    return await submit_comment(request, tweet_id)

# Route for liking a tweet
@app.get("/like/{tweet_id}", response_class=Response)
async def like_tweet_route(request: Request, tweet_id: str):
    return await like_tweet(request, tweet_id)

