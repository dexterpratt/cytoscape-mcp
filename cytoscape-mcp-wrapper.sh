#!/bin/bash
# Wrapper script for cytoscape-mcp with debugging

LOG_FILE="$HOME/cytoscape-mcp-wrapper.log"
echo "$(date): Starting cytoscape-mcp wrapper" >> "$LOG_FILE"
echo "$(date): Original directory: $(pwd)" >> "$LOG_FILE"
echo "$(date): Python path: $PATH" >> "$LOG_FILE"

# Change to project directory to avoid read-only filesystem issues
cd /Users/idekeradmin/Dropbox/GitHub/cytoscape-mcp
echo "$(date): Changed to directory: $(pwd)" >> "$LOG_FILE"

# Set environment variables to prevent py4cytoscape from creating logs in problematic locations
export PY4CYTOSCAPE_DETAIL_LOGGER_DIR="$HOME/.py4cytoscape/logs"
export PY4CYTOSCAPE_SUMMARY_LOGGER_DIR="$HOME/.py4cytoscape/logs"

# Create the log directory if it doesn't exist
mkdir -p "$HOME/.py4cytoscape/logs"

echo "$(date): About to execute: /Users/idekeradmin/Dropbox/GitHub/cytoscape-mcp/.venv/bin/cytoscape-mcp" >> "$LOG_FILE"

# Execute the actual MCP server
/Users/idekeradmin/Dropbox/GitHub/cytoscape-mcp/.venv/bin/cytoscape-mcp 2>&1 | tee -a "$LOG_FILE"

echo "$(date): cytoscape-mcp exited with code $?" >> "$LOG_FILE"