# cursor-extend ⚡

> **⚠️ PREVIEW**: This project is currently in preview. APIs and features may change. Not yet recommended for production use.

**Cursor writes code. cursor-extend lets it do a lot more!**

Give Cursor access beyond the codebase: run commands, check GitHub CI, query your APIs.

Stop copy-pasting terminal output and errors. Cursor gets the info itself.

cursor-extend saves commands and generates Python utilities in `.cursor/`. Commit to git. Your whole team benefits. Forever.

---

<!-- 
TODO: Add demo GIFs here
**GIF 1: Autonomous Iteration**
*Cursor saves command, runs build, sees error, fixes it, repeats until passing*

**GIF 2: Team Onboarding**  
*New engineer clones repo → commands work immediately → zero setup*

-->

---

### **Bonus: Team Onboarding**

Commit `.cursor/commands.json` to git. New team members get commands automatically. No Slack threads. No tribal knowledge.

---

## 🎯 What is cursor-extend?

**A tool that helps you save project commands to `.cursor/commands.json`.**

cursor-extend makes it easy to:
- ✅ Save commands with simple natural language ("Remember: npm run build")
- ✅ Create `.cursor/commands.json` that Cursor reads automatically
- ✅ Generate custom Python utilities for complex operations
- ✅ Share commands with your team via git

### 1️⃣ **Simple Commands**
Save shell commands to `.cursor/commands.json`:
- Build scripts with complex flags
- Test suites with specific options
- Docker compose up/down
- Database migrations
- Development server commands

**Supports auto discovery, or save manually. No code generated, just JSON.**

### 2️⃣ **Custom Python Utilities** (Advanced)
Generate Python modules for operations that need logic:
- Internal API wrappers (with validation)
- CLI tool wrappers (like GitHub's `gh`)
- HTTP API clients (with auth and rate limiting)
- Custom workflow automation

**Pure Python modules - no MCP dependency. Works in Cursor, terminal, scripts, anywhere.**

---

## 🚀 Quick Start (60 Seconds)

### 1. Install cursor-extend

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "cursor-extend": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/mazzucci/cursor-extend",
        "cursor-extend"
      ]
    }
  }
}
```

### 2. Restart Cursor

Close and reopen Cursor completely.

### 3. Save Your First Command

In any Cursor project:

```
You: "Remember this command: npm run build"
Cursor: ✅ Saved to .cursor/commands.json!

You: "Build the project"
Cursor: *Runs npm run build*
```

### 4. Share with Your Team

```bash
git add .cursor/ .cursorrules
git commit -m "Add project commands"
git push
```

**Done.** Everyone who clones the repo gets the commands automatically.

---

## 🏗️ Architecture: Pure Tool-as-Guide Implementation

cursor-extend is a **pure implementation** of the **"Tool-as-Guide"** pattern - MCP tools provide step-by-step instructions, and Cursor executes them.

**What makes it "pure":**
- ⚡ **Tools never write files** - They provide instructions for Cursor to write files
- 🎯 **Cursor stays in control** - User sees all changes, transparent workflow
- 🧠 **Workflow logic in the tool** - Instructions are consistent and testable
- 📝 **Confirmation required** - Cursor always asks user before making changes

**How it works:**

```
User: "Remember command: npm run build"
          ↓
Tool: remember_command() returns {
    "instructions_for_cursor": "Ask user: 'Save to .cursor/commands.json?'
                                 Step 1: Read/create .cursor/commands.json
                                 Step 2: Add command entry
                                 Step 3: Write file
                                 Step 4: Update .cursorrules...",
    "command_entry": {...},
    "cursorrules_content": "..."
}
          ↓
Cursor: "I'll save 'build' to .cursor/commands.json. Proceed?"
          ↓
User: "Yes"
          ↓
Cursor: *Writes files following the instructions*
          ↓
