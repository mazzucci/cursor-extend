# cursor-extend ⚡

**Cursor forgets. Your project remembers.**

Give Cursor a memory for your commands and APIs. Stop re-explaining the same build scripts, deploy commands, and API endpoints every single day.

**Save once. Use forever. Share with your team.**

### TL;DR

- 💨 **Simple commands:** Say "Remember: npm run build" → Never explain again  
- 🎯 **Controlled tools:** Create tools with validation, restrictions, safety guardrails
- 🔌 **APIs:** Only expose safe endpoints, validate inputs, audit access
- 📁 **File ops:** Search only specific folders, prevent accidental deletions
- 🤝 **Team sharing:** Commit to git → Everyone gets safe, consistent tools

**Key insight:** When you need control (not just memory), cursor-extend generates **code** - you decide what's exposed, add validation, restrictions, and create safe abstractions for your team.

---

## 😤 The Problem

**Cursor has no memory.** Every day, you re-explain the same things:

### Commands You Keep Re-Explaining:

> **You:** "Build my iOS app"  
> **Cursor:** *tries random xcodebuild commands*  
> **You:** "No, use THIS workspace, THIS scheme, THIS simulator..."  
> **Cursor:** ✅ Finally works

**Next day:** Cursor forgot everything. You explain again. 😤

### APIs You Keep Looking Up:

> **You:** "Check customer 12345"  
> **Cursor:** "Which endpoint?"  
> **You:** *Opens docs... searches... finds it...*  
> **You:** "It's GET api.company.com/debug/customer?id=X with Bearer auth"  
> **Cursor:** ✅ Finally works

**Next day:** Cursor forgot. You look it up again. 😤

### The Same Cycle for Everything:

- 🏗️ **Build commands** (iOS/Android with specific flags)
- 🚀 **Deploy scripts** (staging/production with your setup)
- 🔌 **Internal APIs** (endpoints you query daily)
- 🧪 **Test suites** (integration tests with specific config)
- 📦 **Release processes** (multi-step publishing workflows)

**Every. Single. Day.**

---

## ✨ The Solution

**Give Cursor a memory - save commands and APIs once, use them forever.**

### Save a Command (Simple):

> **You:** "Remember: xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15' clean build"
>
> **Cursor:** ✅ Saved to `.cursor/commands.json`

**Forever after:**

> **You:** "Build my iOS app"  
> **Cursor:** *Uses saved command* ✅

### Create an API Tool (Control + Customization):

> **You:** "Create a tool for api.company.com/debug/customer"
>
> **Cursor:** *Generates MCP tool with endpoint, params, auth*
> 
> **You customize:** Add validation, hide sensitive fields, audit queries

**Forever after:**

> **You:** "Check customer 12345"  
> **Cursor:** *Uses your safe, controlled tool* ✅

**Benefit:** This is code - you control what's exposed, validate inputs, transform responses. Not just memory!

**Commit to git → Your whole team gets safe, consistent access.**

---

## 🎯 What is cursor-extend?

**Extend Cursor with controlled, safe, customizable functionality.**

cursor-extend gives you two approaches:

1. **💨 Simple memory** (commands): Quick JSON storage for straightforward commands
2. **🎯 Controlled tools** (code): Full control, validation, restrictions when you need safety

**When you need control:** cursor-extend generates **Python code** - you decide what's allowed:
- 🔌 **APIs:** Only expose safe endpoints, validate inputs, hide sensitive data
- 📁 **File operations:** Search only specific folders, prevent dangerous operations
- 🚀 **Deploy commands:** Only staging (not prod), require confirmation
- 🗄️ **Database queries:** Read-only access, validate query patterns
- **Any operation:** Add logging, rate limiting, permission checks

Save once. Use forever. Share with your team via git.

### Two Approaches (cursor-extend picks the right one):

#### 💨 Simple Commands (90% of cases - Zero code!)

**Perfect for:** Shell commands that don't need logic

> **You:** "Remember: npm run build"  
> **Cursor:** ✅ Saved to `.cursor/commands.json`  
> 
> **Later:**  
> **You:** "build the app"  
> **Cursor:** *Runs npm run build* ✅

**Examples:**
- Build scripts: `xcodebuild -workspace...`
- Deploy commands: `./deploy.sh staging`
- Docker: `docker-compose up -d`
- Tests: `npm run test:e2e`

#### 🔌 API Tools (Controlled, Customizable Access)

**Perfect for:** APIs you need controlled, safe access to

> **You:** "Create a tool for api.company.com/debug/customer"  
> **Cursor:** *Generates MCP tool with endpoint, params, auth saved*  
> 
> **Forever after:**  
> **You:** "Check customer 12345"  
> **Cursor:** *Uses saved tool* ✅ (no docs lookup needed!)

