"""
Test fixtures and utilities for Cytoscape MCP tests
"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_network_file():
    """Create a temporary SIF network file for testing"""
    content = """A\tinteracts\tB
B\tinteracts\tC
C\tinteracts\tA
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sif', delete=False) as f:
        f.write(content)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def temp_directory():
    """Create a temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_network_data():
    """Sample network data for testing"""
    return {
        "nodes": ["A", "B", "C", "D"],
        "edges": [
            ["A", "B", "interacts"],
            ["B", "C", "activates"], 
            ["C", "D", "inhibits"],
            ["D", "A", "regulates"]
        ]
    }


@pytest.fixture
def sample_metadata():
    """Sample metadata for NDEx testing"""
    return {
        "name": "Test Network",
        "description": "A test network for unit testing",
        "version": "1.0",
        "author": "Test Author"
    }
