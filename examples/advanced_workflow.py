"""
Example: Advanced Network Analysis Workflow

This example demonstrates a more complex workflow involving
data integration, analysis, and visualization.
"""

import asyncio
from cytoscape_mcp.server import CytoscapeMCPServer


async def pathway_analysis_workflow():
    """Complete pathway analysis workflow"""
    
    server = CytoscapeMCPServer()
    
    print("=== Advanced Pathway Analysis Workflow ===\n")
    
    # 1. Load pathway from STRING
    print("1. Loading cancer pathway proteins from STRING...")
    cancer_proteins = "TP53,MDM2,CDKN1A,ATM,BRCA1,BRCA2,RB1,APC"
    
    try:
        result = await server._load_string_network(
            protein_query=cancer_proteins,
            species=9606,
            confidence_score=0.8,
            network_type="functional"
        )
        print(f"   {result[0].text}\n")
        
        # 2. Apply layout optimized for biological networks
        print("2. Applying organic layout...")
        result = await server._apply_layout("organic")
        print(f"   {result[0].text}\n")
        
        # 3. Get network statistics
        print("3. Getting network information...")
        result = await server._get_network_info()
        print(f"   {result[0].text}\n")
        
        # 4. Focus on core tumor suppressors
        print("4. Selecting key tumor suppressor genes...")
        result = await server._select_nodes(["TP53", "RB1", "APC", "BRCA1"])
        print(f"   {result[0].text}\n")
        
        # 5. Export high-resolution figure
        print("5. Exporting publication-quality figure...")
        result = await server._export_image(
            filename="cancer_pathway.pdf",
            type="PDF",
            resolution=600
        )
        print(f"   {result[0].text}\n")
        
        # 6. Execute clustering analysis (example command)
        print("6. Running network clustering analysis...")
        cluster_command = "cluster mcl network=current"
        result = await server._run_app_command(cluster_command)
        print(f"   {result[0].text}\n")
        
    except Exception as e:
        print(f"   Error in workflow: {e}")
        print("   Make sure Cytoscape is running and connected to the internet.\n")


async def multi_network_comparison():
    """Compare multiple networks side by side"""
    
    server = CytoscapeMCPServer()
    
    print("=== Multi-Network Comparison ===\n")
    
    try:
        # Create first network - cell cycle
        print("1. Creating cell cycle network...")
        cell_cycle_nodes = ["CDK1", "CDK2", "CCNA2", "CCNB1", "RB1", "E2F1"]
        cell_cycle_edges = [
            ["CDK1", "CCNB1", "binds"],
            ["CDK2", "CCNA2", "binds"],
            ["RB1", "E2F1", "inhibits"],
            ["CDK2", "RB1", "phosphorylates"]
        ]
        
        result = await server._create_network(
            nodes=cell_cycle_nodes,
            edges=cell_cycle_edges,
            title="Cell Cycle Network",
            collection="Comparison Study"
        )
        print(f"   {result[0].text}\n")
        
        # Apply layout to first network
        result = await server._apply_layout("hierarchical")
        print(f"   Applied layout to cell cycle network\n")
        
        # Create second network - apoptosis
        print("2. Creating apoptosis network...")
        apoptosis_nodes = ["TP53", "BAX", "BCL2", "CASP3", "CASP9", "APAF1"]
        apoptosis_edges = [
            ["TP53", "BAX", "activates"],
            ["BCL2", "BAX", "inhibits"],
            ["BAX", "CASP9", "activates"],
            ["CASP9", "CASP3", "activates"]
        ]
        
        result = await server._create_network(
            nodes=apoptosis_nodes,
            edges=apoptosis_edges,
            title="Apoptosis Network",
            collection="Comparison Study"
        )
        print(f"   {result[0].text}\n")
        
        # Get list of all networks
        print("3. Listing all networks in session...")
        result = await server._get_network_list()
        print(f"   {result[0].text}\n")
        
    except Exception as e:
        print(f"   Error in comparison: {e}\n")


async def data_integration_example():
    """Integrate external data with network"""
    
    server = CytoscapeMCPServer()
    
    print("=== Data Integration Example ===\n")
    
    try:
        # Create a network with expression data simulation
        print("1. Creating network with simulated expression data...")
        genes = ["EGFR", "ERBB2", "KRAS", "PIK3CA", "AKT1", "MTOR"]
        interactions = [
            ["EGFR", "KRAS", "activates"],
            ["KRAS", "PIK3CA", "activates"],
            ["PIK3CA", "AKT1", "activates"],
            ["AKT1", "MTOR", "activates"],
            ["ERBB2", "PIK3CA", "activates"]
        ]
        
        result = await server._create_network(
            nodes=genes,
            edges=interactions,
            title="Signaling Network with Data",
            collection="Data Integration"
        )
        print(f"   {result[0].text}\n")
        
        # This would typically involve loading data tables
        print("2. In a real workflow, you would:")
        print("   - Load gene expression data tables")
        print("   - Map data to node attributes")
        print("   - Create visual style mappings")
        print("   - Apply color/size mappings based on data\n")
        
        # Apply a layout suitable for data visualization
        print("3. Applying force-directed layout...")
        result = await server._apply_layout("force-directed")
        print(f"   {result[0].text}\n")
        
    except Exception as e:
        print(f"   Error in data integration: {e}\n")


async def run_advanced_examples():
    """Run all advanced examples"""
    try:
        await pathway_analysis_workflow()
        await multi_network_comparison()
        await data_integration_example()
        
        print("=== Advanced Examples Completed ===")
        print("These examples demonstrate complex workflows possible")
        print("with the Cytoscape MCP server.")
        
    except Exception as e:
        print(f"Advanced examples failed: {e}")
        print("Ensure Cytoscape Desktop is running with internet access.")


if __name__ == "__main__":
    asyncio.run(run_advanced_examples())
