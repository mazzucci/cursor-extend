"""
Cursor Extend Server

Extend Cursor with custom Python utilities through conversation.
This MCP extension guides Cursor to build project-specific Python tools
that remember commands, wrap APIs, and expand Cursor's capabilities.

Cursor forgets. Your project remembers.
"""

from fastmcp import FastMCP
from typing import Literal, Dict, Any
import json
import os
from pathlib import Path
from .generator import ToolGenerator

mcp = FastMCP("Cursor Extend ⚡")
generator = ToolGenerator()


def _get_mcp_tool_guide_impl(
    tool_type: str,
    user_requirements: str,
    tool_name: str
) -> dict:
    """Implementation of get_mcp_tool_guide (testable)
    
    This tool provides patterns, reference implementations, and best practices
    that Cursor can use to write a custom Python utility matching the user's exact needs.
    
    IMPORTANT: This does NOT create files. It only returns code and patterns.
    Cursor will write files after user confirmation.
    
    Args:
        tool_type: Type of tool to build (http_api, shell)
        user_requirements: What the user wants the tool to do (in plain English)
        tool_name: Name for the tool (e.g., "github", "kibana")
    
    Returns:
        Complete guide including:
        - reference_code: Working code examples
        - patterns: How to structure each component
        - best_practices: Security, error handling, configuration
        - dependencies: What packages are needed
    """
    # Module name (sanitized for Python imports)
    import re
    module_name = re.sub(r'[^\w\s-]', '', tool_name.lower())
    module_name = re.sub(r'[-\s]+', '_', module_name).strip('_')
    
    # Get reference implementation from templates (in memory only)
    try:
        # Render templates without writing to disk
        from jinja2 import Template
        import importlib.resources
        
        # Load template files
        templates_pkg = "mcp_extend.templates"
        
        # Determine which template to use
        template_file = f"{tool_type}.py.jinja"
        
        # Read templates as text
        with importlib.resources.open_text(templates_pkg, template_file) as f:
            server_template = f.read()
        
        with importlib.resources.open_text(templates_pkg, "pyproject.toml.jinja") as f:
            pyproject_template = f.read()
        
        # Render templates with context
        context = {
            "tool_name": tool_name,
            "description": user_requirements,
        }
        
        server_code = Template(server_template).render(**context)
        pyproject_code = Template(pyproject_template).render(**context)
        
        # Standard .gitignore
        gitignore_code = """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.DS_Store
uv.lock
"""
        
        # No MCP config needed - pure Python modules are imported directly
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to prepare guide"
        }
    
    # Load instructions template
    with importlib.resources.open_text(templates_pkg, "tool_guide_instructions.jinja") as f:
        instructions_template_text = f.read()
    
    instructions = Template(instructions_template_text).render(
        tool_name=tool_name,
        module_name=module_name
    )
    
    # Build comprehensive guide
    guide = {
        "status": "success",
        "tool_name": tool_name,
        "tool_type": tool_type,
        "user_requirements": user_requirements,
        "module_name": module_name,
        
        "instructions_for_cursor": instructions,
        
        "reference_code": {
            f"{module_name}.py": server_code,
            "pyproject.toml": pyproject_code,
            ".gitignore": gitignore_code,
        },
        
        "directory_structure": {
            "path": f".cursor/tools/{tool_name}/",
            "files": [
                f"{module_name}.py",
                "pyproject.toml",
                ".gitignore"
            ]
        },
        
        "usage_after_creation": f"""
To use the generated tool:
1. cd .cursor/tools/{tool_name}
2. uv sync  # Install dependencies
3. python -c 'from {module_name} import *; print("Ready!")'
4. Or import in Cursor code execution:
   from {module_name} import function_name
   result = function_name(args)
""",
        
        "patterns": _get_patterns_for_type(tool_type),
        
        "best_practices": [
            "Use async functions for I/O operations (HTTP requests, file reads)",
            "Include detailed docstrings with Args, Returns, and Examples",
            "Handle errors gracefully and return helpful error messages",
            "Use environment variables for sensitive data (API keys, tokens)",
            "Test locally: cd to .cursor/tools/{tool_name}, run 'uv sync', test imports"
        ]
    }
    
    return guide


@mcp.tool()
def get_mcp_tool_guide(
    tool_type: Literal["http_api", "shell"],
    user_requirements: str,
    tool_name: str
) -> dict:
    """Get instructions and code for building a custom Python utility
    
    This tool provides step-by-step instructions, reference code, and best practices
    for Cursor to create a custom Python utility matching the user's exact needs.
    
    The tool will be created in .cursor/tools/{tool_name}/ so it can be
    committed to git and shared with your team.
    
    IMPORTANT: This does NOT create files - it provides instructions for Cursor to create them.
    
    Args:
        tool_type: Type of tool to build (http_api or shell)
        user_requirements: What the user wants the tool to do (in plain English)
        tool_name: Name for the tool (e.g., "github", "kibana")
    
    Returns:
        Complete guide including:
        - instructions_for_cursor: Step-by-step file creation workflow
        - reference_code: Actual code for each file
        - patterns: How to structure components
        - best_practices: Security, error handling, configuration
    
    Example:
        User: "Create a weather tool called weather-tool"
        Cursor calls: get_mcp_tool_guide("http_api", "Fetch weather data", "weather-tool")
        Cursor: "I'll create weather-tool in .cursor/tools/weather-tool/. Proceed?"
        User: "Yes"
        Cursor: *writes files using reference_code*
        Cursor: "✅ Created Python utility: .cursor/tools/weather-tool/weather_tool.py"
    """
    return _get_mcp_tool_guide_impl(tool_type, user_requirements, tool_name)


