import os
import requests

# Load the API key from the environment
api_key = os.getenv("FASTFUELS_API_KEY")

# Check if the API key is valid
if api_key is None:
    raise ValueError(
        "The Application Default Credentials are not available. "
        "The environment variable FASTFUELS_API_KEY must be defined "
        "containing a valid API key.")

# Use the key to access the API
headers = {"X-API-KEY": api_key}

# Create a requests module session
SESSION = requests.Session()
SESSION.headers.update(headers)

# Define the live API URL
API_URL = "https://fastfuels.silvx.io"
