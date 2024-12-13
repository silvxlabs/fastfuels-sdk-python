# How to Set Up Authentication for FastFuels SDK

This guide shows you how to configure API authentication for the FastFuels SDK in different environments.

## How to Configure Authentication Using Environment Variables

For production environments, set your API key as an environment variable:

```bash
# Linux/MacOS
export FASTFUELS_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set FASTFUELS_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:FASTFUELS_API_KEY="your-api-key-here"
```

Then import and use the SDK - it will automatically use the environment variable:

```python
from fastfuels_sdk import api
from fastfuels_sdk.domains import Domain

# SDK automatically uses FASTFUELS_API_KEY environment variable
domain = Domain.from_id("your-domain-id")
```

## How to Configure Authentication Programmatically

For development or testing environments, set the API key in your code:

```python
from fastfuels_sdk import api

# Configure the API key
api.set_api_key("your-api-key-here")

# SDK will now use this key for all operations
```

## How to Handle Missing Authentication

Add error handling for cases where authentication isn't properly configured:

```python
from fastfuels_sdk import api
from fastfuels_sdk.client_library.exceptions import UnauthorizedException

try:
    # Will raise UnauthorizedException if no API key is configured
    from fastfuels_sdk.domains import Domain
    domain = Domain.from_id("your-domain-id")
except UnauthorizedException as e:
    print(f"Authentication error: {e}")
    # Add your error handling logic here
```


## How to Update Authentication at Runtime

If you need to switch API keys during execution:

```python
from fastfuels_sdk import api

def switch_auth_key(new_key: str) -> None:
    """Update authentication to use a new API key."""
    api.set_api_key(new_key)

# Usage
switch_auth_key("new-api-key")
```

Remember: The API client is maintained as a singleton, so setting a new API key affects all subsequent operations in your application.
