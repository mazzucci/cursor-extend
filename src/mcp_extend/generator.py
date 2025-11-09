"""
Code generation logic for MCP tools
"""

from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, PackageLoader
import re


class ToolGenerator:
    """Generates MCP tool projects from templates"""
    
    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('mcp_extend', 'templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate_tool(
        self,
        tool_name: str,
        description: str,
        template_type: str,
        output_dir: str = "~/cursor-mcp-tools"
    ) -> Dict[str, Any]:
        """Generate a new MCP tool project
        
        Args:
            tool_name: Name of the new tool (e.g., "Weather API", "File Utils")
            description: What the tool does
            template_type: Type of template to use (basic_function, http_api, internal_api, file_operations)
            output_dir: Where to create the tool (default: ~/cursor-mcp-tools)
            
        Returns:
            Dictionary with status, path, files_created, and next_steps
        """
        # Create output directory
        output_path = Path(output_dir).expanduser() / self._sanitize_name(tool_name)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate files
        self._generate_server(output_path, tool_name, description, template_type)
        self._generate_pyproject(output_path, tool_name, description, template_type)
        self._generate_readme(output_path, tool_name, description, template_type)
        self._generate_gitignore(output_path)
        
        script_name = self._to_script_name(tool_name)
        
        return {
            "status": "success",
            "path": str(output_path),
            "files_created": [
                "server.py",
                "pyproject.toml", 
                "README.md",
                ".gitignore"
            ],
            "next_steps": [
                f"cd {output_path}",
                "uv sync",
                "uv run python server.py",
                "# Add to Cursor's MCP config"
            ],
            "install_command": f"uvx --from {output_path} {script_name}"
        }
    
    def _generate_server(self, path: Path, name: str, desc: str, template: str):
        """Generate the main server.py file"""
        template_file = self.env.get_template(f'{template}.py.jinja')
        content = template_file.render(
            tool_name=name,
            description=desc,
            class_name=self._to_class_name(name)
        )
        (path / "server.py").write_text(content)
    
    def _generate_pyproject(self, path: Path, name: str, desc: str, template: str):
        """Generate pyproject.toml"""
        template_file = self.env.get_template('pyproject.toml.jinja')
        
        # Determine dependencies based on template type
        extra_deps = []
        if template in ["http_api", "internal_api"]:
            extra_deps.append("httpx>=0.27.0")
        
        content = template_file.render(
            tool_name=self._to_script_name(name),
            description=desc,
            script_name=self._to_script_name(name),
            extra_dependencies=extra_deps
        )
        (path / "pyproject.toml").write_text(content)
    
    def _generate_readme(self, path: Path, name: str, desc: str, template: str):
        """Generate README.md"""
        template_file = self.env.get_template('README.md.jinja')
        
        # Determine if this is an internal tool
        is_internal = template == "internal_api"
        
        content = template_file.render(
            tool_name=name,
            description=desc,
            script_name=self._to_script_name(name),
            path=str(path),
            is_internal=is_internal
        )
        (path / "README.md").write_text(content)
    
    def _generate_gitignore(self, path: Path):
        """Generate .gitignore"""
        gitignore = """
__pycache__/
*.py[cod]
*$py.class
.venv/
.uv/
*.egg-info/
dist/
build/
.pytest_cache/
"""
        (path / ".gitignore").write_text(gitignore.strip())
    
    def _sanitize_name(self, name: str) -> str:
        """Convert tool name to valid directory name"""
        # Replace spaces and special chars with hyphens
        sanitized = re.sub(r'[^\w\s-]', '', name.lower())
        sanitized = re.sub(r'[-\s]+', '-', sanitized)
        return sanitized.strip('-')
    
    def _to_script_name(self, name: str) -> str:
        """Convert tool name to script/package name"""
        return self._sanitize_name(name)
    
    def _to_class_name(self, name: str) -> str:
        """Convert tool name to PascalCase class name"""
        return "".join(word.capitalize() for word in name.split())






