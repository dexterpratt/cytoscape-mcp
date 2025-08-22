# Installation Guide

## Quick Start

### Prerequisites
1. **Cytoscape Desktop 3.8+** - Download from [cytoscape.org](https://cytoscape.org/)
2. **Python 3.8+** - Required for py4cytoscape
3. **MCP Client** - Claude Desktop, Continue, or other MCP-compatible application

### Install the Package
```bash
pip install cytoscape-mcp
```

### Configure Your MCP Client

#### Claude Desktop
Edit your configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

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

#### Other MCP Clients
Use the command: `cytoscape-mcp`

### Test the Installation

1. Start Cytoscape Desktop
2. Start your MCP client (e.g., Claude Desktop)
3. Test connectivity:
   ```
   Can you check if Cytoscape is running?
   ```

## Development Installation

### Clone and Install
```bash
git clone https://github.com/cytoscape/cytoscape-mcp.git
cd cytoscape-mcp
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
```

## Troubleshooting

### Common Issues

**"py4cytoscape not found"**
```bash
pip install py4cytoscape
```

**"Cytoscape not accessible"**
- Ensure Cytoscape Desktop is running
- Check that CyREST is enabled (default)
- Verify port 1234 is not blocked

**"MCP server not found"**
- Check the configuration file path
- Ensure the command path is correct
- Try absolute path: `/full/path/to/cytoscape-mcp`

### Advanced Configuration

**Custom Cytoscape Port:**
Set environment variable before starting:
```bash
export CYTOSCAPE_PORT=1235
cytoscape-mcp
```

**Remote Cytoscape:**
```bash
export CYTOSCAPE_HOST=192.168.1.100
cytoscape-mcp
```

## System Requirements

- **Python:** 3.8 or higher
- **Cytoscape:** 3.8 or higher  
- **Memory:** 4GB+ recommended for large networks
- **Network:** Internet access for STRING/NDEx integration
