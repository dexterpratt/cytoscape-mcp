# py4cytoscape Usage Issues and Corrections

This document identifies all issues with py4cytoscape API usage in the codebase and provides corrections.

**Review Date**: 2025-10-30
**Reviewed Version**: server.py (857 lines)
**py4cytoscape Target Version**: 1.12.0+

---

## Critical Issues 🔴

### 1. `string_protein_query` Function Does Not Exist

**Location**: `server.py:676`

**Current Code:**
```python
result = p4c.string_protein_query(
    query=protein_query,
    species=species,
    confidence_score=confidence_score,
    network_type=network_type
)
```

**Issue:**
The function `string_protein_query()` does not exist in py4cytoscape. STRING queries must be executed using the `commands_run()` or `commands_get()` functions with the stringApp command syntax.

**Correct Implementation:**
```python
# Build the STRING protein query command
string_cmd = f'string protein query query="{protein_query}" species={species} cutoff={confidence_score}'

# Execute the command
result = p4c.commands_run(string_cmd)
```

**Alternative Approach:**
```python
# More detailed command with all parameters
parts = [
    'string protein query',
    f'query="{protein_query}"',
    f'species={species}',
    f'cutoff={confidence_score}',
]

# Add network type if specified
if network_type == "physical":
    parts.append('networkType=physical')
elif network_type == "functional":
    parts.append('networkType=full')  # STRING uses 'full' for functional

string_cmd = ' '.join(parts)
result = p4c.commands_run(string_cmd)
```

**Impact**: **CRITICAL** - This function call will fail with `AttributeError: module 'py4cytoscape' has no attribute 'string_protein_query'`

**Status**: ❌ **BROKEN** - Feature will not work at all

---

### 2. Unused Parameter in `_load_network_file`

**Location**: `server.py:522-525`

**Current Code:**
```python
async def _load_network_file(self, file_path: str, first_row_as_column_names: bool = True) -> List[TextContent]:
    """Load network from file"""
    try:
        result = p4c.import_network_from_file(file=file_path)
```

**Issue:**
The `first_row_as_column_names` parameter is accepted but never used. The py4cytoscape `import_network_from_file()` function does NOT accept this parameter - it automatically detects the file format and handles headers appropriately.

**Tool Schema** (lines 116-133):
```python
Tool(
    name="load_network_file",
    ...
    "properties": {
        "file_path": {...},
        "first_row_as_column_names": {  # ← This parameter is advertised
            "type": "boolean",
            "description": "Treat first row as column names",
            "default": True
        }
    }
)
```

**Correct Implementation Option 1** (Remove the parameter):
```python
async def _load_network_file(self, file_path: str) -> List[TextContent]:
    """Load network from file"""
    try:
        result = p4c.import_network_from_file(file=file_path)
        # ... rest of function
```

And update the tool schema:
```python
Tool(
    name="load_network_file",
    description="Load a network from file (SIF, GraphML, XGMML, etc.). File format is auto-detected.",
    inputSchema={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to network file"
            }
        },
        "required": ["file_path"]
    }
)
```

