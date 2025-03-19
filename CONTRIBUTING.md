# Contributing to wrmXpress-GUI

Thank you for your interest in contributing to wrmXpress-GUI! This document outlines the process for contributing to the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We strive to maintain a welcoming and inclusive environment for all contributors.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a branch for your changes

## Setting Up the Development Environment

We recommend using Conda/Mamba for managing your development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/wrmXpress-gui.git
cd wrmXpress-gui

# Create and activate the environment
conda env create -f mm_wrmxpress_gui.yml
conda activate wrmxpress_gui

# Install testing dependencies
conda install -c conda-forge pytest pytest-cov
```

## Running Tests

We use pytest for testing. You can run the tests with:

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_utils.py
pytest tests/test_components.py

# Run tests with coverage report
pytest --cov=app
```

## Creating a Pull Request

1. Ensure your code follows the project's style and conventions
2. Make sure all tests pass
3. Update the documentation if necessary
4. Push your changes to your fork
5. Submit a pull request to the main repository

Please provide a clear description of your changes in the pull request.

## Writing Tests

When adding new features or fixing bugs, please include tests that verify your changes. We strive for good test coverage to maintain code quality.

## Continuous Integration

All pull requests are automatically tested using GitHub Actions. The CI pipeline runs unit tests and checks code coverage.

## Getting Help

If you have questions or need help, please open an issue on GitHub or reach out to the project maintainers.

Thank you for your contributions!