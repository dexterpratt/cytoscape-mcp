# Cytoscape MCP Server

An MCP (Model Context Protocol) server that provides programmatic control over Cytoscape Desktop through py4cytoscape.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This MCP server enables AI assistants to control Cytoscape Desktop, the leading platform for network visualization and analysis. It provides seamless integration between conversational AI and powerful network biology tools through a comprehensive set of MCP tools.

## Features

### Core Network Operations
- **Network Creation**: Build networks from nodes and edges programmatically
- **File Import**: Load networks from various formats (SIF, GraphML, XGMML, etc.)
- **Network Management**: List, inspect, and manipulate network properties

### Visualization & Layout
- **Layout Algorithms**: Apply force-directed, circular, hierarchical layouts
- **Visual Styles**: Control node/edge appearance and styling
- **Image Export**: Generate publication-ready figures (PNG, JPG, PDF, SVG)

### Data Integration
- **STRING Database**: Import protein interaction networks
- **NDEx Integration**: Import/export networks from the Network Data Exchange
- **Custom Commands**: Execute any Cytoscape app command

### Advanced Features
- **Node Selection**: Programmatic selection and filtering
- **Metadata Management**: Rich network annotation for NDEx
- **Session Control**: Manage Cytoscape sessions and collections

## Prerequisites

1. **Cytoscape Desktop** (3.8+): Download from [cytoscape.org](https://cytoscape.org/)
2. **Python** (3.8+): Required for py4cytoscape
3. **MCP Client**: Claude Desktop, Continue, or other MCP-compatible client

## Installation

### Option 1: pip install (recommended)
```bash
pip install cytoscape-mcp
```

### Option 2: Development install
```bash
git clone https://github.com/cytoscape/cytoscape-mcp.git
cd cytoscape-mcp
pip install -e .
```

## Configuration

### Claude Desktop
Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cytoscape": {
      "command": "cytoscape-mcp",
      "args": []
    }
  }
}
```

**Config file locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Other MCP Clients
Use the server executable: `cytoscape-mcp`

## Usage

1. **Start Cytoscape Desktop**
2. **Start your MCP client** (e.g., Claude Desktop)
3. **Begin network analysis**:

```
Can you check if Cytoscape is running?
```

### Example Workflows

**Create and visualize a simple network:**
```
Create a network with nodes A, B, C, D and edges A-B, B-C, C-D, D-A. 
Apply a force-directed layout and export as PNG.
```

**Import protein interactions:**
```
Load a STRING network for proteins TP53, MDM2, CDKN1A with confidence > 0.7. 
Apply the "Biological Process" style and export the result.
```

**Work with NDEx:**
```
Import the network with NDEx ID f93f402c-86d4-11e7-a10d-0ac135e8bacf.
After analysis, export it back to NDEx with updated metadata.
```

## Available Tools

### Network Management
- `cytoscape_ping` - Check connectivity
- `create_network` - Build networks from data
- `load_network_file` - Import network files
- `get_network_list` - List all networks
- `get_network_info` - Network details

### Visualization
- `apply_layout` - Apply layout algorithms
- `set_visual_style` - Control appearance
- `export_image` - Generate images

### Data Sources
- `load_string_network` - STRING database
- `import_network_from_ndex` - NDEx import
- `export_network_to_ndex` - NDEx export
- `get_network_ndex_id` - Check NDEx association
- `update_network_in_ndex` - Update NDEx networks

### Analysis
- `select_nodes` - Node selection
- `run_app_command` - Execute Cytoscape commands

## Development

### Setup Development Environment
```bash
git clone https://github.com/cytoscape/cytoscape-mcp.git
cd cytoscape-mcp
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
```

### Code Formatting
```bash
black cytoscape_mcp/
isort cytoscape_mcp/
flake8 cytoscape_mcp/
```

## Architecture

```
MCP Client ↔ MCP Server ↔ py4cytoscape ↔ Cytoscape Desktop (CyREST API)
```

The server translates MCP tool calls into py4cytoscape function calls, which communicate with Cytoscape via its REST API.

## Troubleshooting

### Connection Issues
- Ensure Cytoscape Desktop is running
- Check that CyREST is enabled (default port 1234)
- Verify firewall isn't blocking localhost connections

### Import Errors
- Confirm py4cytoscape installation: `python -c "import py4cytoscape"`
- Check Python environment matches MCP client
- Try reinstalling: `pip install --upgrade py4cytoscape`

### NDEx Authentication
- Verify NDEx credentials are correct
- Check network permissions for private networks
- Use access keys for API-based authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citations

If you use this software in your research, please cite:

- **Cytoscape**: Shannon et al. (2003) Genome Research 13:2498-2504
- **py4cytoscape**: Demchak et al. (2022) Bioinformatics
- **NDEx**: Pillich et al. (2017) Cell Systems 4:572-586

## Support

- **Issues**: [GitHub Issues](https://github.com/cytoscape/cytoscape-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/cytoscape/cytoscape-mcp/discussions)
- **Cytoscape Help**: [Cytoscape Documentation](https://manual.cytoscape.org/)
