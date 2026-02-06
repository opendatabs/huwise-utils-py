"""Integration tests for huwise_utils_py.

Integration tests require real API credentials and make actual API calls.
These tests are excluded from CI and should be run manually.

To run integration tests:
    uv run pytest tests/integration/ -v

Required environment variables:
    - HUWISE_API_KEY
    - HUWISE_DOMAIN
"""
