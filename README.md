# cursor-extend ⚡

**Your project's commands, saved forever.**

Stop re-explaining the same build commands, deploy scripts, and test suites to Cursor every single day. Save once, works forever. Your whole team benefits.

---

<!-- 
TODO: Add demo GIFs here
- GIF 1: New engineer onboarding (clone → commands work immediately)
- GIF 2: Save command once, use forever
-->

---

## 😤 The Problem

**New Engineer's First Day:**

```
Engineer: "How do I build this?"
Senior Dev: "Oh, it's xcodebuild -workspace MyApp.xcworkspace -scheme..."
[Explains 5 flags]

Next Day:
Engineer: "What was that build command again?"
[Asks again, or tries to find it in Slack]

Next Week:
Engineer asks: "Run tests"
Cursor: *tries wrong command*
Engineer: *Explains again*
```

**Every new team member goes through this. Every single time.**

Cursor has no memory. Your project documentation is scattered across Slack, READMEs, and tribal knowledge.

---

## ✨ The Solution

### **One Person Sets Up, Everyone Benefits**

**Step 1:** Senior developer saves commands once
```
Developer A: "Remember: xcodebuild -workspace MyApp.xcworkspace..."
Cursor: ✅ Saved to .cursor/commands.json
Developer A: *Commits to git*
```

**Step 2:** New engineer clones repo
```
Developer B: *Clones repo, opens in Cursor*
Developer B: "Build the iOS app"
Cursor: ✅ *Runs the exact command* (no explaining needed!)
```

**Forever.**

---

## 🎯 What is cursor-extend?

**A setup tool that gives your project a memory.**

It's like project documentation that Cursor actually reads and executes.

**Two ways to save knowledge:**

### 1️⃣ **Simple Commands** (90% of use cases)
Save shell commands to `.cursor/commands.json`:
- Build scripts with complex flags
- Deploy commands with environment configs
- Test suites with specific options
- Docker compose commands
- Release workflows

**No code. Just JSON. Commit to git.**

### 2️⃣ **Custom MCP Tools** (Advanced)
Generate Python tools for operations that need logic:
- Internal API wrappers (with validation)
- Database queries (read-only, safe)
- File operations (restricted directories)
- Deploy scripts (with guardrails)

**cursor-extend generates the code. You add safety rules.**

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
git add .cursor/
git commit -m "Add project commands"
git push
```

**Done.** Everyone who clones the repo gets the commands automatically.

---

## 💡 Use Cases

### 🏗️ Onboarding New Engineers

**Before:**
- New engineer asks: "How do I build this?"
- Senior dev explains complex command
- New engineer writes it down (maybe)
- Next week: Asks again

**After:**
- New engineer clones repo
- Cursor already knows all commands
- Zero questions, instant productivity

**Value:** Onboarding time cut by hours.

---

### 📱 Complex Build Commands

**React Native iOS build:**
```bash
cd ios && 
pod install && 
cd .. && 
npx react-native run-ios --scheme MyApp --configuration Debug --simulator "iPhone 15 Pro"
```

**Save once:**
```
You: "Remember this as 'build-ios': [paste command]"
```

**Use forever:**
```
You: "Build iOS"
Cursor: ✅ *Runs exact command*
```

**No more:**
- Re-explaining flags
- Copy-pasting from Slack
- Looking up documentation
- Remembering simulator names

---

### 🚀 Deployment Workflows

**Staging deploy with multiple steps:**
```json
{
  "commands": {
    "deploy-staging": "./scripts/deploy.sh staging --region us-east-1",
    "deploy-prod": "./scripts/deploy.sh production --region us-east-1 --confirm",
    "rollback": "./scripts/rollback.sh"
  }
}
```

**Everyone on the team can deploy. Safely. Consistently.**

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

When cursor-extend saves a command:

1. **Creates `.cursor/commands.json`** (stores commands)
2. **Updates `.cursorrules`** (tells Cursor to check commands)
3. **Cursor automatically reads these files** when you open the project

**No runtime dependency. No server. Just files in git.**

### **Your Repo Structure:**

```
my-project/
  ├── .cursor/
  │   └── commands.json          ← Commands (commit this!)
  ├── .cursorrules               ← Auto-updated (commit this!)
  ├── .gitignore                 ← Optionally ignore .cursor/commands.local.json
  └── ... (your code)
