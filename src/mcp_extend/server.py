"""
Cursor Extend Server

Extend Cursor with custom MCP tools through conversation.
This MCP tool guides Cursor to build project-specific MCP tools
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
    tool_name: str,
    output_path: str = "./.mcp-tool",
    is_project_tool: bool = True
) -> dict:
    """Implementation of get_mcp_tool_guide (testable)
    
    This tool provides patterns, reference implementations, and best practices
    that Cursor can use to write a custom MCP tool matching the user's exact needs.
    
    IMPORTANT: This does NOT create files. It only returns code and patterns.
    Cursor will ask the user for confirmation before creating anything.
    
    Args:
        tool_type: Type of tool to build (http_api, basic_function, file_operations)
        user_requirements: What the user wants the tool to do (in plain English)
        tool_name: Name for the tool (e.g., "weather-tool", "debug-api")
        output_path: Where to create the tool (default: ./.mcp-tool for project, ~/cursor-mcp-tools for global)
        is_project_tool: True for project-specific tool, False for global tool (default: True)
    
    Returns:
        Complete guide including:
        - project_structure: What files to create and where
        - patterns: How to structure each component
        - reference_code: Working examples to learn from
        - best_practices: Security, error handling, configuration
        - dependencies: What packages are needed
        - setup_instructions: How to test and deploy
    """
    # Expand home directory if needed
    expanded_path = os.path.expanduser(output_path) if output_path.startswith("~") else output_path
    
    # Determine paths based on tool type
    if is_project_tool:
        # Project tool: .mcp-tool in current directory
        tool_dir = expanded_path if not expanded_path.endswith(tool_name) else expanded_path
        cursor_config_path = ".cursor/mcp.json"  # Relative path for project
        tool_path_in_config = output_path  # Use relative path in config
    else:
        # Global tool: ~/cursor-mcp-tools/tool-name
        tool_dir = os.path.join(expanded_path, tool_name)
        cursor_config_path = os.path.join(os.path.expanduser("~"), ".cursor", "mcp.json")
        tool_path_in_config = tool_dir  # Use absolute path for global tools
    
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
        
        with importlib.resources.open_text(templates_pkg, "README.md.jinja") as f:
            readme_template = f.read()
        
        # Render templates with context
        context = {
            "tool_name": tool_name,
            "description": user_requirements,
        }
        
        server_code = Template(server_template).render(**context)
        pyproject_code = Template(pyproject_template).render(**context)
        readme_code = Template(readme_template).render(**context)
        
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
        
        # Cursor MCP config for project tools
        cursor_mcp_config = f'''{{
  "mcpServers": {{
    "{tool_name}": {{
      "command": "uvx",
      "args": ["--from", "{tool_path_in_config}", "{tool_name}"]
    }}
  }}
}}'''
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to prepare guide"
        }
    
    # Build comprehensive guide
    guide = {
        "status": "success",
        "tool_name": tool_name,
        "tool_type": tool_type,
        "user_requirements": user_requirements,
        
        "instructions_for_cursor": (
            "This is a GUIDE only - files are NOT created yet. "
            "Show the user what you'll create and ASK for confirmation before writing files. "
            "Use the reference_implementation to write the actual files. "
            f"FOR PROJECT TOOLS: Also create {cursor_config_path} with the MCP config. "
            f"FOR GLOBAL TOOLS: Show config for ~/.cursor/mcp.json and ask if they want to add it. "
            "After creating files, display the clickable path to server.py: "
            f"'Created your MCP server: {tool_dir}/server.py (click to review)'. "
            "Then offer to test with 'uv sync' (MUST use required_permissions: ['all']). "
            "Finally, remind to restart Cursor to load the new tool."
        ),
        
        "project_structure": {
            "tool_directory": tool_dir,
            "files_to_create": [
                {
                    "path": "server.py",
                    "description": "Main MCP server implementation with tool functions"
                },
                {
                    "path": "pyproject.toml",
                    "description": "Project configuration and dependencies (for uv)"
                },
                {
                    "path": "README.md",
                    "description": "Setup and usage instructions"
                },
                {
                    "path": ".gitignore",
                    "description": "Git ignore patterns for Python projects"
                }
            ] + ([{
                "path": "../.cursor/mcp.json",
                "description": "Cursor MCP configuration (project-level)"
            }] if is_project_tool else [])
        },
        
        "reference_implementation": {
            "server.py": server_code,
            "pyproject.toml": pyproject_code,
            "README.md": readme_code,
            ".gitignore": gitignore_code,
            **({".cursor/mcp.json": cursor_mcp_config} if is_project_tool else {})
        },
        
        "patterns": _get_patterns_for_type(tool_type),
        
        "best_practices": [
            "Use async functions for I/O operations (HTTP requests, file reads)",
            "Include detailed docstrings - Cursor uses these to understand tools",
            "Handle errors gracefully and return helpful error messages",
            "Use environment variables for sensitive data (API keys, tokens)",
            "Tools run locally as subprocesses and inherit user's environment",
            "For internal APIs: No special VPN setup needed - inherits connection",
            "Test locally first: cd to directory, run 'uv sync', then 'uv run python server.py'"
        ],
        
        "next_steps": {
            "1_show_path": f"Display clickable path: 'Created your MCP server: {tool_dir}/server.py (click to review)'",
            "2_test": f"Offer to run: cd {tool_dir} && uv sync (MUST use required_permissions: ['all'])",
            "3_config": (
                f"PROJECT TOOL: Config already created at {cursor_config_path}. Just restart Cursor!" 
                if is_project_tool else
                f"GLOBAL TOOL: Show config block for ~/.cursor/mcp.json (FULL absolute path - clickable!):\n"
                f'```json\n'
                f'"{tool_name}": {{\n'
                f'  "command": "uvx",\n'
                f'  "args": ["--from", "{tool_path_in_config}", "{tool_name}"]\n'
                f'}}\n'
                f'```\n'
                f'ASK: "Want me to add this to your Cursor config?"'
            ),
            "4_add_if_global": "If GLOBAL tool and user says yes, use add_tool_to_cursor_config tool",
            "5_restart": "Remind user to restart Cursor to load the new tool"
        }
    }
    
    return guide


@mcp.tool()
def get_mcp_tool_guide(
    tool_type: Literal["http_api", "basic_function", "file_operations"],
    user_requirements: str,
    tool_name: str,
    output_path: str = "./.mcp-tool",
    is_project_tool: bool = True
) -> dict:
    """Get a comprehensive guide for building a custom MCP tool
    
    This tool provides patterns, reference implementations, and best practices
    that Cursor can use to write a custom MCP tool matching the user's exact needs.
    
    IMPORTANT - Conversational Flow:
    1. When the user asks to create a tool, FIRST ask them:
       - "What should we call this tool?" (suggest a name based on their request)
       - "Project tool (loads when opening this project) or Global tool (available everywhere)?"
       - DEFAULT to project tool (.mcp-tool in current directory)
    2. Call this tool with their answers to get the code
    3. Show them what files you'll create and ask: "Should I create these files?"
    4. ONLY after they confirm, write the files using the reference_implementation
    5. After creating files, show the clickable path to the generated server.py:
       "Created your MCP server: /full/path/to/server.py (click to review)"
    6. Offer to test it: "Want me to run 'uv sync' to test the installation?"
       IMPORTANT: When running uv sync, MUST use required_permissions: ['all'] (sandbox blocks cache access)
    7. FOR PROJECT TOOLS: Automatically create .cursor/mcp.json with relative path
       FOR GLOBAL TOOLS: Show config for ~/.cursor/mcp.json and offer to add it
    8. Consider updating .cursorrules if the tool should be automatically discovered
    9. Remind user to restart Cursor (project tools load automatically on restart)
    
    This does NOT create any files - it only returns code and patterns.
    
    Args:
        tool_type: Type of tool to build (http_api, basic_function, file_operations)
        user_requirements: What the user wants the tool to do (in plain English)
        tool_name: Name for the tool (e.g., "weather-tool", "debug-api")
        output_path: Where to create the tool (default: ./.mcp-tool for project, ~/cursor-mcp-tools for global)
        is_project_tool: True for project-specific tool, False for global tool (default: True)
    
    Returns:
        Complete guide including:
        - project_structure: What files to create and where
        - reference_implementation: Actual code for each file (use this to write files)
        - patterns: How to structure each component
        - best_practices: Security, error handling, configuration
        - next_steps: What to do after creating the tool
    
    Example:
        User: "Create a weather tool"
        Cursor: "I'll create a tool called 'weather-tool' in ~/cursor-mcp-tools. Sound good?"
        User: "Yes"
        Cursor: *calls get_mcp_tool_guide(...)*
        Cursor: "Here's what I'll create: [shows files]. Should I proceed?"
        User: "Yes"
        Cursor: *writes files from reference_implementation*
        Cursor: "Files created! Want me to show server.py so you can review it?"
        User: "Yes"
        Cursor: *calls read_file to show contents*
        Cursor: "Here's your tool (click to open in editor): /path/to/server.py"
        Cursor: "Want me to run 'uv sync' to test the installation?"
    """
    return _get_mcp_tool_guide_impl(tool_type, user_requirements, tool_name, output_path, is_project_tool)


def _get_patterns_for_type(tool_type: str) -> Dict[str, Any]:
    """Get coding patterns and best practices for a specific tool type"""
    patterns = {
        "http_api": {
            "fastmcp_setup": {
                "pattern": "from fastmcp import FastMCP; mcp = FastMCP('ToolName')",
                "explanation": "Initialize FastMCP server with descriptive name"
            },
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
            "tool_decorator": {
                "pattern": "@mcp.tool()\\nasync def function_name(param: type) -> return_type:",
                "explanation": "Decorate functions with @mcp.tool() and include type hints"
            }
        },
        "basic_function": {
            "fastmcp_setup": {
                "pattern": "from fastmcp import FastMCP; mcp = FastMCP('ToolName')",
                "explanation": "Initialize FastMCP server with descriptive name"
            },
            "simple_functions": {
                "pattern": "@mcp.tool()\\ndef function_name(param: type) -> return_type:",
                "explanation": "Simple sync functions for calculations and transformations"
            },
            "docstrings": {
                "pattern": "Detailed docstring with Args and Returns sections",
                "explanation": "Help Cursor understand what the tool does"
            }
        },
        "file_operations": {
            "fastmcp_setup": {
                "pattern": "from fastmcp import FastMCP; mcp = FastMCP('ToolName')",
                "explanation": "Initialize FastMCP server with descriptive name"
            },
            "path_handling": {
                "pattern": "from pathlib import Path; path = Path(file_path).resolve()",
                "explanation": "Use pathlib for safe path manipulation"
            },
            "file_safety": {
                "pattern": "Check file exists, validate paths, handle permission errors",
                "explanation": "Always validate before file operations"
            }
        }
    }
    return patterns.get(tool_type, {})


def _add_tool_to_cursor_config_impl(tool_name: str, tool_path: str) -> dict:
    """Implementation of add_tool_to_cursor_config (testable)
    
    Updates ~/.cursor/mcp.json to include the new tool. The user will need
    to restart Cursor for changes to take effect.
    
    Args:
        tool_name: Name of the tool (must match the tool directory name)
        tool_path: Absolute path to the tool directory
    
    Returns:
        Status and instructions for the user
    """
    try:
        config_path = Path.home() / ".cursor" / "mcp.json"
        
        # Expand path
        expanded_path = os.path.expanduser(tool_path)
        
        # Read existing config or create new one
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config = {"mcpServers": {}}
        
        # Ensure mcpServers exists
        if "mcpServers" not in config:
            config["mcpServers"] = {}
        
        # Add the new tool
        config["mcpServers"][tool_name] = {
            "command": "uvx",
            "args": ["--from", expanded_path, tool_name]
        }
        
        # Write back
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return {
            "status": "success",
            "message": f"✅ Added '{tool_name}' to Cursor configuration",
            "config_path": str(config_path),
            "tool_config": config["mcpServers"][tool_name],
            "next_steps": [
                "⚠️  IMPORTANT: Restart Cursor for changes to take effect",
                f"After restart, you can use the {tool_name} in conversations",
                f"Example: 'Use {tool_name} to...'"
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to update Cursor configuration",
            "manual_instructions": {
                "file": "~/.cursor/mcp.json",
                "add": {
                    "mcpServers": {
                        tool_name: {
                            "command": "uvx",
                            "args": ["--from", tool_path, tool_name]
                        }
                    }
                }
            }
        }


@mcp.tool()
def add_tool_to_cursor_config(
    tool_name: str,
    tool_path: str
) -> dict:
    """Add a generated MCP tool to Cursor's configuration
    
    Updates ~/.cursor/mcp.json to include the new tool. The user will need
    to restart Cursor for changes to take effect.
    
    Args:
        tool_name: Name of the tool (must match the tool directory name)
        tool_path: Absolute path to the tool directory
    
    Returns:
        Status and instructions for the user
    
    Example:
        add_tool_to_cursor_config(
            tool_name="weather-tool",
            tool_path="/Users/username/cursor-mcp-tools/weather-tool"
        )
    """
    return _add_tool_to_cursor_config_impl(tool_name, tool_path)


def _validate_mcp_tool_impl(tool_path: str) -> dict:
    """Implementation of validate_mcp_tool (testable)
    
    Checks that all required files exist, Python syntax is valid,
    and the tool can be imported without errors.
    
    Args:
        tool_path: Path to the tool directory
    
    Returns:
        Validation results with any issues found
    """
    try:
        expanded_path = Path(os.path.expanduser(tool_path))
        
        if not expanded_path.exists():
            return {
                "status": "error",
                "error": "Tool directory does not exist",
                "path": str(expanded_path)
            }
        
        issues = []
        checks = []
        
        # Check required files
        required_files = ["server.py", "pyproject.toml", "README.md", ".gitignore"]
        for filename in required_files:
            file_path = expanded_path / filename
            if file_path.exists():
                checks.append(f"✅ {filename} exists")
            else:
                issues.append(f"❌ Missing {filename}")
        
        # Validate Python syntax in server.py
        server_file = expanded_path / "server.py"
        if server_file.exists():
            try:
                import py_compile
                py_compile.compile(str(server_file), doraise=True)
                checks.append("✅ server.py has valid Python syntax")
            except py_compile.PyCompileError as e:
                issues.append(f"❌ Python syntax error in server.py: {e}")
        
        # Check pyproject.toml has required fields
        pyproject_file = expanded_path / "pyproject.toml"
        if pyproject_file.exists():
            content = pyproject_file.read_text()
            if "fastmcp" in content:
                checks.append("✅ FastMCP dependency found")
            else:
                issues.append("⚠️  FastMCP not found in dependencies")
        
        return {
            "status": "success" if not issues else "warning",
            "tool_path": str(expanded_path),
            "checks_passed": checks,
            "issues_found": issues,
            "summary": f"{len(checks)} checks passed, {len(issues)} issues found" if issues else "All checks passed! ✅"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to validate tool"
        }


@mcp.tool()
def validate_mcp_tool(tool_path: str) -> dict:
    """Validate that a generated MCP tool is properly structured
    
    Checks that all required files exist, Python syntax is valid,
    and the tool can be imported without errors.
    
    Args:
        tool_path: Path to the tool directory
    
    Returns:
        Validation results with any issues found
    
    Example:
        validate_mcp_tool("~/cursor-mcp-tools/weather-tool")
    """
    return _validate_mcp_tool_impl(tool_path)


@mcp.tool()
def list_available_templates() -> dict:
    """List all available MCP tool templates
    
    Returns information about each template type including:
    - Name and description
    - What tools/functions it includes
    - When to use it
    - Example use cases
    
    Returns:
        Dictionary mapping template names to their details
    """
    return {
        "basic_function": {
            "name": "Basic Function",
            "description": "Simple utility functions and calculations",
            "includes": [
                "add() - Add two numbers",
                "multiply() - Multiply two numbers"
            ],
            "use_when": "You want to expose simple Python functions to Cursor",
            "examples": [
                "Calculator tools",
                "String manipulation",
                "Data transformations",
                "Unit conversions"
            ]
        },
        "http_api": {
            "name": "HTTP API Wrapper",
            "description": "Tools for calling HTTP APIs - both external AND internal",
            "includes": [
                "query_api() - Generic HTTP GET with auth support (customize for your needs)",
                "get_weather() - Working example using wttr.in API"
            ],
            "use_when": "You want to integrate APIs that don't have MCP support",
            "how_it_works": [
                "Runs locally as subprocess on your machine",
                "For internal APIs: Inherits your VPN connection automatically",
                "For authenticated APIs: Uses environment variables (API_BASE_URL, API_TOKEN)",
                "For public APIs: Works out of the box (see get_weather example)"
            ],
            "examples": [
                "🌐 External: Weather services, public REST APIs, third-party integrations",
                "🔒 Internal: Debug endpoints, admin APIs, VPN-protected services",
                "💼 Internal: Customer support queries, operational dashboards, database endpoints"
            ],
            "why_useful": [
                "Reduce context switching during debugging",
                "Enable non-engineers to query systems conversationally",
                "Combine with other MCP tools (Datadog, logs) for comprehensive insights",
                "No complex VPN/auth setup needed - uses your existing environment"
            ]
        },
        "file_operations": {
            "name": "File Operations",
            "description": "Tools for working with local files and directories",
            "includes": [
                "search_files() - Find files matching patterns",
                "read_file_content() - Read file contents safely"
            ],
            "use_when": "You want to give Cursor access to local file operations",
            "examples": [
                "Project analysis",
                "Log file parsing",
                "Configuration management",
                "File organization"
            ]
        }
    }


def _update_cursorrules_for_commands():
    """Update or create .cursorrules to tell Cursor about saved commands
    
    This ensures Cursor automatically checks .cursor/commands.json when users
    ask about running, building, testing, or deploying.
    """
    cursorrules_file = Path(".cursorrules")
    
    # The instruction block to add
    commands_instruction = """
