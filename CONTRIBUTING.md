# Contributing to Cytoscape MCP

We welcome contributions to the Cytoscape MCP server! This guide will help you get started.

## Development Setup

### Prerequisites
- Python 3.8+
- Cytoscape Desktop 3.8+
- Git

### Setting Up Your Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/cytoscape-mcp.git
   cd cytoscape-mcp
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Code Style
We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting  
- **flake8** for linting
- **mypy** for type checking

Run all checks:
```bash
black cytoscape_mcp/
isort cytoscape_mcp/
flake8 cytoscape_mcp/
mypy cytoscape_mcp/
```

### Testing

#### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cytoscape_mcp

# Run specific test file
pytest tests/test_server.py

# Run tests with verbose output
pytest -v
```

#### Writing Tests
- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Mock external dependencies (Cytoscape, NDEx)
- Test both success and error cases

Example test:
```python
@pytest.mark.asyncio
async def test_create_network_success(server, mock_p4c):
    """Test successful network creation"""
    nodes = ["A", "B", "C"]
    edges = [["A", "B"], ["B", "C"]]
    
    result = await server._create_network(nodes, edges)
    
    assert len(result) == 1
    assert "Created network" in result[0].text
```

### Adding New Features

#### New MCP Tools
1. **Define the tool schema** in `setup_handlers()`
2. **Implement the handler method** (e.g., `_new_tool_name()`)
3. **Add error handling** and logging
4. **Write comprehensive tests**
5. **Update documentation**

Example tool implementation:
```python
Tool(
    name="new_tool",
    description="Description of what the tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param1"]
    }
)
```

#### New py4cytoscape Integration
1. **Check py4cytoscape documentation** for the function
2. **Implement wrapper method** with proper error handling
3. **Add parameter validation**
4. **Write tests with mocked py4cytoscape calls**
5. **Update API documentation**

### Documentation

#### Types of Documentation
- **README.md** - Overview and quick start
- **docs/installation.md** - Detailed installation guide
- **docs/api.md** - Complete API reference
- **examples/** - Working code examples
- **Docstrings** - Inline code documentation

#### Writing Good Documentation
- Use clear, concise language
- Provide working examples
- Include error handling information
- Update when adding features

### Submitting Changes

#### Before Submitting
1. **Run the full test suite**
   ```bash
   pytest
   ```

2. **Check code style**
   ```bash
   black --check cytoscape_mcp/
   isort --check-only cytoscape_mcp/
   flake8 cytoscape_mcp/
   ```

3. **Update documentation** if needed

4. **Add changelog entry** if applicable

#### Pull Request Process
1. **Create a feature branch**
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Make your changes** with clear, atomic commits

3. **Write descriptive commit messages**
   ```
   Add support for network clustering analysis
   
   - Implement cluster_network tool
   - Add MCL and MCODE algorithm support
   - Include comprehensive tests
   - Update API documentation
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/new-feature-name
   ```

5. **Create a pull request** with:
   - Clear description of changes
   - Link to any related issues
   - Screenshots if applicable
   - Testing instructions

## Issue Guidelines

### Reporting Bugs
Include:
- **Environment details** (OS, Python version, Cytoscape version)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and logs
- **Minimal example** if possible

### Feature Requests
Include:
- **Use case description**
- **Proposed solution** or API
- **Alternative approaches** considered
- **Examples** of how it would be used

### Questions and Support
- Check existing issues and documentation first
- Use GitHub Discussions for questions
- Provide context and what you've tried

## Code Review Guidelines

### For Authors
- Keep changes focused and atomic
- Write clear descriptions
- Respond to feedback promptly
- Be open to suggestions

### For Reviewers
- Be constructive and helpful
- Focus on code quality and maintainability
- Test the changes if possible
- Suggest improvements, don't just point out problems

## Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

### Release Checklist
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release branch
4. Run full test suite
5. Create GitHub release
6. Publish to PyPI

## Community

### Communication
- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - Questions and general discussion
- **Pull Requests** - Code contributions

### Code of Conduct
We follow the [Contributor Covenant](https://www.contributor-covenant.org/). 
Be respectful, inclusive, and professional in all interactions.

## Getting Help

If you need help contributing:
1. Check this guide and existing documentation
2. Look at existing code for examples
3. Ask questions in GitHub Discussions
4. Review existing issues and pull requests

Thank you for contributing to Cytoscape MCP!
