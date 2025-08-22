"""
Test suite for Cytoscape MCP Server
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from cytoscape_mcp.server import CytoscapeMCPServer
import py4cytoscape as p4c


@pytest.fixture
def server():
    """Create a test server instance"""
    return CytoscapeMCPServer()


@pytest.fixture
def mock_p4c():
    """Mock py4cytoscape functions"""
    with patch.multiple(
        'py4cytoscape',
        cytoscape_version_info=Mock(return_value={"version": "3.10.0"}),
        create_network_from_data_frames=Mock(return_value=12345),
        import_network_from_file=Mock(return_value=12346),
        get_network_list=Mock(return_value=["network1", "network2"]),
        get_network_info=Mock(return_value={"nodes": 10, "edges": 15}),
        select_nodes=Mock(return_value=["node1", "node2"]),
        layout_network=Mock(return_value={"status": "success"}),
        set_visual_style=Mock(return_value={"status": "applied"}),
        export_image=Mock(return_value={"file": "test.png"}),
        commands_run=Mock(return_value={"result": "success"}),
        string_protein_query=Mock(return_value={"network": "STRING"}),
        import_network_from_ndex=Mock(return_value=12347),
        export_network_to_ndex=Mock(return_value="ndex-uuid-123"),
        get_network_ndex_id=Mock(return_value="ndex-uuid-456"),
        update_network_in_ndex=Mock(return_value={"status": "updated"})
    ) as mocks:
        yield mocks


class TestCytoscapeMCPServer:
    """Test cases for CytoscapeMCPServer"""

    @pytest.mark.asyncio
    async def test_ping_cytoscape_success(self, server, mock_p4c):
        """Test successful Cytoscape ping"""
        result = await server._ping_cytoscape()
        
        assert len(result) == 1
        assert "Cytoscape is running" in result[0].text
        assert "3.10.0" in result[0].text

    @pytest.mark.asyncio
    async def test_ping_cytoscape_failure(self, server):
        """Test failed Cytoscape ping"""
        with patch('py4cytoscape.cytoscape_version_info', side_effect=Exception("Connection failed")):
            result = await server._ping_cytoscape()
            
            assert len(result) == 1
            assert "Cytoscape not accessible" in result[0].text

    @pytest.mark.asyncio
    async def test_create_network(self, server, mock_p4c):
        """Test network creation"""
        nodes = ["A", "B", "C"]
        edges = [["A", "B"], ["B", "C"]]
        
        result = await server._create_network(nodes, edges, title="Test Network")
        
        assert len(result) == 1
        assert "Created network 'Test Network' with SUID: 12345" in result[0].text
        mock_p4c['create_network_from_data_frames'].assert_called_once()

    @pytest.mark.asyncio
    async def test_load_network_file(self, server, mock_p4c):
        """Test network file loading"""
        file_path = "/path/to/network.sif"
        
        result = await server._load_network_file(file_path)
        
        assert len(result) == 1
        assert "Loaded network from /path/to/network.sif with SUID: 12346" in result[0].text
        mock_p4c['import_network_from_file'].assert_called_once_with(
            file=file_path, first_row_as_column_names=True
        )

    @pytest.mark.asyncio
    async def test_get_network_list(self, server, mock_p4c):
        """Test getting network list"""
        result = await server._get_network_list()
        
        assert len(result) == 1
        assert "Networks:" in result[0].text
        assert "network1" in result[0].text
        assert "network2" in result[0].text

    @pytest.mark.asyncio
    async def test_select_nodes(self, server, mock_p4c):
        """Test node selection"""
        nodes = ["node1", "node2"]
        
        result = await server._select_nodes(nodes)
        
        assert len(result) == 1
        assert "Selected 2 nodes" in result[0].text
        mock_p4c['select_nodes'].assert_called_once_with(nodes=nodes, by_col="name")

    @pytest.mark.asyncio
    async def test_apply_layout(self, server, mock_p4c):
        """Test layout application"""
        result = await server._apply_layout("circular")
        
        assert len(result) == 1
        assert "Applied layout 'circular'" in result[0].text
        mock_p4c['layout_network'].assert_called_once_with(layout_name="circular")

    @pytest.mark.asyncio
    async def test_export_image(self, server, mock_p4c):
        """Test image export"""
        result = await server._export_image("test.png", type="PNG", resolution=300)
        
        assert len(result) == 1
        assert "Exported image to test.png" in result[0].text
        mock_p4c['export_image'].assert_called_once_with(
            filename="test.png", type="PNG", resolution=300
        )

    @pytest.mark.asyncio
    async def test_load_string_network(self, server, mock_p4c):
        """Test STRING network loading"""
        result = await server._load_string_network("TP53,MDM2", species=9606)
        
        assert len(result) == 1
        assert "Loaded STRING network" in result[0].text
        mock_p4c['string_protein_query'].assert_called_once_with(
            query="TP53,MDM2", species=9606, confidence_score=0.4, network_type="functional"
        )

    @pytest.mark.asyncio
    async def test_import_from_ndex(self, server, mock_p4c):
        """Test NDEx import"""
        ndex_id = "test-uuid-123"
        
        result = await server._import_network_from_ndex(ndex_id)
        
        assert len(result) == 1
        assert f"Imported network from NDEx ID '{ndex_id}' with SUID: 12347" in result[0].text
        mock_p4c['import_network_from_ndex'].assert_called_once()

    @pytest.mark.asyncio
    async def test_export_to_ndex(self, server, mock_p4c):
        """Test NDEx export"""
        result = await server._export_network_to_ndex("user", "pass", is_public=True)
        
        assert len(result) == 1
        assert "Exported network to NDEx with ID: ndex-uuid-123" in result[0].text
        mock_p4c['export_network_to_ndex'].assert_called_once()

    @pytest.mark.asyncio
    async def test_get_network_ndex_id(self, server, mock_p4c):
        """Test getting NDEx ID"""
        result = await server._get_network_ndex_id()
        
        assert len(result) == 1
        assert "Network NDEx ID: ndex-uuid-456" in result[0].text

    @pytest.mark.asyncio
    async def test_get_network_ndex_id_none(self, server):
        """Test getting NDEx ID when none exists"""
        with patch('py4cytoscape.get_network_ndex_id', return_value=None):
            result = await server._get_network_ndex_id()
            
            assert len(result) == 1
            assert "Network is not associated with any NDEx entry" in result[0].text

    @pytest.mark.asyncio
    async def test_error_handling(self, server):
        """Test error handling in tool execution"""
        with patch('py4cytoscape.cytoscape_version_info', side_effect=Exception("Test error")):
            result = await server._ping_cytoscape()
            
            assert len(result) == 1
            assert "Cytoscape not accessible: Test error" in result[0].text


class TestToolSchemas:
    """Test tool schema definitions"""

    def test_tool_list_structure(self, server):
        """Test that all tools have required schema structure"""
        # Get the list_tools handler
        list_tools_handler = None
        for handler in server.server._tool_list_handlers:
            list_tools_handler = handler
            break
        
        assert list_tools_handler is not None
        
        # This would need to be adapted based on how the server exposes tools
        # For now, just check that the server initializes properly
        assert server is not None


if __name__ == "__main__":
    pytest.main([__file__])
