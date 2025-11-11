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
    tool_name: str,
    project_path: str = None
) -> dict:
    """Implementation of get_mcp_tool_guide (testable)
    
    This tool provides patterns, reference implementations, and best practices
    that Cursor can use to write a custom Python utility matching the user's exact needs.
    
    All tools are project-level and live in .cursor/tools/ directory.
    This enables team sharing through git commits.
    
    IMPORTANT: This does NOT create files. It only returns code and patterns.
    Cursor will ask the user for confirmation before creating anything.
    
    Args:
        tool_type: Type of tool to build (http_api, shell)
        user_requirements: What the user wants the tool to do (in plain English)
        tool_name: Name for the tool (e.g., "github", "kibana")
        project_path: Path to the project directory (REQUIRED - provide workspace root)
    
    Returns:
        Complete guide including:
        - project_structure: What files to create and where
        - patterns: How to structure each component
        - reference_code: Working examples to learn from
        - best_practices: Security, error handling, configuration
        - dependencies: What packages are needed
        - setup_instructions: How to test and use
    """
    # If no project_path provided, return error
    if project_path is None:
        return {
            "status": "error",
            "error": "project_path parameter is required",
            "message": "Project directory required to create Python utility",
            "instructions": (
                "Please provide the project_path parameter with the workspace root directory.\n\n"
                "Example:\n"
                "get_mcp_tool_guide(\n"
                "    tool_type=\"shell\",\n"
                "    user_requirements=\"Check PR lint status\",\n"
                "    tool_name=\"github\",\n"
                "    project_path=\"/Users/username/Projects/my-project\"\n"
                ")\n\n"
                "This will create the tool in:\n"
                "- /Users/username/Projects/my-project/.cursor/tools/github/\n"
                "- Tool can be committed to git for team sharing!"
            )
        }
    
    # Determine paths - always project-level
    project_dir = Path(project_path).resolve()
    
    # Tool directory: .cursor/tools/tool-name
    tool_dir = str(project_dir / ".cursor" / "tools" / tool_name)
    
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
            f"After creating files, display the clickable path to the module: "
            f"'Created Python utility: {tool_dir}/{module_name}.py (click to review)'. "
            "Then offer to test with 'uv sync' (MUST use required_permissions: ['all']). "
            "The tool will be in .cursor/ so it can be committed to git for your team! "
            "Users can import it directly: from {module_name} import *"
        ),
        
        "project_structure": {
            "tool_directory": tool_dir,
            "module_name": module_name,
            "files_to_create": [
                {
                    "path": f"{module_name}.py",
                    "description": "Main Python module with utility functions"
                },
                {
                    "path": "pyproject.toml",
                    "description": "Project configuration and dependencies (for uv)"
                },
                {
                    "path": ".gitignore",
                    "description": "Git ignore patterns for Python projects"
                }
            ]
        },
        
        "reference_implementation": {
            f"{module_name}.py": server_code,
            "pyproject.toml": pyproject_code,
            ".gitignore": gitignore_code,
        },
        
        "usage_instructions": (
            f"To use the generated tool:\n"
            f"1. cd {tool_dir}\n"
            "2. uv sync  # Install dependencies\n"
            f"3. python -c 'from {module_name} import *; print(\"Ready!\")'\n"
            "4. Or import in Cursor code execution:\n"
            f"   from {module_name} import function_name\n"
            f"   result = function_name(args)\n"
        ),
        
        "patterns": _get_patterns_for_type(tool_type),
        
        "best_practices": [
            "Use async functions for I/O operations (HTTP requests, file reads)",
            "Include detailed docstrings with Args, Returns, and Examples",
            "Handle errors gracefully and return helpful error messages",
            "Use environment variables for sensitive data (API keys, tokens)",
            "Functions run in the user's environment (inherits VPN, credentials, etc.)",
            "For internal APIs: No special VPN setup needed - inherits connection",
            f"Test locally first: cd to {tool_dir}, run 'uv sync', then test imports"
        ],
        
        "next_steps": {
            "1_show_path": f"Display clickable path: 'Created Python utility: {tool_dir}/{module_name}.py (click to review)'",
            "2_test": f"Offer to run: cd {tool_dir} && uv sync (MUST use required_permissions: ['all'])",
            "3_usage": f"Show import example: from {module_name} import function_name",
            "4_commit": "Remind user: Commit .cursor/ directory to git so your team gets this tool automatically!"
        }
    }
    
    return guide


