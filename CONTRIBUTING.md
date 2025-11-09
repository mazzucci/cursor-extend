# Contributing to cursor-extend

Thank you for considering contributing to cursor-extend! This project aims to democratize access to internal systems by making MCP tool creation accessible to everyone.

## 🎯 Project Vision

Make it trivial for anyone (engineers, support teams, business teams) to create MCP tools that enable conversational interaction with their systems.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management

### Setup

```bash
# Clone the repo
git clone https://github.com/mazzucci/cursor-extend
cd cursor-extend

# Install dependencies
uv sync --extra dev

# Run tests
uv run pytest -v
```

## 🔧 Development Workflow

### Making Changes

1. **Create a branch** for your feature/fix
2. **Make your changes** in the appropriate files:
   - `src/mcp_extend/server.py` - MCP tool definitions
   - `src/mcp_extend/generator.py` - Code generation logic
   - `src/mcp_extend/templates/` - Jinja2 templates for generated tools
3. **Add tests** in `tests/` if adding new features
4. **Update documentation** if changing behavior

### Testing

```bash
# Run all tests
uv run pytest -v

# Run specific test
uv run pytest tests/test_generator.py::test_generate_http_api_tool -v
```

### Code Style

- Follow PEP 8
- Use type hints where appropriate
- Write clear docstrings for all public functions
- Keep functions focused and single-purpose

## 📝 What to Contribute

### High Priority

- **New templates** - Add templates for common use cases (database queries, git operations, etc.)
- **Better error messages** - Make generation failures more helpful
- **Template customization** - Allow more configuration options when generating
- **Documentation improvements** - Especially real-world examples

### Ideas for New Templates

- `database_query` - Query databases (SQLite, PostgreSQL, etc.)
- `git_operations` - Git commands wrapped as MCP tools
- `cli_wrapper` - Wrap command-line tools as MCP tools
- `webhook` - Receive webhooks and expose data
- Your idea here!

### Template Guidelines

When adding a new template:

1. **Create the template** in `src/mcp_extend/templates/your_template.py.jinja`
2. **Update `list_available_templates()`** in `server.py` with:
   - Clear description
   - When to use it
   - Example use cases
   - Real-world impact
3. **Add a test** in `tests/test_generator.py`
4. **Generate an example** to verify it works
5. **Update documentation** in README.md

### Example: Adding a Database Template

```python
# src/mcp_extend/templates/database_query.py.jinja
from fastmcp import FastMCP
import sqlite3
from typing import List, Dict, Any

mcp = FastMCP("{{ tool_name }}")

@mcp.tool()
def query_db(sql: str) -> List[Dict[str, Any]]:
    """Execute a SQL query (read-only)"""
    # Implementation here
    pass
```

Then update `server.py`:

```python
"database_query": {
    "name": "Database Query",
    "description": "Query local databases with read-only access",
    "includes": ["query_db() - Execute SELECT queries safely"],
    "use_when": "You want to query databases conversationally",
    "examples": ["SQLite analysis", "Data exploration"]
}
```

## 🐛 Reporting Bugs

Found a bug? Please [open an issue](https://github.com/mazzucci/cursor-extend/issues) with:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Your environment** (OS, Python version, uv version)
- **Generated code** if relevant (sanitize any sensitive data)

## 💡 Feature Requests

Have an idea? [Open an issue](https://github.com/mazzucci/cursor-extend/issues) with:

- **Use case description** - What problem does this solve?
- **Proposed solution** - How should it work?
- **Alternatives considered** - What other approaches did you think about?
- **Real-world example** - How would you use this?

## 📄 Pull Request Process

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** following the guidelines above
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a PR** with:
   - Clear description of what changed and why
   - Link to related issue if applicable
   - Screenshots/examples if helpful

### PR Checklist

- [ ] Tests pass (`uv run pytest -v`)
- [ ] New features have tests
- [ ] Documentation updated if needed
- [ ] Examples generated and tested
- [ ] Code follows project style
- [ ] Commit messages are clear

## 🎨 Design Principles

1. **Simplicity first** - Prefer clear, simple code over clever abstractions
2. **Batteries included** - Generated tools should "just work"
3. **Learn by example** - Include working examples (like `get_weather`)
4. **Customization friendly** - Easy for users to modify generated code
5. **Security conscious** - Never hard-code credentials, warn about security implications

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions

## 📞 Questions?

- Open an issue for questions about contributing
- Start a discussion for architectural decisions
- Reach out to maintainers if unsure about anything

---

**Thank you for helping democratize access to internal systems!** 🙏