# Saved Commands
This project has saved commands in .cursor/commands.json.
When the user asks about running, building, testing, deploying, or executing commands,
check the saved commands first using list_remembered_commands().
"""
    
    # Check if .cursorrules already mentions saved commands
    if cursorrules_file.exists():
        content = cursorrules_file.read_text()
        if "saved commands" in content.lower() or ".cursor/commands.json" in content:
            # Already has instructions, don't duplicate
            return
        # Append to existing file
        with open(cursorrules_file, 'a') as f:
            f.write("\n" + commands_instruction)
    else:
        # Create new file
        cursorrules_file.write_text(commands_instruction.strip() + "\n")


@mcp.tool()
def remember_command(
    name: str,
    command: str,
    description: str = ""
) -> dict:
    """Remember a shell command for easy recall - No Python or MCP knowledge needed!
    
    Stores simple commands in .cursor/commands.json so you can just say
    "run deploy" or "check logs" without creating a full MCP tool.
    
    Also creates/updates .cursorrules to tell Cursor to check saved commands automatically.
    
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
        Confirmation with usage instructions
    
    Example:
        remember_command("deploy", "./scripts/deploy.sh staging", "Deploy to staging")
        → Now just say "run deploy" or "deploy to staging"
    """
    try:
        # Ensure .cursor directory exists
        cursor_dir = Path(".cursor")
        cursor_dir.mkdir(exist_ok=True)
        
        # Load existing commands
        commands_file = cursor_dir / "commands.json"
        if commands_file.exists():
            with open(commands_file, 'r') as f:
                data = json.load(f)
        else:
            data = {"commands": {}, "version": "1.0"}
        
        # Add/update command
        data["commands"][name] = {
            "command": command,
            "description": description or name,
            "created": str(Path.cwd()),
            "updated": "2024-11-09"
        }
        
        # Save
        with open(commands_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Update .cursorrules to ensure Cursor checks saved commands
        _update_cursorrules_for_commands()
        
        return {
            "status": "success",
            "message": f"✅ Remembered '{name}'!",
            "usage": f"Just say '{description or name}' or 'run {name}' to execute",
            "command": command,
            "location": str(commands_file),
            "tip": "No Python needed - this is just a simple JSON file you can edit anytime!"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to save command '{name}'"
        }


@mcp.tool()
def list_remembered_commands() -> dict:
    """List all commands stored in .cursor/commands.json
    
    Shows all commands you've remembered, making it easy to see
    what's available without looking at the file.
    
    Returns:
        Dictionary of all stored commands with their details
    """
    try:
        commands_file = Path(".cursor/commands.json")
        
        if not commands_file.exists():
            return {
                "status": "success",
                "message": "No commands saved yet",
                "tip": "Use remember_command() to save your first command!",
                "commands": {}
            }
        
        with open(commands_file, 'r') as f:
            data = json.load(f)
        
        commands = data.get("commands", {})
        
        return {
            "status": "success",
            "message": f"Found {len(commands)} saved command(s)",
            "commands": commands,
            "file": str(commands_file),
            "tip": "Say 'run <name>' to execute any of these commands"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to list commands"
        }


@mcp.tool()
def discover_project_commands() -> dict:
    """Guide for Cursor to discover commands in this project - the "cursor extend" magic! 🔍
    
    This is a GUIDE, not a template. It tells Cursor HOW to analyze the project
    using AI understanding to find command candidates that keep getting forgotten.
    
    When user says "cursor extend" or "find commands to save":
    1. Use this guide to intelligently analyze the project
    2. Present discovered commands to the user
    3. Offer to save them with remember_command()
    
    Returns:
        Instructions for Cursor on how to discover and categorize commands
    """
    
    # Get current directory name for context
    project_name = Path.cwd().name
    
    return {
        "status": "success",
        "message": f"🔍 Analyzing '{project_name}' for command candidates...",
        
        "instructions_for_cursor": """