Cursor: "✅ Saved! Commit .cursor/ to git for your team."
```

**Benefits:**
- ✅ **Simpler tool code** - No file I/O, no path resolution
- ✅ **Better UX** - User sees Cursor make changes
- ✅ **No conflicts** - Cursor owns all file modifications
- ✅ **True separation** - Tool = guide, Cursor = executor

**Learn more about this pattern:**
- 📖 [Full Pattern Documentation](https://github.com/mazzucci/tool-as-guide) - Complete guide with comparisons and use cases

---

## 💡 Use Cases

### 🤖 Autonomous Development (The Main Benefit)

**You:** "Add email validation to the signup form"

**Cursor:**
1. Adds validation function
2. Runs `npm run build` → TypeScript error: "Property 'email' not found"
3. Fixes the type definition
4. Runs `npm run build` → Success
5. Runs `npm test` → 1 test fails (invalid email passes)
6. Fixes the regex pattern
7. Runs `npm test` → All pass
8. "✅ Email validation added and tested"

**You never touched the terminal.** Cursor iterated autonomously because it knows your commands.

**Value:** 10x faster development. Cursor debugs its own work.

---

### 📱 Complex Commands (No More Copy-Paste)

**React Native iOS:**
```bash
cd ios && pod install && cd .. && 
npx react-native run-ios --scheme MyApp --configuration Debug --simulator "iPhone 15 Pro"
```

**Save once:** `"Remember: build-ios"`

**Use forever:** Cursor runs it perfectly. No flags to remember. No Slack archaeology.

---

### 🏗️ Team Onboarding

Commit commands to git. New engineers clone → Cursor knows everything. Zero Slack questions.

---

### 🧪 Test Suites

```json
{
  "commands": {
    "test": "npm test",
    "test-e2e": "npm run test:e2e -- --headless",
    "test-integration": "docker-compose -f docker-compose.test.yml up --abort-on-container-exit",
    "test-coverage": "npm run test -- --coverage --watchAll=false"
  }
}
```

**No more "which test command should I run?"**

---

## 🎯 How It Works

### **The Magic: Cursor Reads Your Project Files**

When you save a command with cursor-extend:

1. **Creates `.cursor/commands.json`** in your project (stores commands)
2. **Updates `.cursorrules`** in your project (tells Cursor to check commands)
3. **Cursor automatically reads these files** when you open the project

**No runtime dependency. No server. Just files in git.**

> **💡 Why This Works So Well**
> 
> Cursor has powerful built-in features that many users don't know about:
> - **`.cursorrules`** - Project-specific instructions Cursor reads automatically
> - **MCP (Model Context Protocol)** - Extensible tool system for AI editors
> - **Project-level configs** - Settings that travel with your code
> 
> cursor-extend helps you take advantage of these native Cursor capabilities—and extends them with custom tools when needed. We're building on Cursor's solid foundations, not working around them.

---

### **Your Repo Structure:**

```
my-project/
  ├── .cursor/
  │   ├── commands.json          ← Commands (commit this!)
  │   └── tools/                 ← Python utilities (commit this!)
  │       └── github/            ← Example: PR lint checker
  ├── .cursorrules               ← Auto-updated (commit this!)
  └── ... (your code)
```

### **For Advanced Users:**

You can also generate custom Python utilities in `.cursor/tools/`:
- Pure Python modules - no MCP dependency
- Works in Cursor's code execution, terminal, scripts, anywhere
- Validation logic, rate limiting, transformations
- Commit to git - your whole team gets them

**Templates available:**
- `http_api` - Async HTTP clients (uses httpx)
- `shell` - CLI tool wrappers (uses subprocess)

See [detailed examples](docs/EXAMPLES.md) for GitHub PR checkers, weather APIs, and more.

---

## 🔧 Available Tools

When you install cursor-extend, you get these tools in Cursor:

**Core Functions:**
- `remember_command(name, command, description, project_path)` - Save a command to `.cursor/commands.json`
- `discover_project_commands()` - AI analyzes project and suggests commands to save
- `get_mcp_tool_guide(tool_type, requirements, name, project_path)` - Generate Python utilities

**Just ask Cursor naturally:**
- "Remember this command: npm run build"
- "Discover commands in this project"
- "Create a GitHub PR checker using the shell template"

---

## 🎓 Advanced: Custom Python Utilities

### 💡 Inspired By Recent Research

cursor-extend generates pure Python utilities instead of MCP servers, inspired by 
research from [Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp) 
and [Cloudflare](https://blog.cloudflare.com/code-mode/) showing LLMs perform better 
writing code than making tool calls.

cursor-extend bridges the gap by making these patterns easy to use with simple commands.

**Key benefits:**
- **Context efficiency** - Data processed in code, only summaries enter LLM context
- **Better performance** - LLMs excel at writing Python (millions of examples in training)
- **Portability** - Works anywhere Python runs, not just in Cursor

---

### **Example: GitHub PR Lint Checker**

```
You: "Create a GitHub PR checker using the shell template"

Cursor: *Generates pure Python module in .cursor/tools/github/*
```

**The generated module:**
- Wraps `gh` CLI with subprocess
- Has functions like `get_pr_lint_errors()`
- Pure Python - no MCP dependency
- Works in Cursor, terminal, scripts, anywhere

**Then you can:**
```python
# Cursor writes this code and runs it
from github import get_pr_lint_errors

errors = get_pr_lint_errors()
print(errors)
# Only the output enters Cursor's context
```

**Result:** Cursor can autonomously check CI status, fix errors, and verify - all without you touching the terminal.

See [detailed examples](docs/EXAMPLES.md) for complete implementations.

---

### **When to Use Python Utilities:**
- ✅ Need to wrap CLI tools (gh, docker, kubectl)
- ✅ Need to query HTTP APIs with logic
- ✅ Need input validation or transformations
- ✅ Want data processing outside LLM context

### **When to Use Simple Commands:**
- ✅ Shell commands work as-is
- ✅ No logic or validation needed
- ✅ Just want Cursor to remember the command

**Rule of thumb:** Start with simple commands. Generate utilities when you need logic or want to process data efficiently.

---

## 🛠️ Development & Support

**Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

**Requirements:** Cursor IDE with MCP support • Python 3.10+ • Works on macOS/Linux (Windows mostly untested)

**Built with:** [FastMCP](https://gofastmcp.com) (cursor-extend is an MCP extension) • Generated utilities are pure Python

**Feedback:** [Issues](https://github.com/mazzucci/cursor-extend/issues) • [Discussions](https://github.com/mazzucci/cursor-extend/discussions) • ⭐ Star if useful!

**License:** MIT

---

**Cursor writes code. cursor-extend lets it do a lot more!** ⚡
