# API Reference

## Server Class

### CytoscapeMCPServer

Main server class that handles MCP tool execution.

```python
from cytoscape_mcp.server import CytoscapeMCPServer

server = CytoscapeMCPServer()
await server.run()
```

## Tools

### Network Management

#### cytoscape_ping
Check if Cytoscape is running and accessible.

**Parameters:** None

**Returns:** Cytoscape version information

**Example:**
```
Can you check if Cytoscape is running?
```

#### create_network
Create a new network from nodes and edges.

**Parameters:**
- `nodes` (array): List of node names
- `edges` (array): List of edge tuples [source, target] or [source, target, interaction]
- `title` (string, optional): Network title (default: "New Network")
- `collection` (string, optional): Collection name (default: "My Collection")

**Example:**
```
Create a network with nodes A, B, C and edges A-B, B-C, C-A
```

#### load_network_file
Load a network from file (SIF, GraphML, XGMML, etc.).

**Parameters:**
- `file_path` (string): Path to network file
- `first_row_as_column_names` (boolean, optional): Treat first row as column names (default: true)

#### get_network_list
Get list of all networks in current session.

**Parameters:** None

#### get_network_info
Get detailed information about a network.

**Parameters:**
- `network` (string|integer, optional): Network name, SUID, or current network if not specified

### Visualization

#### apply_layout
Apply a layout algorithm to the network.

**Parameters:**
- `layout_name` (string, optional): Layout algorithm name (default: "force-directed")
- `network` (string|integer, optional): Network name or SUID

**Available layouts:**
- `force-directed`
- `circular` 
- `hierarchical`
- `grid`
- `organic`
- `kamada-kawai`

#### set_visual_style
Apply a visual style to the network.

**Parameters:**
- `style_name` (string): Visual style name
- `network` (string|integer, optional): Network name or SUID

#### export_image
Export network view as image.

**Parameters:**
- `filename` (string): Output filename with extension
- `type` (string, optional): Image format - PNG, JPG, PDF, SVG (default: "PNG")
- `resolution` (integer, optional): Image resolution in DPI (default: 300)
- `network` (string|integer, optional): Network name or SUID

### Data Integration

#### load_string_network
Load protein interaction network from STRING database.

**Parameters:**
- `protein_query` (string): Protein names/IDs (comma-separated)
- `species` (integer, optional): NCBI taxonomy ID (default: 9606 for human)
- `confidence_score` (number, optional): Confidence threshold 0.0-1.0 (default: 0.4)
- `network_type` (string, optional): "functional" or "physical" (default: "functional")

**Example:**
```
Load a STRING network for TP53, MDM2, CDKN1A with confidence > 0.7
```

#### import_network_from_ndex
Import a network from the NDEx database into Cytoscape.

**Parameters:**
- `ndex_id` (string): Network external ID provided by NDEx
- `username` (string, optional): NDEx account username (required for private content)
- `password` (string, optional): NDEx account password (required for private content)
- `access_key` (string, optional): NDEx access key (alternative to username/password)
- `ndex_url` (string, optional): NDEx website URL (default: "http://ndexbio.org")

#### export_network_to_ndex
Export current network to NDEx database.

**Parameters:**
- `username` (string): NDEx account username
- `password` (string): NDEx account password
- `is_public` (boolean, optional): Whether to make network publicly accessible (default: false)
- `network` (string|integer, optional): Network name or SUID
- `metadata` (object, optional): Network metadata
  - `name` (string): Network name
  - `description` (string): Network description
  - `version` (string): Network version
  - `author` (string): Author name
- `ndex_url` (string, optional): NDEx website URL

#### get_network_ndex_id
Get the NDEx external ID for a Cytoscape network.

**Parameters:**
- `network` (string|integer, optional): Network name or SUID

#### update_network_in_ndex
Update an existing network in NDEx.

**Parameters:**
- `username` (string): NDEx account username
- `password` (string): NDEx account password
- `is_public` (boolean, optional): Whether to make network publicly accessible
- `network` (string|integer, optional): Network name or SUID
- `metadata` (object, optional): Updated network metadata
- `ndex_url` (string, optional): NDEx website URL

### Selection & Analysis

#### select_nodes
Select nodes in the network.

**Parameters:**
- `nodes` (array): List of node names or SUIDs to select
- `by_col` (string, optional): Column name to select by (default: "name")
- `network` (string|integer, optional): Network name or SUID

#### run_app_command
Execute a Cytoscape app command.

**Parameters:**
- `command` (string): Command string
- `network` (string|integer, optional): Network context

**Examples:**
- `cluster mcl network=current`
- `analyzer analyze network=current`
- `layout kamada-kawai network=current`

## Error Handling

All tools return error messages in a consistent format:

```json
{
  "type": "text",
  "text": "Error: Connection to Cytoscape failed"
}
```

Common error types:
- Connection errors (Cytoscape not running)
- Authentication errors (invalid NDEx credentials)
- File errors (file not found, invalid format)
- Network errors (invalid network ID)
- Command errors (invalid app command)

## Examples

### Basic Workflow
```python
# Check connection
await call_tool("cytoscape_ping", {})

# Create network
await call_tool("create_network", {
    "nodes": ["A", "B", "C"],
    "edges": [["A", "B"], ["B", "C"]]
})

# Apply layout
await call_tool("apply_layout", {"layout_name": "circular"})

# Export image
await call_tool("export_image", {"filename": "network.png"})
```

### NDEx Integration
```python
# Import from NDEx
await call_tool("import_network_from_ndex", {
    "ndex_id": "uuid-string",
    "username": "user",
    "password": "pass"
})

# Export to NDEx
await call_tool("export_network_to_ndex", {
    "username": "user",
    "password": "pass",
    "is_public": True,
    "metadata": {
        "name": "My Network",
        "description": "Research network"
    }
})
```
