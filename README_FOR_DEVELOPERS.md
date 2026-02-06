# Developer Guide for `huwise_utils_py`

This guide provides instructions on setting up the development environment, understanding the codebase architecture, and contributing to this repository.

## Table of Contents
- [Coding Standards](#coding-standards)
- [Getting Started](#getting-started)
- [Setting Up the Development Environment](#setting-up-the-development-environment)
- [Project Structure](#project-structure)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Building and Publishing](#building-and-publishing)
- [Documentation](#documentation)
- [Commit Message Guidelines](#commit-message-guidelines)

---

## Coding Standards

This project follows the **DCC Python Coding Standards**. Before contributing, please read:

**[DCC Python Coding Standards](https://dcc-bs.github.io/documentation/coding/python.html)**

Key points:

- **Python 3.12+** required
- **Google-style docstrings** for all modules, classes, and functions
- **Type hints** everywhere
- **Ruff** for linting and formatting
- **pytest** for testing with descriptive test names
- **Structured logging** with key-value pairs (not f-strings)
- **Dataclasses** for data containers, **Pydantic** for validation
- Prefer **functions** over classes for stateless operations

---

## Getting Started

1. **Install uv**

   This project uses [uv](https://docs.astral.sh/uv/) for dependency management and building.

2. **Clone the Repository**
   ```bash
   git clone https://github.com/opendatabs/huwise-utils-py.git
   ```

3. **Change to the Project Directory**
   ```bash
   cd huwise-utils-py
   ```

4. **Ensure You Are on the `develop` Branch**
   ```bash
   git checkout develop
   ```
   **IMPORTANT:** Never push directly to the `main` branch!

5. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

---

## Setting Up the Development Environment

With uv, setting up the development environment is simple:

1. **Install dependencies and create virtual environment**
   ```bash
   uv sync
   ```

   This will:
   - Create a `.venv` virtual environment if it doesn't exist
   - Install all project dependencies (including dev and docs)
   - Install the package in editable mode

2. **Install pre-commit hooks**
   ```bash
   uv run pre-commit install
   ```

3. **Run commands with uv**
   ```bash
   # Run Python
   uv run python

   # Run tests
   uv run pytest

   # Run linting
   uv run ruff check .

   # Format code
   uv run ruff format .

   # Type checking
   uv run ty check src/
   ```

---

## Project Structure

```
huwise-utils-py/
├── src/huwise_utils_py/
│   ├── __init__.py           # Public API exports
│   ├── config.py             # HuwiseConfig (Pydantic)
│   ├── dataset.py            # HuwiseDataset class
│   ├── http.py               # HttpClient, AsyncHttpClient
│   ├── bulk.py               # Bulk operations (sync + async)
│   ├── logger.py             # Logging re-exports
│   ├── utils/                # Utility functions
│   │   ├── decorators.py     # retry decorator
│   │   └── validators.py     # validate_dataset_identifier
│   └── _legacy/              # Backwards-compatible API
│       ├── getters.py        # get_dataset_* functions
│       └── setters.py        # set_dataset_* functions
├── tests/
│   ├── conftest.py           # Shared fixtures
│   ├── unit/                 # Unit tests (mocked)
│   └── integration/          # Integration tests (real API)
├── docs/                     # MkDocs documentation
├── pyproject.toml            # Project configuration
└── .pre-commit-config.yaml   # Pre-commit hooks
```

### Key Components

- **HuwiseConfig**: Pydantic-based configuration with environment variable loading
- **HuwiseDataset**: Main class for dataset operations with method chaining
- **HttpClient/AsyncHttpClient**: HTTP clients with retry logic
- **_legacy**: Backwards-compatible function wrappers

---

## Adding New Features

### Adding Methods to HuwiseDataset

1. Add the method to `src/huwise_utils_py/dataset.py`
2. Follow the existing patterns for getters/setters
3. Add unit tests in `tests/unit/test_dataset.py`
4. Update documentation in `docs/api/dataset.md`

Example:

```python
def get_new_field(self) -> str | None:
    """Retrieve the new field value.

    Returns:
        The field value or None if not set.
    """
    return self._get_metadata_value("template", "field_name")

def set_new_field(self, value: str, *, publish: bool = True) -> Self:
    """Set the new field value.

    Args:
        value: The value to set.
        publish: Whether to publish after updating.

    Returns:
        Self for method chaining.
    """
    return self._set_metadata_value("template", "field_name", value, publish=publish)
```

### Adding Legacy Function Wrappers

For backwards compatibility, add wrapper functions in `_legacy/getters.py` or `_legacy/setters.py`:

```python
def get_new_field(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> str | None:
    """Get the new field of a dataset."""
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    return dataset.get_new_field()
```

Don't forget to:
1. Export in `_legacy/__init__.py`
2. Export in main `__init__.py`
3. Add to `__all__` list

---

## Testing

### Unit Tests

Unit tests use mocked dependencies and don't require real API credentials:

```bash
uv run pytest tests/unit/ -v
```

### Integration Tests

Integration tests make real API calls and require valid credentials:

```bash
uv run pytest tests/integration/ -v
```

### All Tests

```bash
uv run pytest -v
```

### With Coverage

```bash
uv run pytest --cov=huwise_utils_py --cov-report=html
```

### Test Naming Convention

Follow DCC guidelines:

```python
def test_huwise_dataset_set_title_with_valid_input_returns_self():
    ...

def test_huwise_dataset_from_id_with_invalid_id_raises_value_error():
    ...
```

---

## Code Quality

### Pre-commit Hooks

The project uses pre-commit hooks for automated code quality:

```bash
# Run on all files
uv run pre-commit run --all-files

# Run on staged files only
uv run pre-commit run
```

### Manual Linting and Formatting

```bash
# Lint
uv run ruff check .

# Lint with auto-fix
uv run ruff check . --fix

# Format
uv run ruff format .

# Type check
uv run ty check src/
```

---

## Building and Publishing

### Building the Package

```bash
uv build
```

This creates distribution files in the `dist/` directory.

### Publishing New Version on PyPI

Publishing uses GitHub Actions with Trusted Publishing (no token required):

1. Update the version in `pyproject.toml`:
   ```bash
   # View current version
   uv version

   # Set new version
   uv version 2.1.0

   # Or bump version
   uv version --bump minor
   ```

2. Push to `develop` branch

3. Create a Pull Request into `main` with message "Update to version x.x.x"

4. When merged, manually trigger the publish workflow:
   - Go to Actions > "Publish to PyPI" > Run workflow

---

## Documentation

### Build and Serve Locally

```bash
# Serve documentation locally (with hot reload)
uv run mkdocs serve

# Build documentation
uv run mkdocs build
```

### Documentation Structure

- `docs/index.md` - Home page
- `docs/getting-started.md` - Setup guide
- `docs/api/` - API reference (auto-generated from docstrings)
- `docs/examples.md` - Usage examples
- `docs/migration.md` - v1.x to v2.0 migration guide

---

## Commit Message Guidelines

Commit messages should be meaningful and follow a clear format. Each commit message should complete the sentence:

> "When applied, this commit will ..."

### Guidelines:
- **Start with an uppercase letter**.
- **Do not end with a period**.
- Be **concise** and **descriptive**.

#### Examples:
- `Add HuwiseDataset.get_custom_field method`
- `Fix bulk_get_metadata error handling`
- `Update documentation for v2.0 API`

This format helps maintain clarity and readability in the commit history.
