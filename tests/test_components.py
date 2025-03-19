import pytest
from dash import Dash
import dash_bootstrap_components as dbc
from app.components.instrument_settings import instrument_settings
from app.components.module_selection import module_selection
from app.components.header import header

def test_instrument_settings_component():
    """Test that the instrument settings component has the expected structure."""
    # Verify component ID
    assert instrument_settings.id == "instrument-settings-file-structure"
    
    # Check that the component has a title
    assert instrument_settings.title == "Instrument Settings"
    
    # Check that the component has a body
    assert hasattr(instrument_settings, "children")
    
def test_module_selection_component():
    """Test that the module selection component has the expected structure."""
    # Verify component ID
    assert module_selection.id == "module-selection"
    
    # Check that the component has a title
    assert module_selection.title == "Pipeline Selection"
    
    # Check that the component has a body
    assert hasattr(module_selection, "children")
    
    # Basic check that children exists and is not empty
    assert module_selection.children is not None
    
    # More general test for checking if component is properly structured
    def has_input_elements(component):
        """Check if component or its children contain input elements."""
        import dash_bootstrap_components as dbc
        from dash import dcc
        
        # Check for various input types
        if (isinstance(component, dbc.RadioItems) or 
            isinstance(component, dcc.RadioItems) or 
            isinstance(component, dbc.Checklist) or 
            isinstance(component, dcc.Checklist) or 
            isinstance(component, dcc.Input)):
            return True
            
        # Check if component has an id with "pipeline-selection"
        if hasattr(component, 'id') and component.id == "pipeline-selection":
            return True
            
        if hasattr(component, 'children') and component.children:
            children = component.children
            if isinstance(children, list):
                for child in children:
                    if has_input_elements(child):
                        return True
            else:
                return has_input_elements(children)
        return False
    
    # Verify that the module selection component contains input elements
    assert has_input_elements(module_selection.children)

def test_header_component():
    """Test that the header component has the expected structure."""
    # Check that the component has content
    assert header is not None
    
    # Check that the header contains navigation links or icons
    from dash import html
    
    def has_links(component):
        """Check if component or its children contain an html.A (link) element."""
        if isinstance(component, html.A):
            return True
            
        if hasattr(component, 'children') and component.children:
            children = component.children
            if isinstance(children, list):
                for child in children:
                    if has_links(child):
                        return True
            else:
                return has_links(children)
        return False
    
    # Verify that the header contains at least one link
    assert has_links(header)