def _get_patterns_for_type(tool_type: str) -> Dict[str, Any]:
    """Get coding patterns and best practices for a specific tool type"""
    patterns = {
        "http_api": {
            "async_http": {
                "pattern": "async with httpx.AsyncClient() as client: response = await client.get(url)",
                "explanation": "Use httpx for async HTTP requests with proper resource management"
            },
            "error_handling": {
                "pattern": "try/except with httpx.HTTPStatusError and httpx.RequestError",
                "explanation": "Catch specific HTTP errors and return helpful messages"
            },
            "environment_config": {
                "pattern": "API_BASE_URL = os.getenv('API_BASE_URL', 'default')",
                "explanation": "Use environment variables for configuration"
            },
            "function_signature": {
                "pattern": "async def function_name(param: type) -> return_type:",
                "explanation": "Use type hints for better IDE support and documentation"
            },
            "docstrings": {
                "pattern": "Include docstrings with Args, Returns, and Examples sections",
                "explanation": "Clear documentation helps Cursor understand how to use the function"
            }
        },
        "shell": {
            "subprocess_safety": {
                "pattern": "subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, check=False)",
                "explanation": "Use subprocess.run with timeout and capture_output for safe command execution"
            },
            "error_handling": {
                "pattern": "try/except with subprocess.TimeoutExpired and general Exception",
                "explanation": "Handle timeouts and command failures gracefully"
            },
            "output_parsing": {
                "pattern": "Parse stdout/stderr, check return codes, format output appropriately",
                "explanation": "Transform raw command output into actionable information"
            },
            "validation": {
                "pattern": "Validate inputs, whitelist commands (if production), check tool availability",
                "explanation": "Security: never trust user input, restrict what can be executed"
            },
            "function_signature": {
                "pattern": "def function_name(param: type) -> return_type:",
                "explanation": "Use type hints and clear parameter names"
            }
        },
    }
    return patterns.get(tool_type, {})


@mcp.tool()
def remember_command(
    name: str,
    command: str,
    description: str = ""
) -> dict:
    """Get instructions for saving a command to .cursor/commands.json
    
    This tool provides step-by-step instructions for Cursor to save commands.
    It does NOT create or modify files - Cursor will do that after user confirmation.
    
    Perfect for:
    - Shell commands (ssh, docker, etc.)
    - Build/deploy scripts
    - npm/yarn commands
    - Any command you run repeatedly
    
    Args:
        name: Short name to recall command (e.g., "deploy-staging", "check-logs")
        command: The shell command to run (e.g., "./scripts/deploy.sh staging")
        description: Human-readable description of what this does
    
    Returns:
        Instructions for Cursor on how to save the command
    
    Example:
        remember_command("deploy", "./scripts/deploy.sh staging", "Deploy to staging")
    """
    from jinja2 import Template
    import importlib.resources
    
    # Load templates
    templates_pkg = "mcp_extend.templates"
    
    with importlib.resources.open_text(templates_pkg, "remember_command_instructions.jinja") as f:
        instructions_template = f.read()
    
    with importlib.resources.open_text(templates_pkg, "cursorrules_commands.jinja") as f:
        cursorrules_template = f.read()
    
    # Render templates
    instructions = Template(instructions_template).render(
        name=name,
        command=command,
        description=description or name
    )
    
    cursorrules_content = Template(cursorrules_template).render()
    
    # Create the command entry structure
    command_entry = {
        "command": command,
        "description": description or name
    }
    
    return {
        "status": "success",
        "message": f"📝 Ready to save command '{name}'",
        
        "instructions_for_cursor": instructions,
        "command_entry": command_entry,
        "cursorrules_content": cursorrules_content.strip(),
        
        "files_to_update": {
            ".cursor/commands.json": {
                "action": "add_to_commands_object",
                "key": name,
                "value": command_entry
            },
            ".cursorrules": {
                "action": "append_if_not_exists",
                "check_for": "saved commands",
                "content": cursorrules_content.strip()
            }
        },
        
        "example_commands_json": {
            "commands": {
                name: command_entry,
                "example_other_command": {
                    "command": "npm test",
                    "description": "Run tests"
                }
            }
        },
        
        "next_steps": [
            f"✅ Command '{name}' will be saved to .cursor/commands.json",
            "💡 Commit .cursor/ and .cursorrules to git for team sharing",
            "🎯 Add more commands or start using them"
        ]
    }


@mcp.tool()
def discover_project_commands() -> dict:
    """Guide for Cursor to discover commands in this project - the command discovery magic! 🔍
    
    This is a GUIDE, not a template. It tells Cursor HOW to analyze the project
    using AI understanding to find command candidates that keep getting forgotten.
    
    When user says "discover commands" or "find commands to save":
    1. Use this guide to intelligently analyze the project
    2. Present discovered commands to the user
    3. Offer to save them with remember_command()
    
    Returns:
        Instructions for Cursor on how to discover and categorize commands
    """
    from jinja2 import Template
    import importlib.resources
    
    # Get current directory name for context
    project_name = Path.cwd().name
    
    # Load instructions template
    templates_pkg = "mcp_extend.templates"
    with importlib.resources.open_text(templates_pkg, "discover_commands_instructions.jinja") as f:
        instructions_template = f.read()
    
    instructions = Template(instructions_template).render()
    
    return {
        "status": "success",
        "message": f"🔍 Analyzing '{project_name}' for command candidates...",
        
        "instructions_for_cursor": instructions
    }


def main():
    """Main entry point for the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()

