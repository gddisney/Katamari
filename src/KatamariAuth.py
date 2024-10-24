from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Dict
from KatamariIAM import KatamariIAM  # Assuming KatamariIAM is available
from KatamariDB import KatamariMVCC  # Assuming KatamariMVCC from KatamariDB is available
from KatamariUI import katamari_ui_app
from datetime import timedelta
from fastapi import HTTPException

# OAuth2 token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Initialize KatamariIAM (with a secret key for JWT)
iam = KatamariIAM(secret_key="super_secret_key")

# Set token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Navbar and Sidebar configuration for the UI
navbar_items = [{"label": "Dashboard", "link": "/dashboard"}, {"label": "Logout", "link": "/logout"}]
sidebar_items = [{"label": "Home", "link": "/"}, {"label": "Settings", "link": "/settings"}]


async def authenticate_user(credentials: OAuth2PasswordRequestForm) -> Dict[str, str]:
    """Authenticate the user and issue a JWT token."""
    user = await iam.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = iam.generate_jwt(
        credentials.username, user["roles"], expires_in=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get the current user based on the JWT token."""
    payload = iam.decode_jwt(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


async def dashboard_page(ui):
    """Build the dashboard page."""
    await ui.add_header("Welcome to the Dashboard")
    await ui.text("This is your dashboard where you can access secured resources.")


async def login_page(ui):
    """Build the login form."""
    await ui.add_header("Login", level=2)
    await ui.input("Username", "username")
    await ui.input("Password", "password")
    await ui.button("Login", "submit")


async def register_page(ui):
    """Build the registration form."""
    await ui.add_header("Register", level=2)
    await ui.input("Username", "username")
    await ui.input("Password", "password")
    await ui.input("Roles (comma-separated)", "roles", value="user")
    await ui.button("Register", "submit")


# Create the KatamariUI FastAPI app using katamari_ui_app
app = katamari_ui_app(
    ui_func=dashboard_page,  # Define the UI rendering function for the dashboard
    navbar_items=navbar_items,
    sidebar_items=sidebar_items,
    theme="light",
    requires_auth=True,
    credentials_validator=get_current_user,  # Set the authentication dependency
)


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Handle login and issue access tokens."""
    return await authenticate_user(form_data)


@app.get("/register")
async def render_register_form():
    """Render the registration form."""
    return await register_page(katamari_ui_app)


@app.post("/register")
async def handle_register_form(username: str = Form(...), password: str = Form(...), roles: str = Form("user")):
    """Handle user registration."""
    roles_list = roles.split(",")  # Convert roles input to a list
    await iam.create_user(username, password, roles=roles_list)
    return {"message": "User registered successfully. Please login."}


@app.get("/login")
async def render_login_form():
    """Render the login form."""
    return await login_page(katamari_ui_app)


