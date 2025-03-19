# WrmXpress-GUI Tests

This directory contains unit tests for the WrmXpress-GUI application.

## Test Structure

The tests are organized as follows:

- `test_configure_page.py`: Tests for the Configure page UI elements and interactions
- `test_components.py`: Tests for individual UI components
- `test_utils.py`: Tests for utility functions

## Running Tests

To run all tests:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_configure_page.py
```

To run a specific test:

```bash
pytest tests/test_configure_page.py::test_configure_page_loads
```

## Test Coverage

These tests cover:

1. UI Elements - Verifying that components render correctly and have expected properties
2. Interactions - Testing that UI interactions (like selecting modules) behave as expected
3. Utility Functions - Validating that helper functions produce correct results
4. Component Structure - Checking that components have the correct structure and organization

## Adding New Tests

When adding new tests:

1. Follow the existing pattern of creating descriptive test functions
2. Use meaningful assertions that verify specific behaviors
3. Group related tests in the same file
4. Add appropriate docstrings to describe the purpose of each test