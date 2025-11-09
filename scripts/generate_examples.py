"""Generate example MCP tools for demonstration"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_extend.generator import ToolGenerator


def main():
    generator = ToolGenerator()
    output_dir = Path(__file__).parent.parent / "examples"
    
    examples = [
        ("Calculator", "Basic math operations", "basic_function"),
        ("Weather API", "Fetch weather from wttr.in", "http_api"),
        ("File Search", "Search and read local files", "file_operations"),
    ]
    
    print("Generating example MCP tools...\n")
    
    for name, desc, template in examples:
        print(f"Creating: {name}")
        result = generator.generate_tool(
            tool_name=name,
            description=desc,
            template_type=template,
            output_dir=str(output_dir)
        )
        print(f"  ✓ {result['path']}")
        print(f"  Install: {result['install_command']}\n")
    
    print(f"Done! Examples created in: {output_dir}")
    print("\nTo test an example:")
    print(f"  cd {output_dir}/internal-debug-api")
    print("  uv sync")
    print("  uv run python server.py")


if __name__ == "__main__":
    main()