**Correct Implementation Option 2** (Document that it's ignored):
Keep the parameter but document it:
```python
async def _load_network_file(self, file_path: str, first_row_as_column_names: bool = True) -> List[TextContent]:
    """Load network from file

    Note: first_row_as_column_names is accepted for API compatibility but ignored.
    Cytoscape auto-detects file formats and handles headers appropriately.
    """
    # Note: first_row_as_column_names is not used - Cytoscape handles this automatically
    try:
        result = p4c.import_network_from_file(file=file_path)
```

**Impact**: **MODERATE** - Users may expect different behavior. Feature works but parameter is misleading.

**Status**: ⚠️ **MISLEADING** - Works but parameter has no effect

---

### 3. Incorrect Parameter Name for NDEx Export

**Location**: `server.py:722`

**Current Code:**
```python
kwargs = {
    "username": username,
    "password": password,
    "is_public": is_public,  # ← Wrong parameter name
    "ndex_url": ndex_url
}
# ...
ndex_id = p4c.export_network_to_ndex(**kwargs)
```

**Issue:**
The py4cytoscape function `export_network_to_ndex()` uses the parameter name `isPublic` (camelCase), not `is_public` (snake_case).

**Correct Implementation:**
```python
kwargs = {
    "username": username,
    "password": password,
    "isPublic": is_public,  # ← Correct parameter name
    "ndex_url": ndex_url
}
```

**Impact**: **HIGH** - This will cause a TypeError: `export_network_to_ndex() got an unexpected keyword argument 'is_public'`

**Status**: ❌ **BROKEN** - NDEx export will fail

---

### 4. Incorrect Parameter Name for NDEx Update

**Location**: `server.py:770-781`

**Current Code:**
```python
async def _update_network_in_ndex(self, username: str, password: str, is_public: bool = False,
                                network: Optional[Union[str, int]] = None, metadata: Optional[Dict] = None,
                                ndex_url: str = "http://ndexbio.org") -> List[TextContent]:
    """Update existing network in NDEx"""
    try:
        kwargs = {
            "username": username,
            "password": password,
            "is_public": is_public,  # ← Wrong parameter name
            "ndex_url": ndex_url
        }
```

**Issue:**
Same as #3 - should be `isPublic`, not `is_public`.

**Correct Implementation:**
```python
kwargs = {
    "username": username,
    "password": password,
    "isPublic": is_public,  # ← Correct parameter name
    "ndex_url": ndex_url
}
```

**Impact**: **HIGH** - This will cause NDEx update to fail

**Status**: ❌ **BROKEN** - NDEx update will fail

---

## Moderate Issues ⚠️

### 5. Incorrect Parameter Name: `get_network_suid`

**Location**: `server.py:559`

**Current Code:**
```python
info['suid'] = p4c.get_network_suid(title=network) if isinstance(network, str) else network
```

**Issue:**
Checking the py4cytoscape documentation, `get_network_suid()` may not accept a `title` parameter. Need to verify the exact signature.

**Expected Signature:**
```python
get_network_suid(network=None, base_url='http://127.0.0.1:1234/v1')
```

**Correct Implementation:**
```python
info['suid'] = p4c.get_network_suid(network=network) if isinstance(network, str) else network
```

**Impact**: **MODERATE** - May cause failures when looking up networks by name

**Status**: ⚠️ **NEEDS VERIFICATION** - Likely incorrect but needs testing

---

### 6. Incorrect Parameter Name: `get_network_name`

**Location**: `server.py:560`

**Current Code:**
```python
info['name'] = p4c.get_network_name(suid=info['suid'])
```

**Issue:**
Similar to #5, `get_network_name()` likely uses `network` parameter, not `suid`.

**Expected Signature:**
```python
get_network_name(network=None, base_url='http://127.0.0.1:1234/v1')
```

**Correct Implementation:**
```python
info['name'] = p4c.get_network_name(network=info['suid'])
```

**Impact**: **MODERATE** - May cause failures when getting network name

**Status**: ⚠️ **NEEDS VERIFICATION** - Likely incorrect but needs testing

---

### 7. Missing `preserve_current_selection` Parameter

**Location**: `server.py:584`

**Current Code:**
```python
kwargs = {"nodes": nodes, "by_col": by_col}
if network:
    kwargs["network"] = network

result = p4c.select_nodes(**kwargs)
```

**Issue:**
The function signature for `select_nodes()` has a `preserve_current_selection` parameter (default: True). The current implementation doesn't expose this to users, which may cause unexpected behavior if users want to replace the selection instead of adding to it.

**Expected Signature:**
```python
select_nodes(
    nodes,
    by_col='SUID',
    preserve_current_selection=True,  # ← Missing from tool schema
    network=None,
    base_url='http://127.0.0.1:1234/v1'
)
```

**Recommendation:**
Add `preserve_current_selection` to the tool schema and method signature:

```python
# Tool schema (lines 159-181)
Tool(
    name="select_nodes",
    description="Select nodes in the network",
    inputSchema={
        "type": "object",
        "properties": {
            "nodes": {...},
            "by_col": {...},
            "preserve_current_selection": {  # ← Add this
                "type": "boolean",
                "description": "Whether to keep previously selected nodes",
                "default": True
            },
            "network": {...}
        },
        "required": ["nodes"]
    }
)

# Method signature
async def _select_nodes(
    self,
    nodes: List[Union[str, int]],
    by_col: str = "name",
    preserve_current_selection: bool = True,  # ← Add this
    network: Optional[Union[str, int]] = None
) -> List[TextContent]:
    """Select nodes in network"""
    try:
        kwargs = {
            "nodes": nodes,
            "by_col": by_col,
            "preserve_current_selection": preserve_current_selection  # ← Add this
        }
        if network:
            kwargs["network"] = network

        result = p4c.select_nodes(**kwargs)
```

**Impact**: **LOW** - Feature works but users can't clear selections before selecting

**Status**: ⚠️ **INCOMPLETE** - Missing optional functionality

---

## Minor Issues / Improvements 💡

### 8. Default Value for `by_col` Mismatch

**Location**: `server.py:580` and tool schema line 169

**Current Code:**
```python
# Method signature
async def _select_nodes(self, nodes: List[Union[str, int]], by_col: str = "name", ...)

# Tool schema
"by_col": {
    "type": "string",
    "description": "Column name to select by",
    "default": "name"  # ← Documentation says default is "name"
}
```

**Issue:**
The py4cytoscape `select_nodes()` function has a default of `by_col='SUID'`, not `'name'`. While explicitly setting it to `'name'` is valid, this creates a mismatch between the py4cytoscape default and our default.

**Recommendation:**
Consider using `'SUID'` as the default to match py4cytoscape, or clearly document why `'name'` is preferred:

```python
"by_col": {
    "type": "string",
    "description": "Column name to select by (default: 'name' for user-friendly selection; use 'SUID' for precise selection)",
    "default": "name"
}
```

**Impact**: **VERY LOW** - Mostly a documentation concern

**Status**: ✓ **ACCEPTABLE** - Intentional design choice, but should be documented

---

### 9. Missing STRING Command Parameters

**Location**: `server.py:672-681` and tool schema lines 266-295

**Current Implementation:**
```python
# Tool schema only exposes these parameters
"protein_query": {...},
"species": {...},
"confidence_score": {...},
"network_type": {...}
```

**Issue:**
The STRING protein query command supports additional parameters that aren't exposed:
- `limit` - Maximum number of proteins to retrieve
- `additionalNodes` - Number of additional nodes to add
- `cutoff` - Confidence score cutoff (0.0-1.0)
- `taxonID` - Taxonomy ID (alternative to species name)

**Once #1 is fixed**, consider adding these parameters:

```python
Tool(
    name="load_string_network",
    description="Load protein interaction network from STRING database",
    inputSchema={
        "type": "object",
        "properties": {
            "protein_query": {
                "type": "string",
                "description": "Protein names/IDs (comma-separated)"
            },
            "species": {
                "type": "integer",
                "description": "NCBI taxonomy ID (e.g., 9606 for human)",
                "default": 9606
            },
            "confidence_score": {
                "type": "number",
                "description": "Confidence threshold (0.0-1.0)",
                "default": 0.4
            },
            "network_type": {
                "type": "string",
                "description": "STRING network type",
                "enum": ["functional", "physical"],
                "default": "functional"
            },
            "limit": {  # ← Add this
                "type": "integer",
                "description": "Maximum number of proteins to retrieve",
                "default": 10
            }
        },
        "required": ["protein_query"]
    }
)
```

**Impact**: **LOW** - Feature works but lacks advanced options

**Status**: ✓ **ACCEPTABLE** - Enhancement opportunity

---

## Test Issues 🧪

### 10. Test Mocks Don't Match Real Return Values

**Location**: `tests/test_server.py:24,26`

**Current Code:**
```python
create_network_from_data_frames=Mock(return_value=12345),
import_network_from_file=Mock(return_value=12346),
```

**Issue:**
- `create_network_from_data_frames` returns an **int** (network SUID)
- `import_network_from_file` returns a **dict** with structure `{"networks": [suid], "views": [suid]}`

The test for `import_network_from_file` (line 84) expects the wrong return type.

**Correct Mock:**
```python
create_network_from_data_frames=Mock(return_value=12345),  # ✓ Correct - returns int
import_network_from_file=Mock(return_value={"networks": [12346], "views": [12347]}),  # ✓ Correct
```

**Impact**: **MODERATE** - Tests don't catch real bugs

**Status**: ⚠️ **INCORRECT** - Tests give false confidence

---

### 11. Test Assertion on Wrong Parameter

**Location**: `tests/test_server.py:84-86`

**Current Code:**
```python
result = await server._load_network_file(file_path)

assert len(result) == 1
assert "Loaded network from /path/to/network.sif with SUID: 12346" in result[0].text
mock_p4c['import_network_from_file'].assert_called_once_with(
    file=file_path, first_row_as_column_names=True  # ← This parameter doesn't exist!
)
```

**Issue:**
The test expects `first_row_as_column_names` to be passed to py4cytoscape, but this parameter doesn't exist in the real function.

**Correct Test:**
```python
result = await server._load_network_file(file_path)

assert len(result) == 1
assert "Loaded network from /path/to/network.sif with SUID: 12346" in result[0].text
mock_p4c['import_network_from_file'].assert_called_once_with(
    file=file_path  # ← Only this parameter
)
```

**Impact**: **HIGH** - Test will fail when run, giving false negatives

**Status**: ❌ **BROKEN** - Test won't pass

---

## Summary of Issues

| # | Issue | Severity | Status | Location |
|---|-------|----------|--------|----------|
| 1 | `string_protein_query` doesn't exist | 🔴 Critical | ❌ Broken | server.py:676 |
| 2 | Unused `first_row_as_column_names` parameter | ⚠️ Moderate | ⚠️ Misleading | server.py:522 |
| 3 | Wrong NDEx parameter: `is_public` vs `isPublic` | 🔴 Critical | ❌ Broken | server.py:722 |
| 4 | Wrong NDEx update parameter: `is_public` vs `isPublic` | 🔴 Critical | ❌ Broken | server.py:772 |
| 5 | Wrong parameter: `title` vs `network` in `get_network_suid` | ⚠️ Moderate | ⚠️ Needs verification | server.py:559 |
| 6 | Wrong parameter: `suid` vs `network` in `get_network_name` | ⚠️ Moderate | ⚠️ Needs verification | server.py:560 |
| 7 | Missing `preserve_current_selection` parameter | 💡 Minor | ⚠️ Incomplete | server.py:584 |
| 8 | Default `by_col` mismatch with py4cytoscape | 💡 Minor | ✓ Acceptable | server.py:580 |
| 9 | Missing STRING command parameters | 💡 Minor | ✓ Acceptable | server.py:672 |
| 10 | Test mocks don't match real return values | ⚠️ Moderate | ⚠️ Incorrect | tests/test_server.py:26 |
| 11 | Test assertion on non-existent parameter | 🔴 Critical | ❌ Broken | tests/test_server.py:84 |

---

## Priority for Fixes

### Must Fix (Blocking)
1. Issue #1: Implement STRING query via commands_run()
2. Issue #3: Fix NDEx export parameter name
3. Issue #4: Fix NDEx update parameter name
4. Issue #11: Fix test assertion

### Should Fix (Important)
5. Issue #2: Remove or document unused parameter
6. Issue #5-6: Verify and fix get_network_suid/name parameters
7. Issue #10: Fix test mock return values

### Could Fix (Enhancement)
8. Issue #7: Add preserve_current_selection parameter
9. Issue #9: Add additional STRING parameters
10. Issue #8: Document by_col default choice

---

## Verification Checklist

To verify fixes:

1. ✅ Install py4cytoscape 1.12.0+ and inspect actual function signatures:
   ```python
   import py4cytoscape as p4c
   import inspect
   print(inspect.signature(p4c.export_network_to_ndex))
   print(inspect.signature(p4c.get_network_suid))
   ```

2. ✅ Start Cytoscape Desktop and test each function:
   ```python
   # Test STRING query
   result = p4c.commands_run('string protein query query="TP53" species=9606')

   # Test NDEx export
   result = p4c.export_network_to_ndex("user", "pass", isPublic=True)
   ```

3. ✅ Run the test suite after fixes:
   ```bash
   pytest tests/test_server.py -v
   ```

4. ✅ Test end-to-end with MCP client (Claude Desktop)

---

## Additional Notes

### STRING App Requirement
The STRING functionality requires the stringApp to be installed in Cytoscape. This should be documented in:
- README.md prerequisites
- Installation guide
- Tool description for `load_string_network`

### Python vs R Differences
py4cytoscape aims to match RCy3 (R package) but some differences exist. Always verify against py4cytoscape docs, not RCy3 docs.

### Version Compatibility
These issues are based on py4cytoscape 1.12.0+. If using an older version, additional compatibility issues may exist.
