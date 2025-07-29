import dropbox
import json
import os
from dropbox.oauth import DropboxOAuth2FlowNoRedirect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN_FILE = "dropbox_token.json"

def save_tokens(access_token, refresh_token):
    """Save the access token and refresh token to a file."""
    token_data = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    with open(TOKEN_FILE, 'w') as token_file:
        json.dump(token_data, token_file, indent=2)

def load_tokens():
    """Load the access token and refresh token from a file if it exists."""
    if not os.path.exists(TOKEN_FILE):
        return None, None
    
    try:
        with open(TOKEN_FILE, 'r') as token_file:
            data = json.load(token_file)
            return data.get("access_token"), data.get("refresh_token")
    except (json.JSONDecodeError, KeyError):
        return None, None

def create_dropbox_client(access_token, refresh_token,app_key,app_secret):
    """Create and validate a Dropbox client with the given token."""
    client = dropbox.Dropbox(
        oauth2_access_token=access_token,
        oauth2_refresh_token=refresh_token,
        app_key=app_key,
        app_secret=app_secret
    )
    account_info = client.users_get_current_account()
    return client, account_info

def perform_oauth_flow(app_key, app_secret):
    """Perform the OAuth2 flow to get new access and refresh tokens."""
    auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret, token_access_type='offline')
    authorize_url = auth_flow.start()
    
    print(f"1. Go to this URL: {authorize_url}")
    print("2. Click 'Allow' (you may need to log in first).")
    print("3. Copy the authorization code.")
    
    auth_code = input("Enter the authorization code here: ").strip()
    oauth_result = auth_flow.finish(auth_code)
    return oauth_result.access_token, oauth_result.refresh_token

def authenticate_dropbox():
    """
    Authenticates with Dropbox using saved token or OAuth2 flow.
    Reads app credentials from environment variables.
    Returns a Dropbox client instance.
    """
    # Get credentials from environment variables
    app_key = os.getenv('APP_KEY')
    app_secret = os.getenv('APP_SECRET')
    
    if not app_key or not app_secret:
        print("Error: APP_KEY and APP_SECRET environment variables must be set.")
        return None
    
    # Try existing tokens first
    access_token, refresh_token = load_tokens()
    
    if access_token:
        try:
            client, account_info = create_dropbox_client(access_token, refresh_token,app_key,app_secret)
            print(f"Using saved token. Authenticated as: {account_info.name.display_name}")
            return client
        except Exception as error:
            print(f"Error using saved token: {error}")
            # Proceed to OAuth flow for new tokens

    # Get new tokens via OAuth flow
    try:
        access_token, refresh_token = perform_oauth_flow(app_key, app_secret)
        save_tokens(access_token, refresh_token)
        
        client, account_info = create_dropbox_client(access_token, refresh_token,app_key,app_secret)
        print(f"Successfully authenticated as: {account_info.name.display_name}")
        return client
        
    except Exception as error:
        print(f"Error during authentication: {error}")
        return None

if __name__ == '__main__':
    dropbox_client = authenticate_dropbox()
    
    if dropbox_client:
        print("Authentication successful! You can now use the dropbox_client object.")