@mcp.tool()
def get_mcp_tool_guide(
    tool_type: Literal["http_api", "shell"],
    user_requirements: str,
    tool_name: str,
    project_path: str = None
) -> dict:
    """Get a comprehensive guide for building a custom Python utility
    
    This tool provides patterns, reference implementations, and best practices
    that Cursor can use to write a custom Python utility matching the user's exact needs.
    
    All tools are created in the project's .cursor/tools/ directory so they
    can be committed to git and shared with your team.
    
    IMPORTANT - Conversational Flow:
    1. Ask user: "I'll create {tool_name} in {project}/.cursor/tools/. Proceed?"
    2. After confirmation, write the files using the reference_implementation
    3. Show clickable path: "Created: {path}/{module_name}.py (click to review)"
    4. Remind: "Commit .cursor/ to git for your team!"
    
    This does NOT create any files - it only returns code and patterns.
    
    Args:
        tool_type: Type of tool to build (http_api or shell)
        user_requirements: What the user wants the tool to do (in plain English)
        tool_name: Name for the tool (e.g., "github", "kibana")
        project_path: Path to the project directory (REQUIRED - provide workspace root)
    
    Returns:
        Complete guide including:
        - project_structure: What files to create and where
        - reference_implementation: Actual code for each file (use this to write files)
        - patterns: How to structure each component
        - best_practices: Security, error handling, configuration
        - next_steps: What to do after creating the tool
    
    Example:
        User: "Create a weather tool called weather-tool"
        Cursor: "I'll create weather-tool in /path/to/project/.cursor/mcp-tools/. Proceed?"
        User: "Yes"
        Cursor: *creates files*
        Cursor: "Created: /path/.cursor/mcp-tools/weather-tool/server.py (click to review)"
        Cursor: "Commit .cursor/ to git for your team!"
    """
    return _get_mcp_tool_guide_impl(tool_type, user_requirements, tool_name, project_path)


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


def _update_cursorrules_for_commands():
    """Update or create .cursorrules to tell Cursor about saved commands
    
    This ensures Cursor automatically checks .cursor/commands.json when users
    ask about running, building, testing, or deploying.
    
    DEPRECATED: Use _update_cursorrules_for_commands_at_path() instead.
    """
    cursorrules_file = Path(".cursorrules")
    _update_cursorrules_for_commands_at_path(cursorrules_file)


