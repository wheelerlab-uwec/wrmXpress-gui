import pytest
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define common fixtures for tests
@pytest.fixture(scope="session")
def test_data_dir():
    """Return the path to the test data directory."""
    return os.path.join(os.path.dirname(__file__), "test_data")