import pytest
import os
import time
from dash.testing.application_runners import import_app
from dash.testing.composite import DashComposite

# Check if running in CI environment
IS_CI = os.environ.get('TEST_MODE') == 'ci'

# Skip tests when not in CI environment
pytestmark = pytest.mark.skipif(
    not IS_CI, 
    reason="Integration tests require a proper CI environment"
)

@pytest.fixture
def dash_duo():
    with DashComposite(browser='chrome') as dc:
        yield dc

@pytest.mark.integration
def test_app_loads(dash_duo):
    """Test that the app loads correctly."""
    # Import the app
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Check that the app loads and sidebar is visible
    dash_duo.wait_for_element("#page-content", timeout=10)
    dash_duo.wait_for_element(".sidebar")
    
    # Check that the app title is visible
    dash_duo.wait_for_element("img[src*='logo']")

@pytest.mark.integration
def test_navigation(dash_duo):
    """Test navigation between pages."""
    # Import the app
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Wait for the app to load
    dash_duo.wait_for_element("#page-content", timeout=10)
    
    # Navigate to the configure page
    dash_duo.find_element('a[href="/configure"]').click()
    dash_duo.wait_for_element("#configure-accordion")
    
    # Navigate to the metadata page
    dash_duo.find_element('a[href="/metadata"]').click()
    dash_duo.wait_for_element("#metadata-page-content")
    
    # Navigate to the preview page
    dash_duo.find_element('a[href="/preview"]').click()
    dash_duo.wait_for_element("#preview-page-content")
    
    # Navigate to the run page
    dash_duo.find_element('a[href="/run"]').click()
    dash_duo.wait_for_element("#run-page-content")

@pytest.mark.integration
def test_configure_page_interaction(dash_duo):
    """Test interactions on the configure page."""
    # Import the app
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Navigate to the configure page
    dash_duo.wait_for_element("#page-content", timeout=10)
    dash_duo.find_element('a[href="/configure"]').click()
    
    # Wait for the page to load
    dash_duo.wait_for_element("#configure-accordion")
    
    # Select file structure
    dash_duo.select_dcc_dropdown("#file-structure", "tif")
    
    # Select imaging mode
    dash_duo.select_dcc_dropdown("#imaging-mode", "single-well")
    
    # Select a pipeline
    dash_duo.find_element("#pipeline-selection input[value='motility']").click()
    
    # Verify that motility parameters are visible
    dash_duo.wait_for_element("#motility_params")
    assert dash_duo.get_computed_style("#motility_params", "display") != "none"

# These tests will be skipped unless running in CI environment
# To run locally, set the environment variable TEST_MODE=ci