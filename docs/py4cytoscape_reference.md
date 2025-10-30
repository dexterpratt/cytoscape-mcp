# py4cytoscape API Reference

This document contains the complete function signatures and parameters for all py4cytoscape functions used in this project. This serves as a reference for verifying correct API usage.

**py4cytoscape Version**: 1.12.0+
**Documentation**: https://py4cytoscape.readthedocs.io/en/latest/
**GitHub**: https://github.com/cytoscape/py4cytoscape

---

## Table of Contents

1. [Network Management](#network-management)
2. [Network Import/Export](#network-importexport)
3. [Visualization](#visualization)
4. [Layout](#layout)
5. [Selection](#selection)
6. [Commands](#commands)
7. [External Databases](#external-databases)
8. [System Functions](#system-functions)

---

## Network Management

### `create_network_from_data_frames`

Create a network from pandas DataFrames containing node and edge data.

**Function Signature:**
```python
create_network_from_data_frames(
    nodes=None,
    edges=None,
    title='From dataframe',
    collection='My Dataframe Network Collection',
    base_url='http://127.0.0.1:1234/v1',
    *,
    node_id_list='id',
    source_id_list='source',
    target_id_list='target',
    interaction_type_list='interaction'
)
```

**Parameters:**
- `nodes` (DataFrame, optional): DataFrame with node data. Must contain a column specified by `node_id_list`
- `edges` (DataFrame, optional): DataFrame with edge data. Must contain columns specified by `source_id_list`, `target_id_list`, and `interaction_type_list`
- `title` (str): Network title. Default: `'From dataframe'`
- `collection` (str): Collection name. Default: `'My Dataframe Network Collection'`
- `base_url` (str): CyREST API endpoint. Default: `'http://127.0.0.1:1234/v1'`
- `node_id_list` (str): Column name for node IDs. Default: `'id'`
- `source_id_list` (str): Column name for edge source nodes. Default: `'source'`
- `target_id_list` (str): Column name for edge target nodes. Default: `'target'`
- `interaction_type_list` (str): Column name for interaction types. Default: `'interaction'`

**Returns:**
- `int`: Network SUID

**Example:**
```python
import pandas as pd
nodes_df = pd.DataFrame({'id': ['A', 'B', 'C']})
edges_df = pd.DataFrame({
    'source': ['A', 'B'],
    'target': ['B', 'C'],
    'interaction': ['interacts', 'activates']
})
network_suid = p4c.create_network_from_data_frames(nodes=nodes_df, edges=edges_df, title='My Network')
```

### `import_network_from_file`

Load a network from a file in various formats (SIF, GraphML, XGMML, etc).

**Function Signature:**
```python
import_network_from_file(
    file=None,
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- `file` (str): Path to network file. Supported formats: SIF, GML, xGMML, XGMML, etc. If None, loads a demo network
- `base_url` (str): CyREST API endpoint. Default: `'http://127.0.0.1:1234/v1'`

**Returns:**
- `dict`: `{"networks": [network_suid], "views": [view_suid]}`

**Example:**
```python
>>> import_network_from_file()  # import demo network
{'networks': [131481], 'views': [131850]}

>>> import_network_from_file('data/yeastHighQuality.sif')
{'networks': [131481], 'views': [131850]}
```

**Note:** This function does NOT accept a `first_row_as_column_names` parameter. File format handling is automatic.

### `get_network_list`

Get list of all network names in the current session.

**Function Signature:**
```python
get_network_list(base_url='http://127.0.0.1:1234/v1')
```

**Returns:**
- `list`: List of network names

### `get_network_suid`

Get the SUID of a network.

**Function Signature:**
```python
get_network_suid(title=None, base_url='http://127.0.0.1:1234/v1')
```

**Parameters:**
- `title` (str, optional): Network name. If None, returns current network SUID
- `base_url` (str): CyREST API endpoint

**Returns:**
- `int`: Network SUID

### `get_network_name`

Get the name of a network.

**Function Signature:**
```python
get_network_name(suid=None, base_url='http://127.0.0.1:1234/v1')
```

**Parameters:**
- `suid` (int, optional): Network SUID. If None, returns current network name
- `base_url` (str): CyREST API endpoint

**Returns:**
- `str`: Network name

### `get_node_count`

Get the number of nodes in a network.

**Function Signature:**
```python
get_node_count(network=None, base_url='http://127.0.0.1:1234/v1')
```

**Parameters:**
- `network` (str or int, optional): Network name or SUID. If None, uses current network
- `base_url` (str): CyREST API endpoint

**Returns:**
- `int`: Number of nodes

### `get_edge_count`

Get the number of edges in a network.

**Function Signature:**
```python
get_edge_count(network=None, base_url='http://127.0.0.1:1234/v1')
```

**Parameters:**
- `network` (str or int, optional): Network name or SUID. If None, uses current network
- `base_url` (str): CyREST API endpoint

**Returns:**
- `int`: Number of edges

### `get_network_view_suid`

Get the view SUID for a network.

**Function Signature:**
```python
get_network_view_suid(network=None, base_url='http://127.0.0.1:1234/v1')
```

**Parameters:**
- `network` (str or int, optional): Network name or SUID. If None, uses current network
- `base_url` (str): CyREST API endpoint

**Returns:**
- `int`: View SUID

---

## Network Import/Export

### `export_image`

Export the current network view as an image.

**Function Signature (Cytoscape v3.10+):**
```python
export_image(
    filename=None,
    type='PNG',
    resolution=None,
    units=None,
    height=None,
    width=None,
    zoom=None,
    network=None,
    base_url='http://127.0.0.1:1234/v1',
    *,
    overwrite_file=False,
    force_pre_3_10=False,
    all_graphics_details=None,
    hide_labels=None,
    transparent_background=None,
    export_text_as_font=None,
    orientation=None,
    page_size=None
)
```

**Basic Parameters:**
- `filename` (str): Output file path with name. Extension is added automatically based on type. If None, uses current network name
- `type` (str): Image format. Options: `'PNG'` (default), `'JPEG'`, `'PDF'`, `'SVG'`, `'PS'`
- `network` (str or int, optional): Network name or SUID. If None, uses current network
- `base_url` (str): CyREST API endpoint

**Cytoscape v3.10+ Parameters:**
- `overwrite_file` (bool): False shows message before overwriting; True overwrites without asking. Default: False
- `force_pre_3_10` (bool): Use pre-3.10 export functions for backward compatibility. Default: False
- `all_graphics_details` (bool): True for highest detail; False for faster generation. Default: True (for PNG, JPEG)
- `hide_labels` (bool): True makes node/edge labels invisible. Default: None
- `transparent_background` (bool): True for transparent background. Default: False (PNG only)
- `export_text_as_font` (bool): True exports text as fonts. Default: True (PDF, PS, SVG)
- `orientation` (str): `'Portrait'` or `'Landscape'`. Default: `'Portrait'` (PDF only)
- `page_size` (str): Paper size: `'Letter'`, `'Auto'`, `'Legal'`, `'Tabloid'`, `'A0'`-`'A5'`. Default: `'Letter'` (PDF only)
- `zoom` (float): Zoom percentage. Default: 100.0 (bitmap formats)

**Pre-v3.10 Parameters (DEPRECATED):**
- `resolution` (int): DPI for export. Options: 72, 100, 150, 300, 600. Default: 72
- `units` (str): `'pixels'` (default) or `'inches'`
- `height` (float): Image height in specified units
- `width` (float): Image width in specified units

**Returns:**
- `dict`: Export result information

**Important Notes:**
- The function defaults to v3.10+ functionality
- Mixing pre-v3.10 and v3.10 parameters will raise an exception
- Use `force_pre_3_10=True` to explicitly use old behavior

---

## Visualization

### `set_visual_style`

Apply a visual style to a network.

**Function Signature:**
```python
set_visual_style(
    style_name,
    network=None,
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- `style_name` (str): Name of an existing visual style
- `network` (str or int, optional): Network name or SUID. If None, applies to current network
- `base_url` (str): CyREST API endpoint

**Returns:**
- `dict`: `{'message': 'Visual Style applied.'}`

**Example:**
```python
set_visual_style('default')
# {'message': 'Visual Style applied.'}

set_visual_style('galFiltered Style', network=51)
# {'message': 'Visual Style applied.'}
```

---

## Layout

### `layout_network`

Apply a layout algorithm to a network.

**Function Signature:**
```python
layout_network(
    layout_name=None,
    network=None,
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- `layout_name` (str, optional): Name of layout algorithm with optional parameters. If None, applies the preferred layout from Cytoscape UI preferences
- `network` (str or int, optional): Network name or SUID. If None, applies to current network
- `base_url` (str): CyREST API endpoint

**Returns:**
- `dict`: Layout result information

**Common Layout Names:**
- `'force-directed'` - Force-directed/spring-embedded layout
- `'circular'` - Circular layout
- `'hierarchical'` - Hierarchical layout
- `'grid'` - Grid layout
- `'organic'` - Organic layout
- `'kamada-kawai'` - Kamada-Kawai layout

**Example:**
```python
layout_network('force-directed')
layout_network('hierarchical', network='My Network')
```

---

## Selection

### `select_nodes`

Select nodes in a network.

**Function Signature:**
```python
select_nodes(
    nodes,
    by_col='SUID',
    preserve_current_selection=True,
    network=None,
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- `nodes` (str or list or int): Nodes to select. Can be:
  - List of node names or SUIDs
  - Comma-separated string of node names or SUIDs
  - Single node name or SUID
- `by_col` (str): Node table column to use for lookup. Default: `'SUID'`. Common values: `'SUID'`, `'name'`
- `preserve_current_selection` (bool): Whether to keep previously selected nodes. Default: True
- `network` (str or int, optional): Network name or SUID. If None, uses current network
- `base_url` (str): CyREST API endpoint

**Returns:**
- `list`: List of selected node SUIDs

**Example:**
```python
# Select by name
select_nodes(['GeneA', 'GeneB'], by_col='name')

# Select by SUID
select_nodes([1234, 5678], by_col='SUID')

# Replace current selection
select_nodes(['GeneC'], by_col='name', preserve_current_selection=False)
```

---

## Commands

### `commands_run`

Execute a Cytoscape command using the Command Line Dialog syntax.

**Function Signature:**
```python
commands_run(
    cmd_string,
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- `cmd_string` (str): Command string in Cytoscape Command Line syntax
- `base_url` (str): CyREST API endpoint

**Returns:**
- `list`: Lines from command result (omitting the "Finished" line)

**Example:**
```python
# Start a new session
commands_run('session new destroyCurrentSession=true')

# Run clustering
commands_run('cluster mcl network=current')

# Apply a layout
commands_run('layout kamada-kawai network=current')
```

**Note:**
- Uses HTTP GET, which has URI length limitations
- For very long commands, use `commands_post()` instead
- Command syntax follows Cytoscape's Command Line Dialog format

### `commands_post`

Execute a Cytoscape command using HTTP POST (no URI length limits).

**Function Signature:**
```python
commands_post(
    cmd_string,
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- Same as `commands_run()`

**Returns:**
- Different format from `commands_run()` - returns raw response

---

## External Databases

### NDEx Functions

#### `import_network_from_ndex`

Import a network from the NDEx database.

**Function Signature:**
```python
import_network_from_ndex(
    ndex_id,
    username=None,
    password=None,
    access_key=None,
    ndex_url='http://ndexbio.org',
    ndex_version='v2',
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- `ndex_id` (str): NDEx network externalId (NOT the same as Cytoscape SUID)
- `username` (str, optional): NDEx account username (required for private networks)
- `password` (str, optional): NDEx account password (required for private networks)
- `access_key` (str, optional): NDEx access key (alternative to username/password)
- `ndex_url` (str): NDEx website URL. Default: `'http://ndexbio.org'`
- `ndex_version` (str): NDEx API version. Default: `'v2'`
- `base_url` (str): CyREST API endpoint

**Returns:**
- `int`: SUID of imported network

**Example:**
```python
# Import public network
network_suid = import_network_from_ndex('f93f402c-86d4-11e7-a10d-0ac135e8bacf')

# Import private network
network_suid = import_network_from_ndex(
    'uuid-string',
    username='myuser',
    password='mypass'
)
```

#### `export_network_to_ndex`

Export a network to NDEx.

**Function Signature:**
```python
export_network_to_ndex(
    username,
    password,
    isPublic,
    network=None,
    metadata=None,
    ndex_url='http://ndexbio.org',
    ndex_version='v2',
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- `username` (str): NDEx account username
- `password` (str): NDEx account password
- `isPublic` (bool): Whether the network should be publicly accessible
- `network` (str or int, optional): Network name or SUID. If None, exports current network
- `metadata` (dict, optional): Network metadata dictionary
- `ndex_url` (str): NDEx website URL. Default: `'http://ndexbio.org'`
- `ndex_version` (str): NDEx API version. Default: `'v2'`
- `base_url` (str): CyREST API endpoint

**Returns:**
- `str`: NDEx externalId for the newly submitted network

**Metadata Structure:**
```python
metadata = {
    'name': 'Network Name',
    'description': 'Network description',
    'version': '1.0',
    'author': 'Author Name'
}
```

#### `get_network_ndex_id`

Get the NDEx externalId for a Cytoscape network.

**Function Signature:**
```python
get_network_ndex_id(
    network=None,
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- `network` (str or int, optional): Network name or SUID. If None, uses current network
- `base_url` (str): CyREST API endpoint

**Returns:**
- `str` or `None`: NDEx externalId if network is associated with NDEx, None otherwise

#### `update_network_in_ndex`

Update an existing network in NDEx.

**Function Signature:**
```python
update_network_in_ndex(
    username,
    password,
    isPublic,
    network=None,
    metadata=None,
    ndex_url='http://ndexbio.org',
    ndex_version='v2',
    base_url='http://127.0.0.1:1234/v1'
)
```

**Parameters:**
- Same as `export_network_to_ndex()`

**Returns:**
- `dict`: Update result information

**Note:** Network must already be associated with an NDEx entry (i.e., have an NDEx externalId).

### STRING Database

#### `string_protein_query`

**Note:** This is NOT a direct py4cytoscape function. It's a STRING app command executed via `commands_run()`.

**Usage:**
```python
# Build command string
cmd = 'string protein query query="TP53,MDM2" species="Homo sapiens" limit=10'

# Execute via commands_run
result = p4c.commands_run(cmd)
```

**Available STRING Commands:**
- `'protein query'` - Query proteins
- `'compound query'` - Query compounds
- `'disease query'` - Query diseases
- `'pubmed query'` - Query PubMed
- `'add nodes'` - Add nodes to network
- `'expand'` - Expand network
- `'change confidence'` - Change confidence cutoff
- `'make string'` - Make STRING network
- `'stringify'` - Convert network to STRING
- `'retrieve enrichment'` - Get enrichment data
- `'show enrichment'` - Display enrichment
- `'list species'` - List available species

**Common Parameters for STRING Protein Query:**
- `query` - Protein names/IDs (comma-separated)
- `species` - Species name or NCBI taxonomy ID (e.g., "Homo sapiens" or 9606)
- `limit` - Maximum number of interactors
- `cutoff` - Confidence score cutoff (0.0-1.0)
- `networkType` - Network type: "functional" or "physical"

---

## System Functions

### `cytoscape_ping`

Test basic Cytoscape connectivity.

**Function Signature:**
```python
cytoscape_ping(base_url='http://127.0.0.1:1234/v1')
```

**Returns:**
- `str`: "You are connected to Cytoscape!"

### `cytoscape_version_info`

Get Cytoscape version information.

**Function Signature:**
```python
cytoscape_version_info(base_url='http://127.0.0.1:1234/v1')
```

**Returns:**
- `dict`: Dictionary with version information including:
  - `apiVersion` - CyREST API version
  - `cytoscapeVersion` - Cytoscape version

**Example:**
```python
>>> cytoscape_version_info()
{
    'apiVersion': 'v1',
    'cytoscapeVersion': '3.10.0'
}
```

---

## Common Parameter Notes

### `network` Parameter
Most functions accept a `network` parameter that can be:
- `None` - Uses the current/active network in Cytoscape
- `str` - Network name (title)
- `int` - Network SUID

### `base_url` Parameter
All functions accept a `base_url` parameter for the CyREST API endpoint:
- Default: `'http://127.0.0.1:1234/v1'`
- Format: `'http://{host}:{port}/{version}'`
- Only override if using custom Cytoscape configuration

### Return Value Validation
Many py4cytoscape functions return dictionaries or lists. Always validate return values before accessing keys:

```python
result = p4c.import_network_from_file('network.sif')
if result and 'networks' in result and result['networks']:
    network_suid = result['networks'][0]
else:
    # Handle error
    pass
```

---

## Version Compatibility

This reference is based on py4cytoscape v1.12.0. Some functions have evolved over versions:

- **v1.12.0+**: Current stable version with full feature set
- **v1.10.0+**: Added Cytoscape v3.10 export_image enhancements
- **v1.0.0+**: Stable API with consistent naming

Always check the version in use:
```python
import py4cytoscape as p4c
print(p4c.__version__)
```

---

## Additional Resources

- **Official Documentation**: https://py4cytoscape.readthedocs.io/en/latest/
- **GitHub Repository**: https://github.com/cytoscape/py4cytoscape
- **Jupyter Tutorials**: https://github.com/cytoscape/cytoscape-automation
- **Cytoscape Manual**: https://manual.cytoscape.org/
- **CyREST API**: Access at `http://localhost:1234/v1` when Cytoscape is running
