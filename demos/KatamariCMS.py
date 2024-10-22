import asyncio
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from KatamariUI import KatamariUI
from KatamariDB import KatamariORM

app = FastAPI()
katamari_ui = KatamariUI(title="Katamari CMS", header="Welcome to Katamari CMS")

# Initialize ORM
schema_fields = {
    'username': 'TEXT',
    'password': 'TEXT',  # In practice, store hashed passwords
    'title': 'TEXT',
    'content': 'TEXT',
    'comments': 'TEXT'  # Storing comments as a serialized JSON string
}
db = KatamariORM(schema_fields=schema_fields, database='katamari_cms_db')


@app.get("/")
async def read_root(request: Request):
    """Render the homepage with a list of posts."""
    await katamari_ui.header("Recent Posts")
    posts = await db.items()  # Fetch all posts
    for post_id, post in posts.items():
        await katamari_ui.text(f"<a href='/post/{post_id}'>{post['title']}</a>")

    return await katamari_ui.generate_template()


@app.get("/post/{post_id}")
async def read_post(request: Request, post_id: str):
    """Render a single post and its comments."""
    post_data = await db.get(post_id)
    if post_data:
        await katamari_ui.header(post_data['title'])
        await katamari_ui.markdown(post_data['content'])
        comments = post_data['comments'] or []
        for comment in comments:
            await katamari_ui.text(f"<p>{comment}</p>")
    else:
        await katamari_ui.text("Post not found.")

    return await katamari_ui.generate_template()


@app.post("/create_post")
async def create_post(request: Request):
    """Create a new post."""
    form_data = await request.form()
    title = form_data.get('title')
    content = form_data.get('content')
    await db.set(title, {'title': title, 'content': content, 'comments': []})
    return await read_root(request)


@app.get("/login")
async def login_page(request: Request):
    """Render the login page."""
    await katamari_ui.header("Login")
    await katamari_ui.input("Username", "username")
    await katamari_ui.input("Password", "password")
    await katamari_ui.text("<button type='submit'>Login</button>")
    return await katamari_ui.generate_template()


@app.post("/login")
async def login(request: Request):
    """Handle user login."""
    form_data = await request.form()
    username = form_data.get('username')
    password = form_data.get('password')
    # Here, you would verify username and password
    return await read_root(request)


@app.post("/post/{post_id}/comment")
async def add_comment(post_id: str, request: Request):
    """Add a comment to a post."""
    form_data = await request.form()
    comment = form_data.get('comment')
    post_data = await db.get(post_id)
    if post_data:
        comments = post_data['comments'] or []
        comments.append(comment)
        await db.set(post_id, {'comments': comments})
    return await read_post(request, post_id)