**Why this is powerful (beyond just memory):**

🧠 **Memory:**
- ✅ Never look up endpoints/parameters again
- ✅ Auth configured once

🎯 **Control & Safety:**
- ✅ **Restrict what's exposed** (only safe endpoints, not dangerous ones)
- ✅ **Add validation** (ensure customer IDs are valid before calling)
- ✅ **Rate limiting** (prevent accidental API abuse)
- ✅ **Permission checks** (who can call what)

🎨 **Customization:**
- ✅ **Transform responses** (format data exactly how you need)
- ✅ **Add business logic** (combine multiple API calls)
- ✅ **Error handling** (graceful failures, helpful messages)
- ✅ **Logging/audit** (track who queries what)

🤝 **Safe Abstraction for Teams:**
- ✅ **Hide complexity** (support team uses "get_customer_info", doesn't need to know raw API)
- ✅ **Prevent mistakes** (can't accidentally call DELETE endpoints)
- ✅ **Consistent interface** (everyone uses the same safe wrapper)

**This is code, not just saved commands - you have full control over ANY operation!**

**Examples where control matters:**
- **APIs:** Customer debug (read-only), order status (validate IDs), metrics (rate limited)
- **File ops:** Search logs (only /var/log/myapp), read configs (not /etc/passwd)
- **Deploys:** Staging only (block prod), specific services only (validate names)
- **Database:** Customer queries (read-only replica, timeout 5s, validate IDs)
- **Admin tools:** Employee lookup (audit trail), feature flags (approval required)

---

## 🚀 Quick Start

### 1. Add to Cursor

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

**Note:** Repository is now published at [github.com/mazzucci/cursor-extend](https://github.com/mazzucci/cursor-extend).

For local development:

```json
{
  "mcpServers": {
    "cursor-extend": {
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

### 2. Restart Cursor

Close and reopen Cursor.

### 3. Discover Commands in Your Project

#### ⚡ The Magic Command: "cursor extend"

> **You:** "cursor extend"
>
> **Cursor:** *Analyzes package.json, README, Makefile, tech stack...*  
> "🔍 Found 8 commands in your project:
> - build-ios: npx react-native run-ios
> - build-android: npx react-native run-android
> - test: npm test
> - deploy-staging: ./scripts/deploy.sh staging
> - ..."
>
> **Cursor:** "Want me to save all of these?"
>
> **You:** "Yes"
>
> **Cursor:** ✅ Saved 8 commands! Your team can now use them.

**What `cursor extend` does:**
- ✅ Uses AI to intelligently discover commands (not rigid pattern matching)
- ✅ Understands your tech stack and suggests relevant commands
- ✅ Categorizes by complexity (simple commands vs. MCP tools)
- ✅ Offers to save everything at once

#### 💨 Or Save Commands Manually:

> **You:** "Remember this command: npm run build"

Cursor will use `remember_command()` to save it instantly:
- ✅ Stored in `.cursor/commands.json`
- ✅ Updates `.cursorrules` so Cursor automatically checks commands
- ✅ No Python, no MCP knowledge needed
- ✅ Just say "build" to run it anytime
- ✅ Commit to git, share with team

#### 🧠 API Tools (For Endpoint Memory):

> **You:** "Create a tool for api.company.com/debug/customer"

Cursor will:
1. ✅ Generate MCP tool with HTTP client
2. ✅ Save endpoint, parameters, auth
3. ✅ Offer to show code for review
4. ✅ Help you test locally
5. ✅ Add to Cursor config

**cursor-extend automatically picks the right approach!**

---

## 📁 Project Commands vs Global Tools

### 🎯 Project Commands (Simplest - Recommended)

**Stored in `.cursor/commands.json` in your project:**
```
my-project/
  ├── .cursor/
  │   └── commands.json      ← Simple JSON (commit to git!)
  ├── .cursorrules           ← Auto-updated to tell Cursor about commands
  └── ... (your code)
```

**Example:**
```json
{
  "commands": {
    "deploy": "./scripts/deploy.sh staging",
    "test": "npm run test:e2e",
    "build-ios": "cd ios && pod install && cd .. && npx react-native run-ios"
  }
}
```

**Benefits:**
- ✅ **Zero code required** - Just JSON
- ✅ **Automatic discovery** - `.cursorrules` updated for you
- ✅ **Team sharing** - Clone repo = get commands
- ✅ **Easy to edit** - No Python knowledge needed
- ✅ **Version controlled** - Evolves with project

**Perfect for:** 90% of use cases!

---

### 🧠 Project MCP Tools (When You Need Logic)

**Generated in your project directory:**
```
my-project/
  ├── .cursor/
  │   └── mcp.json           ← Loads MCP tool
  ├── .mcp-tool/             ← Python tool (commit to git!)
  │   ├── server.py
  │   └── pyproject.toml
  └── ... (your code)
```

**Perfect for:**
- API wrappers (need HTTP client)
- Data transformation (need logic)
- Complex workflows (need conditionals)
- Error handling/retries

---

### 🌍 Global Tools (Optional)

**For commands/tools used across all projects:**
```
~/cursor-mcp-tools/
  └── my-tool/               ← Available everywhere
```

**Perfect for:**
- Personal utilities
- Cross-project tools

---

## 💡 Real-World Use Cases

### 🏗️ Command Memory (Stop Re-Explaining Build Scripts)

**Before cursor-extend:**
```
You: "Build my iOS app"
Cursor: *tries wrong command*
You: "No, use xcodebuild -workspace MyApp.xcworkspace -scheme MyApp..."
      *explains all 5 flags again*
Cursor: ✅ Works

Tomorrow: Same cycle. Cursor forgot. 😤
```

**After cursor-extend:**
```
You (once): "Remember: xcodebuild -workspace MyApp.xcworkspace..."
Cursor: ✅ Saved!

Forever:
You: "Build my iOS app"
Cursor: ✅ Works perfectly (uses saved command)
```

**Common commands to save:**
- iOS/Android builds with specific configurations
- Deploy scripts: `./deploy.sh staging --region us-east-1`
- Test suites: `npm run test:e2e -- --env=staging`
- Docker: `docker-compose -f compose.prod.yml up -d`
- Release: `npm version patch && git push --tags && npm publish`

---

### 🔌 API Tools (Controlled Access, Not Just Memory)

**The real problem:** Internal APIs need safe, controlled access - not just remembering endpoints.

**Before cursor-extend:**
```
You: "Check customer 12345"
Cursor: "Which endpoint?"
You: *Opens internal wiki*
     *Searches "customer API"*
     *Finds outdated doc*
     *Asks in Slack: "What's the customer debug endpoint?"*
     *Waits 10 minutes*
     *Finally: "GET api.company.com/debug/customer?id=X"*
Cursor: ✅ Works

Tomorrow: Same thing. 😤

Also:
- Support accidentally calls DELETE endpoint 😱
- Junior dev queries prod database directly 😱
- No audit trail of who queried what 😱
```

**After cursor-extend:**
```python
# You (once): "Create a tool for api.company.com/debug/customer"
# Cursor generates, you customize:

@mcp.tool()
async def get_customer_info(customer_id: str) -> dict:
    """Get customer info - SAFE, controlled access"""
    
    # Validation - prevent mistakes
    if not customer_id.isdigit():
        return {"error": "Invalid customer ID"}
    
    # Only expose safe read-only endpoint (not DELETE!)
    endpoint = f"https://api.company.com/debug/customer?id={customer_id}"
    
    # Logging - audit trail
    log_query(user=os.getenv("USER"), customer_id=customer_id)
    
    # Transform response - hide sensitive data
    raw_data = await http_client.get(endpoint)
    return {
        "name": raw_data["name"],
        "status": raw_data["status"],
        # DON'T expose: SSN, credit card, etc.
    }

Forever:
You: "Check customer 12345"
Cursor: ✅ Instant, safe, audited result
```

**Why this is game-changing:**

🎯 **Control (This is the KEY difference):**
- ✅ **Only expose safe operations** (read-only, specific endpoints)
- ✅ **Validate inputs** (prevent invalid IDs, SQL injection, etc.)
- ✅ **Add rate limiting** (prevent accidental API abuse)
- ✅ **Audit all queries** (know who accessed what customer data)
- ✅ **Hide sensitive fields** (SSN, passwords, etc. never exposed)

🧠 **Memory (Yes, this too):**
- ✅ **No documentation hunts** (endpoints saved)
- ✅ **No Slack interruptions** ("What's the endpoint for X?")
- ✅ **No context switching** (stay in Cursor)

🤝 **Safe Team Abstraction:**
- ✅ **Support self-service** (can query via Claude Desktop, but SAFELY)
- ✅ **Junior devs protected** (can't accidentally delete data)
- ✅ **Consistent interface** (everyone uses same validated wrapper)
- ✅ **Team onboarding** (new devs get safe tools immediately)

**Common APIs to save:**
- **Customer debug:** Get order history, feature flags, account status
- **Internal dashboards:** Query metrics, deployment status, error rates
- **Admin tools:** Employee lookup, permission checks, audit logs
- **Infrastructure:** K8s pod status, service health, resource usage
- **Third-party APIs:** Your specific GitHub/Stripe/AWS queries

**Real impact:**
- **Developer:** Saves 5-10 min/day (no docs lookup)
- **Support team:** Saves 30+ engineer interruptions/week
- **New hires:** Get all APIs immediately on day 1

---

### 🔒 Controlled Operations (Not Just APIs!)

**The power of code:** Control applies to ANY operation, not just APIs.

**Example 1: Safe File Search**
```python
@mcp.tool()
def search_project_logs(pattern: str) -> list:
    """Search logs - but ONLY in safe directories"""
    
    # Restriction: Only search specific folders
    SAFE_DIRS = ["/var/log/myapp", "/tmp/debug-logs"]
    
    # Validation: Prevent dangerous patterns
    if ".." in pattern or "/" in pattern:
        return {"error": "Invalid search pattern"}
    
    results = []
    for safe_dir in SAFE_DIRS:
        # Search only within allowed directories
        results.extend(search_in_directory(safe_dir, pattern))
    
    return results

# Can't accidentally search /etc/passwd or delete files!
```

**Example 2: Deploy with Guardrails**
```python
@mcp.tool()
def deploy_service(service: str, environment: str) -> str:
    """Deploy - but with safety checks"""
    
    # Restriction: Only staging allowed
    if environment == "production":
        return {"error": "Use manual process for prod deploys"}
    
    # Validation: Known services only
    ALLOWED_SERVICES = ["api", "frontend", "worker"]
    if service not in ALLOWED_SERVICES:
        return {"error": f"Unknown service: {service}"}
    
    # Logging: Audit trail
    log_deployment(user=os.getenv("USER"), service=service, env=environment)
    
    # Execute safe deployment
    return run_deploy_script(service, environment)

# Junior devs can deploy staging safely, can't touch prod!
```

**Example 3: Database Queries with Limits**
```python
@mcp.tool()
def query_customer_data(customer_id: str) -> dict:
    """Query DB - but read-only and limited"""
    
    # Validation: Prevent SQL injection
    if not customer_id.isdigit():
        return {"error": "Invalid ID"}
    
    # Restriction: Read-only connection
    db = connect_readonly_replica()
    
    # Restriction: Specific query only (no arbitrary SQL)
    query = "SELECT name, email, status FROM customers WHERE id = ?"
    
    # Add timeout to prevent long-running queries
    result = db.execute(query, [customer_id], timeout=5)
    
    return result

# Can't run UPDATE/DELETE, can't query sensitive tables, can't DOS the DB!
```

**Why this matters:**
- ✅ Support can query data (but safely)
- ✅ Junior devs can deploy (but only staging)
- ✅ Anyone can search logs (but only safe directories)
- ✅ Full audit trail of who did what
- ✅ Impossible to accidentally break things

---

### 🤝 Combined Intelligence (Use Multiple Tools Together)

Once you've created controlled tools, use them together:

```
You: "Check logs AND customer debug info for order #12345"
Cursor: *Uses both safe tools, correlates data*

You: "Run tests AND deploy to staging if they pass"
Cursor: *Orchestrates workflow with your guardrails*

You: "Search for errors in the last hour"
Cursor: *Searches only allowed log directories*
```

---

## 📦 What Can You Save?

cursor-extend automatically chooses the right approach based on what you describe:

### 💨 Simple Commands → `.cursor/commands.json` (Recommended!)

**Use for:** Any shell command (90% of cases)

**Just say:**
- "Remember: npm run build"
- "Remember: docker-compose up -d"
- "Remember: ./deploy.sh staging"

**Why this is best:**
- ✅ Zero code - just JSON
- ✅ Instant to save
- ✅ Easy to edit
- ✅ Git-committable
- ✅ Team shares automatically

---

### 🎯 Controlled Tools → Python MCP (When you need safety/validation)

**Use for:** Any operation that needs control, validation, or restrictions

**Just say:**
- "Create a tool for api.company.com/debug/customer" (API with validation)
- "Create a tool to search logs in /var/log/myapp" (file ops with restrictions)
- "Create a tool to deploy to staging" (commands with guardrails)

**What you get (beyond memory):**
- 🎯 **Control:** Only expose what's safe
- ✅ **Validation:** Prevent invalid inputs, SQL injection, path traversal
- 🔒 **Restrictions:** Read-only access, specific directories, staging-only deploys
- 📊 **Audit:** Log who did what, when
- 🎨 **Customization:** Transform data, combine operations, add business logic
- 🤝 **Team safety:** Junior devs can't accidentally break prod

**Common patterns:**
- `http_api` - APIs with endpoint/auth/validation
- `file_operations` - Safe file search (only specific folders), log parsing
- `basic_function` - Deploy commands (with env restrictions), DB queries (read-only)

**cursor-extend generates the code, you add your safety rules!**

---

## 🔧 How It Works

### Behind the Scenes:

1. **You describe** what you need in natural language
2. **Cursor asks cursor-extend** for guidance (patterns, examples, best practices)
3. **cursor-extend provides** comprehensive guide with reference code
4. **Cursor writes** the exact custom implementation
5. **You review** (optional), test, and deploy

### Core Tools:

**"cursor extend"** (`discover_project_commands()`) - 🔍 AI-Powered Command Discovery
- Guides Cursor to intelligently analyze your project
- Discovers commands from package.json, Makefile, README, etc.
- Categorizes by complexity (simple commands vs. MCP tools)
- Offers to save everything at once

**`remember_command()`** - 💨 Zero-Code Command Storage
- Saves commands to `.cursor/commands.json`
- Updates `.cursorrules` for automatic discovery
- No Python or MCP knowledge needed

**`get_mcp_tool_guide()`** - 🧠 MCP Tool Generation
- Returns patterns, reference implementations, best practices
- Cursor uses this to write custom MCP tools with logic

**`add_tool_to_cursor_config()`** - ⚙️ Auto-Configuration
- Automatically updates `~/.cursor/mcp.json`
- No manual config editing

**`validate_mcp_tool()`** - ✅ Validation
- Checks generated tool is properly structured
- Validates Python syntax and dependencies

---

## 💡 Example: iOS Build Tool

**Before (Every Day):**

> **You:** "Build my iOS app"  
> **Cursor:** *tries wrong commands*  
> **You:** *explains the exact xcodebuild command again*  
> **Cursor:** *finally works*

**With cursor-extend (Once):**

> **You:** "Create a tool called 'build-ios' that runs: xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 15 Pro' clean build"
>
> **Cursor:** Uses `get_mcp_tool_guide()` → Gets patterns → Writes:

```python
from fastmcp import FastMCP
import subprocess

mcp = FastMCP("iOS Build")

@mcp.tool()
def build_ios_app() -> str:
    """Build iOS app for simulator"""
    cmd = [
        "xcodebuild",
        "-workspace", "MyApp.xcworkspace",
        "-scheme", "MyApp",
        "-configuration", "Debug",
        "-destination", "platform=iOS Simulator,name=iPhone 15 Pro",
        "clean", "build"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return "✅ Build successful!"
    else:
        return f"❌ Build failed:\n{result.stderr}"

if __name__ == "__main__":
    mcp.run()
```

> **Cursor:** "✅ Created! Would you like me to add it to Cursor?"

**After (Forever):**

> **You:** "Build my iOS app"  
> **Cursor:** *Uses build-ios tool, works perfectly every time*  
> **You:** 🎉

**No more daily explanations. Your project remembers.**

---

## 🎓 For Everyone

You don't need to know MCP or how to code!

**Describe what you need:**

**For any developer:**
- "Create a tool that runs: \<your complex command>"
- "Build a deployment tool with our company's scripts"
- "Make a test runner that sets up the database first"

**For non-engineers (via Claude Desktop):**
- "Build me a tool to check customer status"
- "Create a tool to query order information"
- "Make a tool to search our logs for errors"

**Cursor writes the code. You just describe it.**

---

## 🛠️ Development

```bash
# Clone
git clone https://github.com/mazzucci/cursor-extend
cd cursor-extend

# Install
uv sync

# Test
uv run pytest -v
```

---

## 🤝 Share Tools with Your Team

Once you create a tool, share it via Git:

```bash
# Push to company GitHub
git init
git add .
git commit -m "Add iOS build MCP tool"
git push origin main

# Team installs with one command
uvx --from git+ssh://git@github.company.com/eng/ios-build-tool ios-build
```

**Now your whole team benefits from the same tool.**

---

## 📚 Learn More

- [FastMCP Documentation](https://gofastmcp.com) - The framework powering cursor-extend
- [Model Context Protocol](https://modelcontextprotocol.io/) - The protocol specification
- [Cursor IDE](https://cursor.sh/) - AI-first code editor with MCP support

---

## 🤝 Contributing

Contributions welcome! Ideas for new tool types, better patterns, improved guidance.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

Built on [FastMCP](https://gofastmcp.com) by the FastMCP team.

---

**Stop re-teaching Cursor every day. Create tools that remember.**

*The best MCP tool is the one you build through conversation.*
