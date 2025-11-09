"""
Tests for the MCP tool generator
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from mcp_extend.generator import ToolGenerator


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def generator():
    return ToolGenerator()


def test_generate_basic_tool(generator, temp_output_dir):
    """Test generating a basic function tool"""
    result = generator.generate_tool(
        tool_name="test-calculator",
        description="Test calculator tool",
        template_type="basic_function",
        output_dir=temp_output_dir
    )
    
    assert result["status"] == "success"
    assert "test-calculator" in result["path"]
    
    # Check files were created
    tool_path = Path(result["path"])
    assert (tool_path / "server.py").exists()
    assert (tool_path / "pyproject.toml").exists()
    assert (tool_path / "README.md").exists()
    assert (tool_path / ".gitignore").exists()
    
    # Check server.py contains expected content
    server_content = (tool_path / "server.py").read_text()
    assert "FastMCP" in server_content
    assert "def add" in server_content
    assert "def multiply" in server_content


def test_generate_http_api_tool(generator, temp_output_dir):
    """Test generating an HTTP API tool (works for both external and internal APIs)"""
    result = generator.generate_tool(
        tool_name="api-tool",
        description="HTTP API wrapper",
        template_type="http_api",
        output_dir=temp_output_dir
    )
    
    assert result["status"] == "success"
    
    # Verify server.py contains expected content
    server_content = (Path(result["path"]) / "server.py").read_text()
    assert "httpx" in server_content
    assert "async" in server_content
    assert "query_api" in server_content  # Generic function
    assert "get_weather" in server_content  # Working example
    assert "API_BASE_URL" in server_content  # Configuration
    assert "API_TOKEN" in server_content  # Auth support


def test_generate_file_ops_tool(generator, temp_output_dir):
    """Test generating a file operations tool"""
    result = generator.generate_tool(
        tool_name="file-search",
        description="File search utilities",
        template_type="file_operations",
        output_dir=temp_output_dir
    )
    
    assert result["status"] == "success"
    
    # Verify server.py contains file ops code
    server_content = (Path(result["path"]) / "server.py").read_text()
    assert "Path" in server_content
    assert "search_files" in server_content
    assert "read_file_content" in server_content


def test_generated_tool_is_valid_python(generator, temp_output_dir):
    """Test that generated Python code is syntactically valid"""
    result = generator.generate_tool(
        tool_name="test-tool",
        description="Test",
        template_type="basic_function",
        output_dir=temp_output_dir
    )
    
    server_file = Path(result["path"]) / "server.py"
    
    # Try to compile the generated Python code
    import py_compile
    try:
        py_compile.compile(str(server_file), doraise=True)
    except py_compile.PyCompileError as e:
        pytest.fail(f"Generated Python code is invalid: {e}")


def test_tool_name_sanitization(generator, temp_output_dir):
    """Test that tool names with spaces/special chars are handled"""
    result = generator.generate_tool(
        tool_name="My Cool Tool!!!",
        description="Test",
        template_type="basic_function",
        output_dir=temp_output_dir
    )
    
    assert result["status"] == "success"
    # Should create a valid directory name
    assert Path(result["path"]).exists()
    assert "my-cool-tool" in result["path"].lower()


def test_get_mcp_tool_guide(temp_output_dir):
    """Test the get_mcp_tool_guide function"""
    from mcp_extend.server import _get_mcp_tool_guide_impl
    
    result = _get_mcp_tool_guide_impl(
        tool_type="http_api",
        user_requirements="Query weather API",
        tool_name="weather-tool",
        output_path=temp_output_dir
    )
    
    assert result["status"] == "success"
    assert result["tool_name"] == "weather-tool"
    assert result["tool_type"] == "http_api"
    assert "project_structure" in result
    assert "reference_implementation" in result
    assert "patterns" in result
    assert "best_practices" in result
    assert "next_steps" in result
    
    # Check reference code is included
    assert "server.py" in result["reference_implementation"]
    assert "pyproject.toml" in result["reference_implementation"]
    assert "fastmcp" in result["reference_implementation"]["server.py"].lower()


def test_validate_mcp_tool(generator, temp_output_dir):
    """Test the validate_mcp_tool function"""
    from mcp_extend.server import _validate_mcp_tool_impl
    
    # Generate a tool first
    result = generator.generate_tool(
        tool_name="test-tool",
        description="Test",
        template_type="basic_function",
        output_dir=temp_output_dir
    )
    
    # Validate it
    validation = _validate_mcp_tool_impl(result["path"])
    
    assert validation["status"] in ["success", "warning"]
    assert len(validation["checks_passed"]) > 0
    assert "server.py" in str(validation["checks_passed"])
    assert "pyproject.toml" in str(validation["checks_passed"])


def test_validate_nonexistent_tool():
    """Test validation of non-existent tool"""
    from mcp_extend.server import _validate_mcp_tool_impl
    
    result = _validate_mcp_tool_impl("/nonexistent/path/to/tool")
    
    assert result["status"] == "error"
    assert "does not exist" in result["error"]

