# WrmXpress-GUI Commands and Code Style Guidelines

## Build/Run Commands
- Run development server: `python app.py` or `app.run_server(debug=True, host="0.0.0.0", port=9000)`
- Run production server: `python app.py` (uses waitress with `serve(app.server, host="0.0.0.0", port=9000, threads=16)`)
- Docker build: `docker build --platform=linux/amd64 .`
- Docker run: `docker run -p 9000:9000 <image_id>`

## Test Commands
- Run all tests: `pytest`
- Run specific test file: `pytest tests/test_utils.py`
- Run specific test: `pytest tests/test_utils.py::test_create_df_from_inputs`
- Run with coverage: `pytest --cov=app`
- Generate coverage report: `pytest --cov=app --cov-report=html`

## CI/CD Workflows
- Basic tests: `.github/workflows/python-tests.yml` - Runs component and utility tests
- UI tests: `.github/workflows/ui-tests.yml` - Setup for Selenium-based UI testing
- All PRs should pass tests before merging
- Integration tests require special environment setup (see `tests/test_integration.py`)

## Code Style
- **Imports**: Group standard library, third-party, and local imports separately
- **Naming**: Use snake_case for variables/functions, PascalCase for classes
- **Error handling**: Use specific try/except blocks with meaningful error messages
- **Docstrings**: Simple descriptive comments for functions
- **Callbacks**: Follow Dash callback pattern with appropriate Input/Output/State
- **Components**: Modular design with separate files for UI components

## Module Development
- For adding new modules, follow guidelines in `/app/utils/new_module.md`
- Update module selection in `app/components/module_selection.py`
- Implement logic in `app/utils/callback_functions.py` and `app/utils/background_callback.py`
- Add tests for new functionality in the `tests` directory