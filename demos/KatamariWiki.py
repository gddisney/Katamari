from fastapi import FastAPI, Request, Response, Form, HTTPException
from KatamariDB import KatamariMVCC  # Import the provided KatamariMVCC
from KatamariUI import katamari_ui_app, KatamariUI
from typing import Optional, Dict

# Initialize the MVCC store for wiki pages
wiki_db = KatamariMVCC()

# Navbar and Sidebar configurations
navbar_items = [
    {"label": "Home", "link": "/"},
    {"label": "Create New Page", "link": "/edit/new_page"},
]
sidebar_items = [
    {"label": "History", "link": "/history"},
]

# Utility function to begin a transaction for edits
def begin_edit_transaction() -> str:
    return wiki_db.begin_transaction()

# Main wiki page listing all pages
async def home_page_ui(ui: KatamariUI):
    """Render the home page UI with a list of all wiki pages."""
    await ui.add_header("Wiki Home", level=1)
    pages = wiki_db.store.keys()  # List of all pages
    await ui.text("List of Pages:")
    for page_id in pages:
        await ui.text(f"<a href='/wiki/{page_id}'>{page_id}</a>")
    await ui.text("<a href='/edit/new_page'>Create New Page</a>")

# View individual wiki page
async def view_page_ui(ui: KatamariUI, page_id: str):
    """Render a specific wiki page."""
    page_data = wiki_db.get(page_id, None)  # Get the latest version of the page
    if page_data is None:
        raise HTTPException(status_code=404, detail="Page not found")
    
    title = page_data.get("title", "Untitled")
    body = page_data.get("body", "No content available.")
    tags = page_data.get("tags", [])

    await ui.add_header(f"{title}", level=1)
    await ui.text(body)
    await ui.text(f"Tags: {', '.join(tags)}")
    await ui.text(f"<a href='/edit/{page_id}'>Edit</a> | <a href='/history/{page_id}'>View History</a>")

# Edit or create a wiki page
async def edit_page_ui(ui: KatamariUI, page_id: str):
    """Render the form to edit or create a wiki page."""
    page_data = wiki_db.get(page_id, None) or {"title": "", "body": "", "tags": []}
    
    await ui.add_header(f"Edit {page_id}", level=1)
    await ui.input("Page Title:", "title", page_data["title"])
    await ui.textarea("Page Body:", "body", page_data["body"])
    await ui.input("Tags (comma-separated):", "tags", ",".join(page_data["tags"]))
    await ui.button("Save", "save_page")

# Handle the edit form submission
async def submit_edit_page(request: Request, ui: KatamariUI, page_id: str):
    """Handle edit form submission for a wiki page."""
    form_data = await request.form()
    title = form_data.get("title", "Untitled")
    body = form_data.get("body", "")
    tags = form_data.get("tags", "").split(",")

    page_data = {
        "title": title,
        "body": body,
        "tags": [tag.strip() for tag in tags]  # Clean up any extra whitespace
    }
    
    tx_id = begin_edit_transaction()
    wiki_db.put(page_id, page_data, tx_id)  # Store the new version of the page
    wiki_db.commit(tx_id)
    await ui.text(f"Page {page_id} has been updated!")
    return Response(content=await ui.generate_template(), media_type="text/html")

# View history of a wiki page
async def history_page_ui(ui: KatamariUI, page_id: str):
    """Render the version history of a page."""
    history = wiki_db.store[page_id]  # Get all versions of the page
    await ui.add_header(f"History of {page_id}", level=1)
    if history:
        for versioned_value in history:
            await ui.text(f"Version {versioned_value.version} | Timestamp: {versioned_value.timestamp}")
            await ui.text(f"<a href='/revert/{page_id}/{versioned_value.version}'>Revert to this version</a>")
    else:
        await ui.text(f"No history available for {page_id}.")

# Revert to a previous version
async def revert_page_ui(request: Request, ui: KatamariUI, page_id: str, version: int):
    """Revert a wiki page to a specific version."""
    history = wiki_db.store[page_id]
    if version > len(history):
        raise HTTPException(status_code=400, detail="Invalid version")
    # Revert to the selected version
    selected_version = history[version - 1].value
    tx_id = begin_edit_transaction()
    wiki_db.put(page_id, selected_version, tx_id)
    wiki_db.commit(tx_id)
    await ui.text(f"Page {page_id} has been reverted to version {version}.")

# Main FastAPI app with KatamariUI
app = katamari_ui_app(
    home_page_ui,          # Main home page function
    navbar_items,          # Navbar configuration
    sidebar_items,         # Sidebar configuration
    custom_css="",         # Optional custom CSS
    show_sidebar=True,     # Show the sidebar
    theme="light",         # Set the theme to light mode
    requires_auth=False,   # No authentication for this app
)

# Route for viewing a wiki page
@app.get("/wiki/{page_id}", response_class=Response)
async def view_wiki_page(request: Request, page_id: str):
    ui_instance = KatamariUI()
    await view_page_ui(ui_instance, page_id)
    return Response(content=await ui_instance.generate_template(), media_type="text/html")

# Route for editing a wiki page
@app.get("/edit/{page_id}", response_class=Response)
async def edit_wiki_page(request: Request, page_id: str):
    ui_instance = KatamariUI()
    await edit_page_ui(ui_instance, page_id)
    return Response(content=await ui_instance.generate_template(), media_type="text/html")

@app.post("/edit/{page_id}", response_class=Response)
async def submit_edit_wiki_page(request: Request, page_id: str):
    ui_instance = KatamariUI()
    return await submit_edit_page(request, ui_instance, page_id)

# Route for viewing the history of a page
@app.get("/history/{page_id}", response_class=Response)
async def view_wiki_history(request: Request, page_id: str):
    ui_instance = KatamariUI()
    await history_page_ui(ui_instance, page_id)
    return Response(content=await ui_instance.generate_template(), media_type="text/html")

# Route for reverting a page to a previous version
@app.get("/revert/{page_id}/{version}", response_class=Response)
async def revert_wiki_page(request: Request, page_id: str, version: int):
    ui_instance = KatamariUI()
    await revert_page_ui(request, ui_instance, page_id, version)
    return Response(content=await ui_instance.generate_template(), media_type="text/html")

