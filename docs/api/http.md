# HTTP Clients

Low-level HTTP clients for making API requests.

## Overview

The library provides two HTTP clients:

- **HttpClient**: Synchronous client for simple use cases
- **AsyncHttpClient**: Asynchronous client for concurrent operations

Both clients include:

- Automatic retry with exponential backoff
- Proper timeout handling
- Connection pooling (async)
- HTTP/2 support (async)

## Usage

### Synchronous Client

```python
from huwise_utils_py import HuwiseConfig, HttpClient

config = HuwiseConfig.from_env()
client = HttpClient(config)

# GET request
response = client.get("/datasets/?limit=10")
data = response.json()

# POST request
response = client.post("/datasets/da_123/publish/")

# PUT request with JSON body
response = client.put("/datasets/da_123/metadata/", json=metadata)
```

### Asynchronous Client

```python
import asyncio
from huwise_utils_py import HuwiseConfig, AsyncHttpClient

config = HuwiseConfig.from_env()
client = AsyncHttpClient(config)

async def fetch_datasets():
    async with client.session() as session:
        # Make concurrent requests
        tasks = [
            session.get(f"{config.base_url}/datasets/{uid}")
            for uid in ["da_123", "da_456", "da_789"]
        ]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# Run async function
datasets = asyncio.run(fetch_datasets())
```

### Custom Requests

For advanced use cases, you can use the clients directly:

```python
# With query parameters
response = client.get("/datasets/", params={"limit": 100, "offset": 0})

# With custom headers (merged with auth headers)
response = client.get("/datasets/", headers={"X-Custom": "value"})
```

## Retry Logic

Both clients use automatic retry for transient errors:

- Connection errors
- Timeout errors
- HTTP 5xx errors

Default settings:

- 6 retry attempts
- 5 second initial delay
- Exponential backoff (delay doubles each retry)

## API Reference

::: huwise_utils_py.http.HttpClient
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - get
        - post
        - put
        - patch
        - delete

::: huwise_utils_py.http.AsyncHttpClient
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - session
        - get
        - post
        - put