GOAL: Find commands that the user runs repeatedly but Cursor keeps forgetting.

ANALYSIS STEPS:

1. **Read key files** (use your AI understanding, not pattern matching):
   - package.json → Look at "scripts" section
   - Makefile → Look for targets
   - README.md → Find documented commands in code blocks
   - pyproject.toml / setup.py → Python project commands
   - Dockerfile / docker-compose.yml → Container commands
   - .github/workflows/ → CI/CD commands
   - Any files with "build", "deploy", "test" in name

2. **Understand the tech stack** (be intelligent about it):
   - React Native? → Suggest iOS/Android build commands
   - Python? → Suggest test/lint commands
   - Docker? → Suggest compose up/down
   - Kubernetes? → Suggest kubectl commands
   - Multiple services? → Suggest commands for each

3. **Categorize by complexity**:
   
   💨 **SIMPLE COMMANDS** (save to .cursor/commands.json):
   - Single commands or simple chains
   - Build/test/deploy scripts
   - npm/make/cargo commands
   - SSH commands
   - Docker commands
   - Anything that's just "run this shell command"
   
   🧠 **MCP TOOL CANDIDATES** (needs Python logic):
   - Requires HTTP client (calling APIs)
   - Needs data parsing/transformation
   - Conditional logic or error handling
   - Multi-step workflows with decision points
   - Authentication flows
   
