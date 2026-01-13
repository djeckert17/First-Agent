"""
Marbella Travel Planning Agent
A travel agent using Claude Agent SDK's ClaudeSDKClient for custom MCP tools support.
"""

import asyncio
import os
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
from tools import travel_tools_server

# Load environment variables
load_dotenv()

# Verify API key is configured
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY not found in environment. Please configure your .env file.")


async def plan_trip(prompt: str) -> str:
    """
    Send a travel planning query to Claude.

    This uses ClaudeSDKClient which supports custom MCP tools.

    Args:
        prompt: The travel planning question or request

    Returns:
        Claude's response as a string
    """
    # Configure the agent with a specialized system prompt for Marbella travel
    options = ClaudeAgentOptions(
        system_prompt="""You are an expert travel advisor specializing in Marbella, Spain
        and the Costa del Sol region. You provide detailed, practical advice about:

        - Beaches and coastal areas (Marbella, Puerto Banús, Estepona, Mijas Costa)
        - Restaurants and local cuisine (chiringuitos, tapas bars, seafood)
        - Activities and attractions (water sports, golf, old town, marina)
        - Day trips to nearby towns (Ronda, Granada, Málaga, Gibraltar)
        - Best times to visit and seasonal considerations
        - Practical tips (transportation, accommodations, local customs)

        Provide specific, actionable recommendations with practical details like
        approximate costs, locations, and booking considerations when relevant.

        You now have access to tools for enhanced trip planning:

        WEATHER TOOL:
        - get_weather_forecast: Get weather forecasts for any location
        - Defaults to Fahrenheit (can specify Celsius if user prefers)
        - Marbella coordinates: lat=36.51, lon=-4.88
        - Use for day trips: Granada (37.18, -3.60), Málaga (36.72, -4.42), Ronda (36.74, -5.17)

        TASK MANAGEMENT:
        - Create trips to organize planning tasks
        - Add tasks with categories: accommodation, activities, dining, transport
        - Set priorities: low, medium, high
        - Track completion and due dates
        - Help users build comprehensive travel checklists""",

        # MCP server with weather and task management tools
        mcp_servers={"travel": travel_tools_server},

        # Allow all travel planning tools
        allowed_tools=[
            "mcp__travel__get_weather_forecast",
            "mcp__travel__create_trip",
            "mcp__travel__add_task",
            "mcp__travel__list_tasks",
            "mcp__travel__complete_task",
            "mcp__travel__update_task",
            "mcp__travel__delete_task",
            "mcp__travel__list_trips"
        ],

        # Use default permission mode
        permission_mode='default'
    )

    # Use ClaudeSDKClient which supports custom MCP tools
    response_text = ""

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        async for message in client.receive_response():
            # Extract text from assistant messages
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text

    return response_text


async def main():
    """
    Main function demonstrating the Marbella travel agent.
    """
    print("=" * 70)
    print("🏖️  Marbella Travel Planning Agent")
    print("=" * 70)
    print("This is a stateless agent - each query is independent.\n")

    # Example query
    example_prompt = """I'm planning a 5-day trip to Marbella in June.
    Can you suggest the best beaches to visit and a few good seafood restaurants?"""

    print("Query:")
    print(f"  {example_prompt}\n")
    print("-" * 70)
    print("Response:\n")

    try:
        response = await plan_trip(example_prompt)
        print(response)
        print("\n" + "=" * 70)

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Configured ANTHROPIC_API_KEY in your .env file")
        print("3. Installed Claude CLI: npm install -g @anthropic-ai/claude-code")


if __name__ == "__main__":
    asyncio.run(main())
