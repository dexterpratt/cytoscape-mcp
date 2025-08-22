#!/usr/bin/env python3
"""
Simple test script to verify Cytoscape connection and create a basic network
"""

import sys
import traceback

try:
    import py4cytoscape as p4c
    print("✓ py4cytoscape imported successfully")
except ImportError as e:
    print(f"✗ Failed to import py4cytoscape: {e}")
    sys.exit(1)

def test_cytoscape_connection():
    """Test basic Cytoscape connection"""
    try:
        # Test ping/connection
        result = p4c.cytoscape_ping()
        print(f"✓ Cytoscape ping successful: {result}")
        return True
    except Exception as e:
        print(f"✗ Cytoscape ping failed: {e}")
        print("Make sure Cytoscape Desktop is running")
        return False

def test_create_network():
    """Test creating a simple network with 2 nodes and 1 edge"""
    try:
        import pandas as pd
        
        # Create nodes and edges data
        nodes_data = pd.DataFrame({'id': ['Node1', 'Node2']})
        edges_data = pd.DataFrame({
            'source': ['Node1'], 
            'target': ['Node2'], 
            'interaction': ['interacts']
        })
        
        print(f"Creating network with nodes: {nodes_data['id'].tolist()}")
        print(f"Creating network with edges: {edges_data.to_dict('records')}")
        
        # Create network
        network_suid = p4c.create_network_from_data_frames(
            nodes=nodes_data,
            edges=edges_data,
            title="Test Network",
            collection="Test Collection"
        )
        
        print(f"✓ Network created successfully with SUID: {network_suid}")
        
        # Get network info
        network_list = p4c.get_network_list()
        print(f"✓ Network list: {network_list}")
        
        # Get node count
        node_count = p4c.get_node_count()
        edge_count = p4c.get_edge_count()
        print(f"✓ Network has {node_count} nodes and {edge_count} edges")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to create network: {e}")
        traceback.print_exc()
        return False

def main():
    print("Testing Cytoscape MCP functionality...")
    print("-" * 40)
    
    # Test connection first
    if not test_cytoscape_connection():
        return False
    
    # Test network creation
    if not test_create_network():
        return False
    
    print("-" * 40)
    print("✓ All tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)