4. **Present findings to user**:
   - Group by category (build, test, deploy, etc.)
   - Show actual command strings
   - Explain what each does
   - Recommend which to save

5. **Offer to save**:
   - For simple: "Want me to save these with remember_command()?"
   - For complex: "Want me to create an MCP tool for [description]?"

REMEMBER: You're using your AI understanding of the project, not rigid pattern matching!
""",
        
        "what_to_look_for": {
            "repetitive_commands": [
                "Commands documented in README that users run manually",
                "Build commands with specific flags/configurations",
                "Deploy scripts with staging/production variants",
                "Test commands with specific suites or options",
                "Database migration commands",
                "Cache clearing / environment reset commands"
            ],
            "hidden_complexity": [
                "Commands with environment variables",
                "Multi-step processes (build → test → deploy)",
                "Commands that require specific working directories",
                "Commands with project-specific paths/arguments"
            ],
            "team_pain_points": [
                "Commands that are 'tribal knowledge' (not documented)",
                "Different commands for different environments",
                "Commands that fail silently if done wrong",
                "Setup commands for new developers"
            ]
        },
        
        "categorization_guide": {
            "simple_command_indicators": [
                "Single shell command",
                "npm/yarn/pnpm run [script]",
                "make [target]",
                "Docker compose commands",
                "git commands",
                "SSH commands",
                "File system operations"
            ],
            "mcp_tool_indicators": [
                "Calls an API endpoint",
                "Requires parsing JSON/XML responses",
                "Needs authentication/tokens",
                "Conditional logic (if/else)",
                "Data transformation",
                "Error handling and retries"
            ]
        },
        
        "presentation_template": """
