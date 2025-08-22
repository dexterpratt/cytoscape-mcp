#!/usr/bin/env python3
"""
MCP Server for Cytoscape Desktop Control via py4cytoscape

This server provides MCP tools to control Cytoscape desktop application
through the py4cytoscape Python library.
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional, Union
import logging

try:
    import py4cytoscape as p4c
except ImportError:
    print("Error: py4cytoscape not installed. Install with: pip install py4cytoscape", file=sys.stderr)
    sys.exit(1)

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.types as types

# Configure logging
import os
log_file = os.path.join(os.path.expanduser("~"), "cytoscape-mcp.log")

# Only log to file to avoid interfering with MCP JSON protocol over stdio
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a')  # Only file logging
    ]
)
logger = logging.getLogger("cytoscape-mcp")

# Suppress other loggers that might interfere with stdio
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("mcp").setLevel(logging.INFO)

# Force log flushing
for handler in logger.handlers:
    handler.setLevel(logging.DEBUG)
    if hasattr(handler, 'flush'):
        handler.flush()

class CytoscapeMCPServer:
    def __init__(self):
        logger.info("Initializing CytoscapeMCPServer...")
        self.server = Server("cytoscape-mcp")
        logger.info("Server instance created")
        self.setup_handlers()
        logger.info("Handlers setup complete")
        
    def setup_handlers(self):
        """Setup MCP message handlers"""
        logger.debug("Setting up MCP handlers...")
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available Cytoscape tools"""
            return [
                Tool(
                    name="cytoscape_ping",
                    description="Check if Cytoscape is running and accessible",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="create_network",
                    description="Create a new network from nodes and edges",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "nodes": {
                                "type": "array",
                                "description": "List of node names",
                                "items": {"type": "string"}
                            },
                            "edges": {
                                "type": "array", 
                                "description": "List of edge tuples [source, target] or [source, target, interaction]",
                                "items": {
                                    "type": "array",
                                    "minItems": 2,
                                    "maxItems": 3
                                }
                            },
                            "title": {
                                "type": "string",
                                "description": "Network title",
                                "default": "New Network"
                            },
                            "collection": {
                                "type": "string", 
                                "description": "Collection name",
                                "default": "My Collection"
                            }
                        },
                        "required": ["nodes", "edges"]
                    }
                ),
                Tool(
                    name="load_network_file",
                    description="Load a network from file (SIF, GraphML, XGMML, etc.)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to network file"
                            },
                            "first_row_as_column_names": {
                                "type": "boolean",
                                "description": "Treat first row as column names",
                                "default": True
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="get_network_list",
                    description="Get list of all networks in current session",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_network_info",
                    description="Get detailed information about a network",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "network": {
                                "type": ["string", "integer"],
                                "description": "Network name, SUID, or current network if not specified"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="select_nodes",
                    description="Select nodes in the network",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "nodes": {
                                "type": "array",
                                "description": "List of node names or SUIDs to select",
                                "items": {"type": ["string", "integer"]}
                            },
                            "by_col": {
                                "type": "string",
                                "description": "Column name to select by",
                                "default": "name"
                            },
                            "network": {
                                "type": ["string", "integer"],
                                "description": "Network name or SUID"
                            }
                        },
                        "required": ["nodes"]
                    }
                ),
                Tool(
                    name="apply_layout",
                    description="Apply a layout algorithm to the network",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "layout_name": {
                                "type": "string",
                                "description": "Layout algorithm name (e.g., 'force-directed', 'circular', 'hierarchical')",
                                "default": "force-directed"
                            },
                            "network": {
                                "type": ["string", "integer"], 
                                "description": "Network name or SUID"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="set_visual_style",
                    description="Apply a visual style to the network",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "style_name": {
                                "type": "string",
                                "description": "Visual style name"
                            },
                            "network": {
                                "type": ["string", "integer"],
                                "description": "Network name or SUID" 
                            }
                        },
                        "required": ["style_name"]
                    }
                ),
                Tool(
                    name="export_image",
                    description="Export network view as image",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string", 
                                "description": "Output filename with extension (PNG, JPG, PDF, SVG)"
                            },
                            "type": {
                                "type": "string",
                                "description": "Image format",
                                "enum": ["PNG", "JPG", "PDF", "SVG"],
                                "default": "PNG"
                            },
                            "resolution": {
                                "type": "integer",
                                "description": "Image resolution (DPI)",
                                "default": 300
                            },
                            "network": {
                                "type": ["string", "integer"],
                                "description": "Network name or SUID"
                            }
                        },
                        "required": ["filename"]
                    }
                ),
                Tool(
                    name="run_app_command", 
                    description="Execute a Cytoscape app command",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Command string"
                            },
                            "network": {
                                "type": ["string", "integer"],
                                "description": "Network context"
                            }
                        },
                        "required": ["command"]
                    }
                ),
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
                            }
                        },
                        "required": ["protein_query"]
                    }
                ),
                Tool(
                    name="import_network_from_ndex",
                    description="Import a network from the NDEx database into Cytoscape",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ndex_id": {
                                "type": "string",
                                "description": "Network external ID provided by NDEx (not Cytoscape SUID)"
                            },
                            "username": {
                                "type": "string",
                                "description": "NDEx account username (required for private content)"
                            },
                            "password": {
                                "type": "string",
                                "description": "NDEx account password (required for private content)"
                            },
                            "access_key": {
                                "type": "string",
                                "description": "NDEx access key (alternative to username/password)"
                            },
                            "ndex_url": {
                                "type": "string",
                                "description": "NDEx website URL",
                                "default": "http://ndexbio.org"
                            }
                        },
                        "required": ["ndex_id"]
                    }
                ),
                Tool(
                    name="export_network_to_ndex",
                    description="Export current network to NDEx database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "NDEx account username"
                            },
                            "password": {
                                "type": "string",
                                "description": "NDEx account password"
                            },
                            "is_public": {
                                "type": "boolean",
                                "description": "Whether to make the network publicly accessible",
                                "default": False
                            },
                            "network": {
                                "type": ["string", "integer"],
                                "description": "Network name or SUID (current network if not specified)"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Network metadata (name, description, version, etc.)",
                                "properties": {
                                    "name": {"type": "string", "description": "Network name"},
                                    "description": {"type": "string", "description": "Network description"},
                                    "version": {"type": "string", "description": "Network version"},
                                    "author": {"type": "string", "description": "Author name"}
                                }
                            },
                            "ndex_url": {
                                "type": "string",
                                "description": "NDEx website URL",
                                "default": "http://ndexbio.org"
                            }
                        },
                        "required": ["username", "password"]
                    }
                ),
                Tool(
                    name="get_network_ndex_id",
                    description="Get the NDEx external ID for a Cytoscape network",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "network": {
                                "type": ["string", "integer"],
                                "description": "Network name or SUID (current network if not specified)"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="update_network_in_ndex",
                    description="Update an existing network in NDEx",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "NDEx account username"
                            },
                            "password": {
                                "type": "string",
                                "description": "NDEx account password"
                            },
                            "is_public": {
                                "type": "boolean",
                                "description": "Whether to make the network publicly accessible",
                                "default": False
                            },
                            "network": {
                                "type": ["string", "integer"],
                                "description": "Network name or SUID (current network if not specified)"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Updated network metadata",
                                "properties": {
                                    "name": {"type": "string", "description": "Network name"},
                                    "description": {"type": "string", "description": "Network description"},
                                    "version": {"type": "string", "description": "Network version"},
                                    "author": {"type": "string", "description": "Author name"}
                                }
                            },
                            "ndex_url": {
                                "type": "string",
                                "description": "NDEx website URL",
                                "default": "http://ndexbio.org"
                            }
                        },
                        "required": ["username", "password"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Handle tool execution"""
            logger.debug(f"Received tool call: {name} with arguments: {arguments}")
            try:
                if name == "cytoscape_ping":
                    return await self._ping_cytoscape()
                elif name == "create_network":
                    return await self._create_network(**arguments)
                elif name == "load_network_file":
                    return await self._load_network_file(**arguments)
                elif name == "get_network_list":
                    return await self._get_network_list()
                elif name == "get_network_info":
                    return await self._get_network_info(**arguments)
                elif name == "select_nodes":
                    return await self._select_nodes(**arguments)
                elif name == "apply_layout":
                    return await self._apply_layout(**arguments)
                elif name == "set_visual_style":
                    return await self._set_visual_style(**arguments)
                elif name == "export_image":
                    return await self._export_image(**arguments)
                elif name == "run_app_command":
                    return await self._run_app_command(**arguments)
                elif name == "load_string_network":
                    return await self._load_string_network(**arguments)
                elif name == "import_network_from_ndex":
                    return await self._import_network_from_ndex(**arguments)
                elif name == "export_network_to_ndex":
                    return await self._export_network_to_ndex(**arguments)
                elif name == "get_network_ndex_id":
                    return await self._get_network_ndex_id(**arguments)
                elif name == "update_network_in_ndex":
                    return await self._update_network_in_ndex(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                logger.error(f"Error executing tool {name}: {str(e)}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def _ping_cytoscape(self) -> List[TextContent]:
        """Check Cytoscape connectivity"""
        try:
            version_info = p4c.cytoscape_version_info()
            return [TextContent(
                type="text", 
                text=f"Cytoscape is running. Version info: {json.dumps(version_info, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Cytoscape not accessible: {str(e)}"
            )]

    async def _create_network(self, nodes: List[str], edges: List[List], 
                            title: str = "New Network", collection: str = "My Collection") -> List[TextContent]:
        """Create a new network"""
        try:
            import pandas as pd
            
            # Format edges for py4cytoscape
            formatted_edges = []
            for edge in edges:
                if len(edge) == 2:
                    formatted_edges.append([edge[0], edge[1], "interacts"])
                else:
                    formatted_edges.append(edge)
            
            # Create proper pandas DataFrames
            nodes_df = pd.DataFrame({'id': nodes})
            edges_df = pd.DataFrame({
                'source': [e[0] for e in formatted_edges],
                'target': [e[1] for e in formatted_edges], 
                'interaction': [e[2] for e in formatted_edges]
            })
            
            network_suid = p4c.create_network_from_data_frames(
                nodes=nodes_df,
                edges=edges_df,
                title=title,
                collection=collection
            )
            
            return [TextContent(
                type="text",
                text=f"Created network '{title}' with SUID: {network_suid}"
            )]
        except Exception as e:
            return [TextContent(
                type="text", 
                text=f"Failed to create network: {str(e)}"
            )]

    async def _load_network_file(self, file_path: str, first_row_as_column_names: bool = True) -> List[TextContent]:
        """Load network from file"""
        try:
            result = p4c.import_network_from_file(file=file_path)
            network_suid = result['networks'][0] if result and 'networks' in result and result['networks'] else None
            
            return [TextContent(
                type="text",
                text=f"Loaded network from {file_path} with SUID: {network_suid}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to load network file: {str(e)}"
            )]

    async def _get_network_list(self) -> List[TextContent]:
        """Get list of networks"""
        try:
            networks = p4c.get_network_list()
            return [TextContent(
                type="text",
                text=f"Networks: {json.dumps(networks, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to get network list: {str(e)}"
            )]

    async def _get_network_info(self, network: Optional[Union[str, int]] = None) -> List[TextContent]:
        """Get network information"""
        try:
            # Gather network information using available py4cytoscape functions
            info = {}
            
            if network:
                info['suid'] = p4c.get_network_suid(title=network) if isinstance(network, str) else network
                info['name'] = p4c.get_network_name(suid=info['suid'])
            else:
                # Get current network info
                info['suid'] = p4c.get_network_suid()
                info['name'] = p4c.get_network_name()
            
            info['node_count'] = p4c.get_node_count(network=info['suid'])
            info['edge_count'] = p4c.get_edge_count(network=info['suid'])
            info['view_suid'] = p4c.get_network_view_suid(network=info['suid'])
            
            return [TextContent(
                type="text", 
                text=f"Network info: {json.dumps(info, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to get network info: {str(e)}"
            )]

    async def _select_nodes(self, nodes: List[Union[str, int]], by_col: str = "name",
                          network: Optional[Union[str, int]] = None) -> List[TextContent]:
        """Select nodes in network"""
        try:
            kwargs = {"nodes": nodes, "by_col": by_col}
            if network:
                kwargs["network"] = network
                
            result = p4c.select_nodes(**kwargs)
            return [TextContent(
                type="text",
                text=f"Selected {len(result)} nodes: {result}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to select nodes: {str(e)}"
            )]

    async def _apply_layout(self, layout_name: str = "force-directed", 
                          network: Optional[Union[str, int]] = None) -> List[TextContent]:
        """Apply layout to network"""
        try:
            kwargs = {"layout_name": layout_name}
            if network:
                kwargs["network"] = network
                
            result = p4c.layout_network(**kwargs)
            return [TextContent(
                type="text",
                text=f"Applied layout '{layout_name}': {result}"
            )]
        except Exception as e:
            return [TextContent(
                type="text", 
                text=f"Failed to apply layout: {str(e)}"
            )]

    async def _set_visual_style(self, style_name: str, 
                              network: Optional[Union[str, int]] = None) -> List[TextContent]:
        """Set visual style"""
        try:
            kwargs = {"style_name": style_name}
            if network:
                kwargs["network"] = network
                
            result = p4c.set_visual_style(**kwargs)
            return [TextContent(
                type="text",
                text=f"Applied visual style '{style_name}': {result}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to set visual style: {str(e)}"
            )]

    async def _export_image(self, filename: str, type: str = "PNG", resolution: int = 300,
                          network: Optional[Union[str, int]] = None) -> List[TextContent]:
        """Export network image"""
        try:
            kwargs = {"filename": filename, "type": type, "resolution": resolution}
            if network:
                kwargs["network"] = network
                
            result = p4c.export_image(**kwargs)
            return [TextContent(
                type="text", 
                text=f"Exported image to {filename}: {result}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to export image: {str(e)}"
            )]

    async def _run_app_command(self, command: str, 
                             network: Optional[Union[str, int]] = None) -> List[TextContent]:
        """Run app command"""
        try:
            # Note: py4cytoscape commands_run doesn't take network parameter, it's in the command string
            result = p4c.commands_run(cmd_string=command)
            return [TextContent(
                type="text",
                text=f"Command result: {json.dumps(result, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to run command: {str(e)}"
            )]

    async def _load_string_network(self, protein_query: str, species: int = 9606,
                                 confidence_score: float = 0.4, network_type: str = "functional") -> List[TextContent]:
        """Load STRING protein network"""
        try:
            result = p4c.string_protein_query(
                query=protein_query,
                species=species,
                confidence_score=confidence_score,
                network_type=network_type
            )
            return [TextContent(
                type="text",
                text=f"Loaded STRING network: {json.dumps(result, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to load STRING network: {str(e)}"
            )]

    async def _import_network_from_ndex(self, ndex_id: str, username: Optional[str] = None,
                                      password: Optional[str] = None, access_key: Optional[str] = None,
                                      ndex_url: str = "http://ndexbio.org") -> List[TextContent]:
        """Import network from NDEx"""
        try:
            kwargs = {"ndex_id": ndex_id, "ndex_url": ndex_url}
            if username and password:
                kwargs.update({"username": username, "password": password})
            elif access_key:
                kwargs["access_key"] = access_key
                
            network_suid = p4c.import_network_from_ndex(**kwargs)
            return [TextContent(
                type="text",
                text=f"Imported network from NDEx ID '{ndex_id}' with SUID: {network_suid}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to import from NDEx: {str(e)}"
            )]

    async def _export_network_to_ndex(self, username: str, password: str, is_public: bool = False,
                                    network: Optional[Union[str, int]] = None, metadata: Optional[Dict] = None,
                                    ndex_url: str = "http://ndexbio.org") -> List[TextContent]:
        """Export network to NDEx"""
        try:
            kwargs = {
                "username": username,
                "password": password, 
                "is_public": is_public,
                "ndex_url": ndex_url
            }
            if network:
                kwargs["network"] = network
            if metadata:
                kwargs["metadata"] = metadata
                
            ndex_id = p4c.export_network_to_ndex(**kwargs)
            return [TextContent(
                type="text",
                text=f"Exported network to NDEx with ID: {ndex_id}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to export to NDEx: {str(e)}"
            )]

    async def _get_network_ndex_id(self, network: Optional[Union[str, int]] = None) -> List[TextContent]:
        """Get network NDEx ID"""
        try:
            kwargs = {}
            if network:
                kwargs["network"] = network
                
            ndex_id = p4c.get_network_ndex_id(**kwargs)
            if ndex_id:
                return [TextContent(
                    type="text",
                    text=f"Network NDEx ID: {ndex_id}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="Network is not associated with any NDEx entry"
                )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to get NDEx ID: {str(e)}"
            )]

    async def _update_network_in_ndex(self, username: str, password: str, is_public: bool = False,
                                    network: Optional[Union[str, int]] = None, metadata: Optional[Dict] = None,
                                    ndex_url: str = "http://ndexbio.org") -> List[TextContent]:
        """Update existing network in NDEx"""
        try:
            kwargs = {
                "username": username,
                "password": password,
                "is_public": is_public,
                "ndex_url": ndex_url
            }
            if network:
                kwargs["network"] = network
            if metadata:
                kwargs["metadata"] = metadata
                
            result = p4c.update_network_in_ndex(**kwargs)
            return [TextContent(
                type="text",
                text=f"Updated network in NDEx: {json.dumps(result, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to update network in NDEx: {str(e)}"
            )]

    async def run(self):
        """Run the MCP server"""
        from mcp.server.stdio import stdio_server
        
        logger.info("Setting up stdio server...")
        try:
            async with stdio_server() as (read_stream, write_stream):
                logger.info("Stdio server established, starting MCP server...")
                logger.debug("About to call server.run()")
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="cytoscape-mcp",
                        server_version="0.1.0",
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={}
                        )
                    )
                )
                logger.info("MCP server run completed")
        except Exception as e:
            logger.error(f"Error in server run: {e}")
            logger.error("Stack trace:", exc_info=True)
            raise

def main():
    """Main entry point"""
    try:
        logger.info("Starting Cytoscape MCP Server...")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"py4cytoscape version: {p4c.__version__ if hasattr(p4c, '__version__') else 'unknown'}")
        
        # Test Cytoscape connection at startup
        try:
            result = p4c.cytoscape_ping()
            logger.info(f"Cytoscape connection test successful: {result}")
        except Exception as e:
            logger.warning(f"Cytoscape connection test failed: {e}")
            logger.warning("Make sure Cytoscape Desktop is running")
        
        server = CytoscapeMCPServer()
        logger.info("Server initialized, starting event loop...")
        
        # Flush logs before starting server
        for handler in logger.handlers:
            if hasattr(handler, 'flush'):
                handler.flush()
        
        asyncio.run(server.run())
        logger.info("Server exited normally")
        
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        logger.error("Stack trace:", exc_info=True)
        # Flush logs before exiting
        for handler in logger.handlers:
            if hasattr(handler, 'flush'):
                handler.flush()
        sys.exit(1)

if __name__ == "__main__":
    main()
