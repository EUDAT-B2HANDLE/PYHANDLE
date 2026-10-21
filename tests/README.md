# Tests

Install the development dependencies and run the unit tests from the repository root:

```console
uv sync --all-groups
uv run pytest
```

Tests requiring access to a Handle server are integration tests and need their
credentials configured separately. The regular pytest run covers unit tests only.