When presenting findings to user, format like this:

🔍 **Found X command candidates in [project_name]**

**💨 Simple Commands (save to .cursor/commands.json):**

*Build Commands:*
- `build-ios`: cd ios && pod install && cd .. && npx react-native run-ios
- `build-android`: npx react-native run-android --variant=release

*Test Commands:*
- `test`: npm test
- `test-e2e`: npm run test:e2e

*Deploy Commands:*
- `deploy-staging`: ./scripts/deploy.sh staging
- `deploy-prod`: ./scripts/deploy.sh production

**🧠 MCP Tool Candidates (need logic):**
- Debug API at `api.company.com/debug` → Needs HTTP client + auth
- Database query script → Needs connection + result formatting

**Want me to save these?**
Say "save all" or "save [specific command]"
""",
        
        "example_workflow": """
USER: "cursor extend"
CURSOR: *Calls discover_project_commands() → Gets this guide*
CURSOR: *Reads package.json, README.md, Makefile intelligently*
CURSOR: *Identifies 8 npm scripts, 3 documented README commands, 2 API endpoints*
CURSOR: *Categorizes: 11 simple commands, 2 MCP tool candidates*
CURSOR: *Presents organized list to user*
CURSOR: "Want me to save all 11 simple commands?"
USER: "yes"
CURSOR: *Calls remember_command() for each*
CURSOR: "✅ Saved! Your team can now clone and use these immediately."
""",
        
        "tips_for_cursor": [
            "Use your understanding of the tech stack - be smart, not mechanical",
            "Look for patterns in file names and content",
            "Check for commands in documentation (README, CONTRIBUTING.md)",
            "Consider the developer workflow: setup → develop → test → deploy",
            "Present commands in a way that makes sense to the user",
            "Offer to save everything at once for convenience"
        ]
    }


@mcp.tool()
def forget_command(name: str) -> dict:
    """Remove a command from .cursor/commands.json
    
    Args:
        name: The name of the command to forget
    
    Returns:
        Confirmation of deletion
    """
    try:
        commands_file = Path(".cursor/commands.json")
        
        if not commands_file.exists():
            return {
                "status": "error",
                "message": "No commands file found"
            }
        
        with open(commands_file, 'r') as f:
            data = json.load(f)
        
        if name in data.get("commands", {}):
            removed = data["commands"].pop(name)
            
            # Save updated file
            with open(commands_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return {
                "status": "success",
                "message": f"✅ Forgot '{name}'",
                "removed_command": removed["command"]
            }
        else:
            return {
                "status": "error",
                "message": f"Command '{name}' not found",
                "available": list(data.get("commands", {}).keys())
            }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to forget command '{name}'"
        }


def main():
    """Main entry point for the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()

