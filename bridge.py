import asyncio
import os

import httpx
from ollama_mcp_bridge.mcp_manager import MCPManager

MODEL = os.environ.get("OLLAMA_MODEL", "gpt-oss:120b-cloud")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "mcp.config.json")
SYSTEM_PROMPT = (
    "You are FinInsights, an AI assistant for POS order analysis. "
    "Use the available tools to look up and reconcile orders."
)


async def chat_loop(manager: MCPManager):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print(f"FinInsights ready (model={MODEL}). Type 'quit' to exit.\n")
    async with httpx.AsyncClient(timeout=None) as http:
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                break
            if user_input.lower() in ("quit", "exit", "q"):
                print("Goodbye.")
                break
            if not user_input:
                continue

            messages.append({"role": "user", "content": user_input})

            # First call — inject MCP tools
            resp = await http.post(
                f"{OLLAMA_URL}/api/chat",
                json={"model": MODEL, "messages": messages, "tools": manager.all_tools, "stream": False},
            )
            resp.raise_for_status()
            result = resp.json()

            # Execute any tool calls
            for tc in result.get("message", {}).get("tool_calls", []):
                name = tc["function"]["name"]
                args = tc["function"]["arguments"]
                print(f"  [tool: {name}({args})]")
                try:
                    tool_result = await manager.call_tool(name, args)
                except (IndexError, AttributeError):
                    tool_result = "Tool returned no content."
                messages.append({"role": "tool", "name": name, "content": str(tool_result)})

            # Follow-up call to get final answer after tool results
            if result.get("message", {}).get("tool_calls"):
                resp = await http.post(
                    f"{OLLAMA_URL}/api/chat",
                    json={"model": MODEL, "messages": messages, "stream": False},
                )
                resp.raise_for_status()
                result = resp.json()

            reply = result["message"]["content"]
            messages.append({"role": "assistant", "content": reply})
            print(f"\nAssistant: {reply}\n")


async def main():
    manager = MCPManager(ollama_url=OLLAMA_URL)
    await manager.load_servers(CONFIG_FILE)
    tools = [t["function"]["name"] for t in manager.all_tools]
    print(f"Connected. Tools: {tools}")
    try:
        await chat_loop(manager)
    finally:
        await manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
