# cursor-extend ⚡

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

## 🏗️ Architecture: Tool-as-Guide Pattern

cursor-extend implements the **"Tool-as-Guide"** pattern - a design where the MCP tool actively orchestrates workflows rather than passively returning data.

**Traditional MCP Tool (Passive):**
```python
# Returns data, AI figures out what to do
mcp.tool() → {"code": "...", "config": "..."}
```

**Tool-as-Guide (Active):**
```python
# Returns instructions + data
mcp.tool() → {
    "instructions_for_cursor": "Step 1: Show user what you'll create. 
                                 Step 2: ASK for confirmation. 
                                 Step 3: Write files...",
    "reference_implementation": {...},
    "next_steps": {...}
}
```

**Why this matters:**
- 🧠 **Workflow logic lives in the tool** - Not scattered across AI prompts
- 🎯 **Consistent execution** - Same steps every time, not dependent on AI interpretation  
- 🔧 **Easier to debug** - Workflow is code, not emergent behavior
- 📈 **Scales better** - Complex workflows don't overwhelm context window

Examples in cursor-extend:
- `get_mcp_tool_guide()` - Guides Cursor through tool creation workflow
- `discover_project_commands()` - Provides analysis steps and presentation format

This pattern is particularly useful for multi-step workflows where consistency matters more than flexibility.

### Real-World Example: Medical Triage (Conceptual)

> **⚠️ Disclaimer**: This is a simplified conceptual example to illustrate the pattern's value in high-stakes domains. Real medical AI systems require clinical expertise, regulatory approval, and extensive validation. This is NOT production medical software.

Consider a medical triage system. Without the Tool-as-Guide pattern, an AI might skip vital signs, miss red flags, or jump to conclusions. With the guide pattern, clinical protocols are enforced:

```python
@mcp.tool()
def triage_workflow(session_id: str, user_input: str) -> dict:
    """Guide AI through medical triage protocol"""
    
    session = get_session(session_id)
    
    # CRITICAL: Red flags must be checked first
    if not session.state.get("red_flags_screened"):
        return {
            "action": "screen_red_flags",
            "prompt": "Before we continue, do you have: severe chest pain, "
                     "difficulty breathing, or loss of consciousness?",
            "required": True
        }
    
    # Immediate escalation if red flags present
    if session.state.get("red_flags_present"):
        return {
            "action": "emergency_escalation",
            "message": "Please call 911 immediately.",
            "severity": "CRITICAL"
        }
    
    # Standard protocol steps (cannot skip)
    if not session.state.get("vital_signs_gathered"):
        return {
            "action": "request_vital_signs",
            "required": True,
            "cannot_skip": True  # Protocol enforcement
        }
    
    # Only after all required steps
    return {
        "action": "provide_assessment",
        "protocol_followed": True,
        "audit_trail": session.get_audit_log()
    }
```

**Why this matters:**
- ✅ **Mandatory protocol steps** cannot be skipped
- ✅ **Red flag screening** happens first, always  
- ✅ **Audit trail** shows compliance for legal/regulatory review
- ✅ **Consistency** across all cases, regardless of AI model

This pattern applies to any domain where reliability and compliance are critical: financial trading, legal review, deployment pipelines, and more.

**🍕 Want to see it in action?** Check out the [pizza ordering demo](https://github.com/mazzucci/mcp-tool-as-guide-pizza) - a complete, runnable implementation of the Tool-as-Guide pattern with an animated demo!

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
