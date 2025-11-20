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
            }
        }
    )
    
    print("Getting tools from all servers...")
    tools = await client.get_tools()
    print(f"Loaded tools: {tools}")

    agent = create_react_agent(llm, tools)
    # result = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "What is 2 + 2 + 5 + 2 +10?"}]}
    # )

    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is the weather in New York"}]}
    )
    print(f"Agent result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
