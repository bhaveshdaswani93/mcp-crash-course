import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

llm = ChatOpenAI()
print(f"Model being used: {llm.model_name}")


async def main():
    print("Starting Multi-Server MCP Client...")
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [Path("servers/math_server.py").absolute().as_posix()],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
            "playwright": {
                "command": "npx",
                "args": ["@playwright/mcp@latest"],
                "transport": "stdio",
            }
        }
    )
    
    print("Getting tools from all servers...")
    tools = await client.get_tools()
    print(f"Loaded tools: {tools}")

    agent = create_react_agent(llm, tools)
    
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Navigate to https://en.wikipedia.org/wiki/Albert_Einstein, read the page content, and provide a brief summary about Albert Einstein"}]}
    )
    print(f"Agent result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
