"""
Example: Basic Network Creation and Visualization

This example demonstrates creating a simple network, applying layouts,
and exporting visualizations using the Cytoscape MCP server.
"""

import asyncio
import json
from cytoscape_mcp.server import CytoscapeMCPServer


async def basic_network_example():
    """Create and visualize a basic network"""
    
    # Initialize server (normally this would be handled by MCP framework)
    server = CytoscapeMCPServer()
    
    print("=== Basic Network Creation Example ===\n")
    
    # 1. Check Cytoscape connectivity
    print("1. Checking Cytoscape connectivity...")
    result = await server._ping_cytoscape()
    print(f"   {result[0].text}\n")
    
    # 2. Create a simple network
    print("2. Creating a simple network...")
    nodes = ["Gene1", "Gene2", "Gene3", "Gene4"]
    edges = [
        ["Gene1", "Gene2", "activates"],
        ["Gene2", "Gene3", "inhibits"], 
        ["Gene3", "Gene4", "regulates"],
        ["Gene4", "Gene1", "interacts"]
    ]
    
    result = await server._create_network(
        nodes=nodes,
        edges=edges,
        title="Gene Regulatory Network",
        collection="Example Networks"
    )
    print(f"   {result[0].text}\n")
    
    # 3. Apply a layout
    print("3. Applying force-directed layout...")
    result = await server._apply_layout("force-directed")
    print(f"   {result[0].text}\n")
    
    # 4. Export as image
    print("4. Exporting network image...")
    result = await server._export_image(
        filename="gene_network.png",
        type="PNG",
        resolution=300
    )
    print(f"   {result[0].text}\n")
    
    # 5. Get network information
    print("5. Getting network information...")
    result = await server._get_network_info()
    print(f"   Network details: {result[0].text}\n")


async def string_network_example():
    """Load and analyze a protein network from STRING"""
    
    server = CytoscapeMCPServer()
    
    print("=== STRING Network Example ===\n")
    
    # 1. Load protein interaction network from STRING
    print("1. Loading protein network from STRING database...")
    result = await server._load_string_network(
        protein_query="TP53,MDM2,CDKN1A,ATM",
        species=9606,  # Human
        confidence_score=0.7,
        network_type="functional"
    )
    print(f"   {result[0].text}\n")
    
    # 2. Apply biological layout
    print("2. Applying hierarchical layout...")
    result = await server._apply_layout("hierarchical")
    print(f"   {result[0].text}\n")
    
    # 3. Select specific nodes
    print("3. Selecting TP53 and MDM2 nodes...")
    result = await server._select_nodes(["TP53", "MDM2"])
    print(f"   {result[0].text}\n")


async def ndex_workflow_example():
    """Demonstrate NDEx import/export workflow"""
    
    server = CytoscapeMCPServer()
    
    print("=== NDEx Workflow Example ===\n")
    
    # Note: This example uses placeholder credentials
    # In real usage, you would use actual NDEx credentials
    
    print("1. Creating a network for NDEx export...")
    nodes = ["Protein1", "Protein2", "Protein3"]
    edges = [["Protein1", "Protein2"], ["Protein2", "Protein3"]]
    
    result = await server._create_network(
        nodes=nodes,
        edges=edges,
        title="Research Network",
        collection="NDEx Examples"
    )
    print(f"   {result[0].text}\n")
    
    # Commented out to avoid requiring real credentials
    """
    print("2. Exporting network to NDEx...")
    result = await server._export_network_to_ndex(
        username="your_username",
        password="your_password",
        is_public=False,
        metadata={
            "name": "Research Network",
            "description": "Example network for research",
            "version": "1.0",
            "author": "Researcher"
        }
    )
    print(f"   {result[0].text}\n")
    
    print("3. Getting NDEx ID...")
    result = await server._get_network_ndex_id()
    print(f"   {result[0].text}\n")
    """
    
    print("2. For NDEx operations, you would use real credentials like:")
    print("   username='your_ndex_username'")
    print("   password='your_ndex_password'")
    print("   or access_key='your_api_key'\n")


async def file_import_example():
    """Demonstrate importing networks from files"""
    
    server = CytoscapeMCPServer()
    
    print("=== File Import Example ===\n")
    
    print("This example shows how to import network files.")
    print("You would use actual file paths like:")
    print("   /path/to/your/network.sif")
    print("   /path/to/your/network.graphml")
    print("   /path/to/your/network.xgmml\n")
    
    # Example with a hypothetical file
    """
    print("1. Importing SIF file...")
    result = await server._load_network_file(
        file_path="/path/to/network.sif",
        first_row_as_column_names=True
    )
    print(f"   {result[0].text}\n")
    """


async def run_all_examples():
    """Run all examples"""
    try:
        await basic_network_example()
        await string_network_example() 
        await ndex_workflow_example()
        await file_import_example()
        
        print("=== All Examples Completed ===")
        print("Note: Some examples require Cytoscape to be running")
        print("and may need actual file paths or NDEx credentials.")
        
    except Exception as e:
        print(f"Example failed: {e}")
        print("Make sure Cytoscape Desktop is running before executing examples.")


if __name__ == "__main__":
    asyncio.run(run_all_examples())
