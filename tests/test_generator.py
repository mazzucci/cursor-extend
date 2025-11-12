"""
Tests for the Python utility generator
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


def test_generate_shell_tool(generator, temp_output_dir):
    """Test generating a shell command utility"""
    result = generator.generate_tool(
        tool_name="test-shell",
        description="Test shell command tool",
        template_type="shell",
        output_dir=temp_output_dir
    )
    
    assert result["status"] == "success"
    assert "test-shell" in result["path"]
    
    # Check files were created
    tool_path = Path(result["path"])
    assert (tool_path / "test_shell.py").exists()
    assert (tool_path / "pyproject.toml").exists()
    assert (tool_path / ".gitignore").exists()
    
    # Check module contains expected content (pure Python, no FastMCP)
    module_content = (tool_path / "test_shell.py").read_text()
    assert "subprocess" in module_content
    assert "run_command" in module_content
    assert "check_command_available" in module_content
    assert "FastMCP" not in module_content  # Should NOT have FastMCP
    assert "@mcp.tool()" not in module_content  # Should NOT have decorators


def test_generate_http_api_tool(generator, temp_output_dir):
    """Test generating an HTTP API utility"""
    result = generator.generate_tool(
        tool_name="api-tool",
        description="HTTP API wrapper",
        template_type="http_api",
        output_dir=temp_output_dir
    )
    
    assert result["status"] == "success"
    
    # Verify module contains expected content (pure Python, no FastMCP)
    module_content = (Path(result["path"]) / "api_tool.py").read_text()
    assert "httpx" in module_content
    assert "async" in module_content
    assert "query_api" in module_content  # Generic function
    assert "API_BASE_URL" in module_content  # Configuration
    assert "API_TOKEN" in module_content  # Auth support
    assert "Add your API-specific functions here" in module_content  # Guidance comment
    assert "FastMCP" not in module_content  # Should NOT have FastMCP
    assert "@mcp.tool()" not in module_content  # Should NOT have decorators


def test_generated_tool_is_valid_python(generator, temp_output_dir):
    """Test that generated Python code is syntactically valid"""
    result = generator.generate_tool(
        tool_name="test-tool",
        description="Test",
        template_type="shell",
        output_dir=temp_output_dir
    )
    
    module_file = Path(result["path"]) / "test_tool.py"
    
    # Try to compile the generated Python code
    import py_compile
    try:
        py_compile.compile(str(module_file), doraise=True)
    except py_compile.PyCompileError as e:
        pytest.fail(f"Generated Python code is invalid: {e}")


def test_tool_name_sanitization(generator, temp_output_dir):
    """Test that tool names with spaces/special chars are handled"""
    result = generator.generate_tool(
        tool_name="My Cool Tool!!!",
        description="Test",
        template_type="shell",
        output_dir=temp_output_dir
    )
    
    assert result["status"] == "success"
    # Should create a valid directory name
    assert Path(result["path"]).exists()
    assert "my-cool-tool" in result["path"].lower()
    # Should create valid Python module name
    assert Path(result["path"] + "/my_cool_tool.py").exists()


def test_get_mcp_tool_guide(temp_output_dir):
    """Test the get_mcp_tool_guide function (instruction-based)"""
    from mcp_extend.server import _get_mcp_tool_guide_impl
    
    # Test tool guide generation
    result = _get_mcp_tool_guide_impl(
        tool_type="http_api",
        user_requirements="Query weather API",
        tool_name="weather"
    )
    
    assert result["status"] == "success"
    assert result["tool_name"] == "weather"
    assert result["tool_type"] == "http_api"
    assert result["module_name"] == "weather"
    
    # Check instruction-based structure
    assert "instructions_for_cursor" in result
    assert "reference_code" in result
    assert "patterns" in result
    assert "best_practices" in result
    assert "directory_structure" in result
    
    # Verify instructions ask for confirmation
    assert "Ask user for confirmation" in result["instructions_for_cursor"]
    assert "Step 1" in result["instructions_for_cursor"]
    
    # Check reference code is included (module name, not server.py)
    assert "weather.py" in result["reference_code"]
    assert "pyproject.toml" in result["reference_code"]
    # Should NOT have FastMCP
    assert "fastmcp" not in result["reference_code"]["weather.py"].lower()
    # Should have httpx
    assert "httpx" in result["reference_code"]["weather.py"].lower()
    
    # Check that MCP config is NOT present (pure Python modules don't need it)
    assert "mcp_config_to_merge" not in result
    assert "mcp_config_path" not in result
    
    # Verify tool directory structure uses .cursor/tools/
    assert ".cursor/tools" in result["directory_structure"]["path"]
    assert ".cursor/mcp-tools" not in result["directory_structure"]["path"]
