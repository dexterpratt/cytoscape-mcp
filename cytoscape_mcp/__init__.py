"""
Cytoscape MCP Server

An MCP (Model Context Protocol) server that provides programmatic control 
over Cytoscape Desktop through py4cytoscape.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .server import CytoscapeMCPServer

__all__ = ["CytoscapeMCPServer"]
