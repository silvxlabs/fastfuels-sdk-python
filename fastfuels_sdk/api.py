import os
import requests


class FastFuelsAPI:
    """
    FastFuelsAPI class for the FastFuels SDK.

    This class provides an interface for accessing the FastFuels API. It handles
    authentication and session management, allowing users to make requests to
    the FastFuels API and retrieve data.

    Attributes
    ----------
    headers : dict
        A dictionary containing the headers for API requests, including the
        API key.
    session : requests.Session
        A session object for making HTTP requests to the FastFuels API.
    api_url : str
        The URL of the FastFuels API.

    Methods
    -------
    None

    """

    def __init__(self):
        """
        Initialize a FastFuelsAPI object.

        The FastFuelsAPI object is responsible for handling authentication and
        session management for requests to the FastFuels API.

        Raises
        ------
        ValueError
            If the API key is not available in the environment variables.

        """
        # Load the API key from the environment
        api_key = os.getenv("FASTFUELS_API_KEY")

        # Check if the API key is valid
        if api_key is None:
            raise ValueError(
                "The Application Default Credentials are not available. "
                "The environment variable FASTFUELS_API_KEY must be defined "
                "containing a valid API key.")

        # Use the key to access the API
        self.headers = {"X-API-KEY": api_key}

        # Create a requests module session
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Define the live API URL
        self.api_url = "https://fastfuels.silvx.io"
