import os
import requests

# Load the API key from the environment
API_KEY = os.getenv("X_API_KEY")

# Check if the API key is valid
if API_KEY is None:
    raise ValueError("The Application Default Credentials are not available. "
                     "The environment variable X_API_KEY must be defined "
                     "containing a valid API key.")

# Use the key to access the API
HEADERS = {"X-API-KEY": API_KEY}

# Create a requests module session
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# Define the live API URL
API_URL = "https://fastfuels.silvx.io"