def _update_cursorrules_for_commands_at_path(cursorrules_file: Path):
    """Update or create .cursorrules at specific path
    
    Args:
        cursorrules_file: Path object pointing to .cursorrules file
    """
    # GENERIC instructions (no hardcoded paths - must work when committed to git!)
    commands_instruction = """
# Saved Commands (cursor-extend)

This project has saved commands in .cursor/commands.json.

When the user asks about running, building, testing, deploying, or executing commands,
check the saved commands first.

**IMPORTANT: Always pass project_path parameter**

When calling cursor-extend tools, use the workspace root (the directory you opened in Cursor):

```
list_remembered_commands(project_path="<workspace_root>")
remember_command(name="...", command="...", project_path="<workspace_root>")
forget_command(name="...", project_path="<workspace_root>")
```

Replace <workspace_root> with the absolute path to this project's root directory.

**Why:** This ensures commands are saved in THIS project, not globally.

**Note:** These instructions are generic so this file can be committed to git.
Each person's workspace_root will be different (wherever they cloned the repo).
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
    description: str = "",
    project_path: str = None
) -> dict:
    """Remember a shell command for easy recall - No Python or MCP knowledge needed!
    
    Stores simple commands in .cursor/commands.json in your project directory.
    
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
        project_path: Path to the project directory (REQUIRED - provide workspace root)
    
    Returns:
        Confirmation with usage instructions, or error if project_path not provided
    
    Example:
        remember_command("deploy", "./scripts/deploy.sh staging", "Deploy to staging", 
                        project_path="/Users/user/Projects/my-app")
    
    Note:
        project_path is required - the function will return an error if not provided.
    """
    try:
        # If no project_path provided, return error
        if project_path is None:
            return {
                "status": "error",
                "error": "project_path parameter is required",
                "message": "Project directory required to save command",
                "instructions": (
                    "Please provide the project_path parameter with the workspace root directory.\n\n"
                    "Example:\n"
                    "remember_command(\n"
                    "    name=\"build\",\n"
                    "    command=\"npm run build\",\n"
                    "    description=\"Build the project\",\n"
                    "    project_path=\"/Users/username/Projects/my-project\"\n"
                    ")\n\n"
                    "This will create:\n"
                    "- /Users/username/Projects/my-project/.cursor/commands.json\n"
                    "- Command can be committed to git for team sharing!"
                )
            }
        
        # Resolve project path
        project_dir = Path(project_path).resolve()
        
        # Safety check: Don't save to cursor-extend's own installation directory
        if (project_dir / "src" / "mcp_extend" / "server.py").exists():
            return {
                "status": "error",
                "message": "This looks like cursor-extend's installation directory",
                "detected_path": str(project_dir),
                "tip": "Please provide the path to YOUR project, not cursor-extend's directory.",
                "example": "remember_command(name='build', command='npm run build', project_path='/Users/you/Projects/your-app')"
            }
        
        # Safety check: Warn if path looks suspicious
        path_str = str(project_dir)
        if any(suspicious in path_str.lower() for suspicious in ['/tmp/', '\\temp\\', '/.cache/', '\\.cache\\', '/uvx-', '\\uvx-']):
            return {
                "status": "warning",
                "message": "Path looks like a temporary directory",
                "detected_path": path_str,
                "tip": "Are you sure you want to save commands here? This doesn't look like a project directory.",
                "suggestion": "Please confirm the project path or provide the correct path to your project."
            }
        
        # Ensure .cursor directory exists in the project
        cursor_dir = project_dir / ".cursor"
        cursor_dir.mkdir(exist_ok=True)
        
        # Load existing commands
        commands_file = cursor_dir / "commands.json"
        if commands_file.exists():
            with open(commands_file, 'r') as f:
                data = json.load(f)
        else:
            data = {"commands": {}}
        
        # Add/update command
        data["commands"][name] = {
            "command": command,
            "description": description or name
        }
        
        # Save
        with open(commands_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Update .cursorrules to ensure Cursor checks saved commands
        cursorrules_file = project_dir / ".cursorrules"
        _update_cursorrules_for_commands_at_path(cursorrules_file)
        
        full_path = str(commands_file.resolve())
        
        return {
            "status": "success",
            "message": f"✅ Saved command '{name}'!",
            "command_saved": {
                "name": name,
                "command": command,
                "description": description or name
            },
            "files_updated": {
                "commands": full_path,
                "rules": str(cursorrules_file.resolve())
            },
            "usage": f"Just say '{description or name}' or 'run {name}' to execute",
            "next_steps": [
                f"📁 View/edit commands: {full_path}",
                "💡 Commit .cursor/ and .cursorrules to git to share with your team!",
                "🎯 Add more commands or just start using them"
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to save command '{name}'"
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
USER: "discover commands in this project"
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


def main():
    """Main entry point for the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()

