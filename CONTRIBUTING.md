# Contributing to cursor-extend

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Git

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/mazzucci/cursor-extend
cd cursor-extend

# Install dependencies
uv sync

# Run tests
uv run pytest -v
```

### Project Structure

```
cursor-extend/
├── src/
│   └── mcp_extend/
│       ├── __init__.py
│       ├── server.py              # Main MCP server with tools
│       ├── generator.py           # Tool generation logic
│       └── templates/             # Jinja2 templates for tool generation
│           ├── basic_function.py.jinja
│           ├── http_api.py.jinja
│           ├── file_operations.py.jinja
│           ├── pyproject.toml.jinja
│           └── README.md.jinja
├── tests/
│   └── test_generator.py         # Test suite
├── docs/
│   ├── MVP_USER_STORIES.md        # Launch features
│   └── POST_MVP_IMPROVEMENTS.md   # Future roadmap
├── .cursor/
│   ├── commands.json              # Example saved commands
│   ├── mcp.json                   # Project-level MCP config
│   └── TEST_INSTRUCTIONS.md       # Testing notes
├── .cursorrules                   # Project rules for Cursor
├── pyproject.toml                 # Package configuration
└── README.md                      # Main documentation
```

---

## 🧪 Running Tests

### Run all tests:
```bash
uv run pytest -v
```

### Run specific test file:
```bash
uv run pytest tests/test_generator.py -v
```

### Run with coverage:
```bash
uv run pytest --cov=mcp_extend --cov-report=html
```

### Test the MCP server locally:
```bash
# Run the server directly
uv run cursor-extend

# Or use Python module
uv run python -m mcp_extend.server
```

---

## 🔧 Testing in Cursor

### Local Development Setup

1. **Update your `~/.cursor/mcp.json`:**

```json
{
  "mcpServers": {
    "cursor-extend-local": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/cursor-extend",
        "cursor-extend"
      ]
    }
  }
}
```

2. **Restart Cursor**

3. **Test the tools:**
```
# In Cursor chat:
"What MCP tools are available?"
"List remembered commands"
"Remember this command: echo 'test'"
```

---

## 📝 Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints where possible
- Write docstrings for all public functions
- Keep functions focused and small

### Example:

```python
def remember_command(
    name: str,
    command: str,
    description: str = ""
) -> dict:
    """Remember a shell command for easy recall
    
    Args:
        name: Short name to recall command
        command: The shell command to run
        description: Human-readable description
    
    Returns:
        Dictionary with status and details
    """
    # Implementation...
```

### Template Style

- Use clear, descriptive variable names
- Include comprehensive docstrings in generated code
- Provide helpful error messages
- Add security best practices in comments

---

## 🎯 What to Contribute

### High Priority

**Simple Improvements:**
- Documentation fixes (typos, clarity)
- Test coverage improvements
- Bug fixes
- Error message improvements

**New Templates:**
- Additional tool templates (with security-first design)
- Must include: validation, error handling, examples
- GitHub, Kubernetes, database templates welcome

**Platform Support:**
- Windows compatibility fixes
- Cross-platform path handling
- Platform-specific testing

### Medium Priority

**New Features (check roadmap first):**
- Simple command discovery (file parsing)
- Personal command support (`.cursor/commands.local.json`)
- Tool validation improvements

### Lower Priority (Discuss First)

**Major Features:**
- Investigation workflows
- Multi-tool orchestration
- AI-powered discovery

**Please open an issue first to discuss scope and approach.**

---

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try with latest version
3. Test with minimal reproduction

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what's broken.

**To Reproduce**
Steps to reproduce:
1. Run command X
2. See error Y

**Expected behavior**
What should happen instead.

**Environment**
- OS: [e.g., macOS 14.1]
- Python version: [e.g., 3.11.6]
- cursor-extend version: [e.g., 0.1.0]
- Cursor version: [e.g., 0.41.0]

**Additional context**
Logs, screenshots, etc.
```

---

## 💡 Requesting Features

### Feature Request Template

```markdown
**Problem to solve**
What pain point does this address?

**Proposed solution**
How would this feature work?

**Use case**
Real-world example of how you'd use it.

**Alternatives considered**
What other approaches did you think about?
```

---

## 🔀 Pull Request Process

### Before Submitting

1. **Create an issue** describing what you plan to do
2. **Fork the repository**
3. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
4. **Make your changes**
5. **Add tests** for new functionality
6. **Run tests** (`uv run pytest -v`)
7. **Update documentation** if needed

### PR Guidelines

**Good PR:**
- Focuses on one thing
- Includes tests
- Updates docs
- Has clear commit messages
- Passes CI checks

**PR Template:**

```markdown
**What does this PR do?**
Brief description.

**Why is this needed?**
Context and motivation.

**How was this tested?**
Manual testing steps + automated tests.

**Checklist:**
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
- [ ] No breaking changes (or documented)
```

### Commit Message Style

```
type(scope): Short description

Longer explanation if needed.

Fixes #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

Examples:
- `feat(templates): Add GitHub integration template`
- `fix(generator): Handle invalid tool names`
- `docs(readme): Update installation instructions`

---

## 📋 Testing Checklist for Major Changes

Before submitting PR with major changes:

- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Tested in actual Cursor (not just unit tests)
- [ ] Works on fresh project (not just your dev setup)
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Error messages are helpful
- [ ] Edge cases handled

---

## 🎨 Template Contribution Guidelines

If contributing new tool templates:

### Requirements:

1. **Security-first design:**
   - Input validation on all parameters
   - No arbitrary code execution
   - Safe defaults
   - Clear security notes in README

2. **Complete implementation:**
   - `{type}.py.jinja` template
   - Example usage in template README
   - Error handling
   - Type hints
   - Comprehensive docstrings

3. **Documentation:**
   - When to use this template
   - Security considerations
   - Configuration options
   - Example customizations

4. **Testing:**
   - Test that template renders correctly
   - Generated code has valid syntax
   - Example runs successfully

### Template Checklist:

- [ ] Security: Input validation, no eval/exec, safe defaults
- [ ] Documentation: Clear use cases, security notes, examples
- [ ] Error handling: Graceful failures, helpful messages
- [ ] Testing: Template renders, code is valid, runs correctly
- [ ] Examples: Real-world use case demonstrated

---

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks
- Trolling or inflammatory comments
- Publishing others' private information

---

## 📞 Getting Help

**Questions about development?**
- Open a [discussion](https://github.com/mazzucci/cursor-extend/discussions)
- Tag with `question` label

**Stuck on something?**
- Check existing issues/discussions first
- Provide context and what you've tried
- We're here to help!

---

## 🗺️ Roadmap

See [docs/POST_MVP_IMPROVEMENTS.md](docs/POST_MVP_IMPROVEMENTS.md) for planned features and priorities.

**Want to work on something?**
1. Check the roadmap
2. Open an issue to discuss
3. Get feedback before investing time
4. Submit PR when ready

---

## 🙏 Thank You!

Every contribution helps make cursor-extend better for everyone. Whether it's:
- Bug reports
- Documentation fixes
- New features
- Template contributions
- Testing and feedback

**All contributions are valued!** 🚀

---

**Questions?** Open an issue or discussion. We're happy to help!