```

### **For Advanced Users:**

You can also generate custom MCP tools in `.mcp-tool/` directory:
- Python-based tools with validation logic
- API wrappers with auth and rate limiting
- Database query helpers (read-only, safe)
- File operation tools (restricted directories)

These tools give you full control: validation, restrictions, audit logging, transformations.

---

## 📦 What You Can Save

### ✅ Build Commands
- `npm run build`
- `cargo build --release`
- `./gradlew assembleRelease`
- Complex xcodebuild commands

### ✅ Test Commands
- `npm test`
- `pytest -v`
- `go test ./...`
- E2E test suites

### ✅ Deploy Scripts
- `./deploy.sh staging`
- `kubectl apply -f k8s/`
- `terraform apply`

### ✅ Development Workflows
- `docker-compose up -d`
- `npm run dev`
- Database migrations
- Code generation scripts

### ✅ Anything You Run Repeatedly
- Git workflows
- Release processes
- Cleanup scripts
- Environment setup

---

## 🔧 Available Tools

When you install cursor-extend, you get these tools in Cursor:

**Command Management:**
- `remember_command(name, command, description)` - Save a command
- `list_remembered_commands()` - See all saved commands
- `forget_command(name)` - Remove a command

**Advanced Features:**
- `discover_project_commands()` - AI analyzes project, suggests commands to save
- `get_mcp_tool_guide(...)` - Generate custom MCP tools with logic
- `validate_mcp_tool(path)` - Validate generated tools
- `add_tool_to_cursor_config(...)` - Auto-configure tools

**Just ask Cursor naturally:**
- "Remember this command: npm run build"
- "What commands are saved in this project?"
- "Create a tool for api.company.com/debug"

---

## 🤝 Team Workflow

### **Perfect for:**

✅ **Onboarding new engineers**
- Commands are discoverable immediately
- No tribal knowledge required
- Productive on day 1

✅ **Complex projects**
- React Native, iOS, Android builds
- Multi-service deployments
- Microservices architectures

✅ **Growing teams**
- Junior devs get senior-level commands
- Consistent workflows across team
- Knowledge doesn't leave when people do

✅ **Documentation that works**
- Lives in git, evolves with project
- Cursor actually uses it
- Never gets outdated

---

## 💡 Pro Tips

### **Start Simple**
```
1. Save 3-5 commands you use daily
2. Commit to git
3. Watch team adoption grow organically
```

### **Use Descriptive Names**
```json
{
  "build-ios-simulator": "cd ios && pod install && ...",
  "build-ios-device": "cd ios && pod install && ...",
  "test-unit": "npm test",
  "test-e2e-headless": "npm run test:e2e -- --headless"
}
```

### **Add Comments (via descriptions)**
cursor-extend saves metadata with each command. Use the description field to add context.

### **Personal Commands**
Want personal commands that don't get committed?
- Use `.cursor/commands.local.json` (add to `.gitignore`)
- Future feature, coming soon!

---

## 🎓 Advanced: Custom MCP Tools

For operations that need **logic, validation, or restrictions**, generate custom MCP tools:

### **Example: Internal API Wrapper**

```
You: "Create a tool for api.company.com/debug/customer"

Cursor: *Generates Python MCP tool*
```

**Then you customize it:**
- Add validation (ensure customer IDs are valid)
- Add rate limiting (prevent API abuse)
- Add audit logging (track who queries what)
- Hide sensitive fields (SSN, credit cards)
- Read-only access only

**Result:** Safe, controlled access to internal APIs. Junior devs can query data without breaking anything.

### **When to Use Custom Tools:**
- ✅ Need input validation
- ✅ Need rate limiting
- ✅ Need audit trails
- ✅ Need data transformations
- ✅ Need access restrictions

### **When to Use Simple Commands:**
- ✅ Shell commands work as-is
- ✅ No logic needed
- ✅ Just want memory

**Rule of thumb:** Start with simple commands. Upgrade to tools when you need control.

---

## 🔍 How cursor-extend Actually Works

### **The "Guide-as-a-Service" Pattern**

cursor-extend is **not a traditional tool**. It's a **guide** for Cursor.

**Traditional MCP tools:**
```
User: "Get weather"
Tool: *Makes HTTP request*
Tool: *Returns data*
```

**cursor-extend:**
```
User: "Create a tool for my API"
cursor-extend: *Returns instructions to Cursor*
Cursor: *Reads instructions*
Cursor: *Writes the actual tool code*
```

**Why this is powerful:**
- ✅ Cursor does the work (you just provide requirements)
- ✅ Tools are generated as real code (you can review/edit)
- ✅ No black box magic (everything is transparent)
- ✅ Tools improve as Cursor's AI improves

**You describe what you want. Cursor builds it. cursor-extend teaches Cursor how.**

---

## 📚 What's Next?

### **After Launch:**

Based on user feedback, we may add:
- Simple command discovery (parse package.json, Makefile)
- Personal/local commands (git-ignored)
- More tool templates (GitHub, Kubernetes, databases)
- Investigation workflows (debug production issues)
- Guide marketplace (share workflows)

**But first:** We're validating that command memory solves real problems.

**Your feedback shapes the roadmap.** 🚀

---

## 🛠️ Installation Notes

### **Requirements:**
- Cursor IDE (with MCP support)
- Python 3.10+ (for generated tools)
- `uv` or `pip` (for package management)

### **Platform Support:**
- ✅ macOS (tested)
- ✅ Linux (tested)
- ⚠️ Windows (should work, not extensively tested)

### **For Local Development:**

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, testing, and contribution guidelines.

---

## 📚 Learn More

- [FastMCP Documentation](https://gofastmcp.com) - Framework powering cursor-extend
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification
- [Cursor IDE](https://cursor.sh/) - AI-first code editor

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

Built on [FastMCP](https://gofastmcp.com) by the FastMCP team.

---

## 💬 Feedback & Support

- 🐛 **Found a bug?** [Open an issue](https://github.com/mazzucci/cursor-extend/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/mazzucci/cursor-extend/discussions)
- ⭐ **Like it?** Star the repo!

---

**Stop re-teaching Cursor every day. Your project remembers.** ⚡
