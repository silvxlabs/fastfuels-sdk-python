import os
import requests


class FastFuelsAPI:
    def __init__(self):
        # Load the API key from the environment
        api_key = os.getenv("FF_API_KEY")

        # Check if the API key is valid
        if api_key is None:
            raise ValueError(
                "The Application Default Credentials are not available. "
                "The environment variable FF_API_KEY must be defined "
                "containing a valid API key.")

        # Use the key to access the API
        self.headers = {"X-API-KEY": api_key}

        # Create a requests module session
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Define the live API URL
        self.api_url = "https://fastfuels.silvx.io"
