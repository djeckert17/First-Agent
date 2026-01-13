"""
Marbella Conversational Travel Planning Agent
Uses ClaudeSDKClient for stateful conversations with memory.
Each session maintains conversation history across multiple turns.
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


class MarbellaConversationalAgent:
    """
    A conversational travel agent that maintains conversation history.

    Unlike the stateless query() approach, this agent remembers previous
    interactions and can build on context from earlier in the conversation.
    """

    def __init__(self):
        """Initialize the conversational agent with Claude SDK client."""
        # Configure the agent options
        self.options = ClaudeAgentOptions(
            system_prompt="""You are an expert travel advisor specializing in Marbella, Spain
            and the Costa del Sol region. You provide detailed, practical advice about:

            - Beaches and coastal areas (Marbella, Puerto Banús, Estepona, Mijas Costa)
            - Restaurants and local cuisine (chiringuitos, tapas bars, seafood)
            - Activities and attractions (water sports, golf, old town, marina)
            - Day trips to nearby towns (Ronda, Granada, Málaga, Gibraltar)
            - Best times to visit and seasonal considerations
            - Practical tips (transportation, accommodations, local customs)

            You maintain conversation context and remember previous questions and preferences.
            Build on earlier discussions to provide personalized, coherent travel planning.
            If the user mentions previous preferences or constraints, acknowledge and incorporate them.

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
            - Help users build comprehensive travel checklists
            - Remember tasks across conversation turns to build comprehensive plans""",

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

        # Create the client - this maintains the conversation state
        self.client = ClaudeSDKClient(options=self.options)
        self._connected = False

    async def _ensure_connected(self):
        """Ensure the client is connected before sending messages."""
        if not self._connected:
            await self.client.connect()
            self._connected = True

    async def send_message(self, user_message: str) -> str:
        """
        Send a message and get a response while maintaining conversation history.

        Args:
            user_message: The user's message or question

        Returns:
            Claude's response as a string
        """
        # Ensure we're connected before sending
        await self._ensure_connected()

        response_text = ""

        # Send message using the stateful client
        await self.client.query(user_message)

        # Receive the response
        async for message in self.client.receive_response():
            # Extract text from assistant messages
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text

        return response_text

    async def reset_conversation(self):
        """Reset the conversation by disconnecting and creating a new client."""
        if self._connected:
            await self.client.disconnect()
        self.client = ClaudeSDKClient(options=self.options)
        self._connected = False


async def demo_conversation():
    """
    Demonstrate a multi-turn conversation with memory.
    Shows how the agent builds on previous context.
    """
    print("=" * 80)
    print("🏖️  Marbella Conversational Travel Planning Agent")
    print("=" * 80)
    print("This agent maintains conversation history across multiple turns.\n")

    # Create the conversational agent
    agent = MarbellaConversationalAgent()

    # Multi-turn conversation demonstrating memory and context building
    conversation_turns = [
        {
            "turn": 1,
            "message": "Hi! I'm planning a trip to Marbella in July. I have a family with two kids aged 6 and 9.",
            "note": "Initial context - establishes family travel with kids"
        },
        {
            "turn": 2,
            "message": "That sounds great! What beaches would you recommend for us?",
            "note": "Agent should remember the family context from turn 1"
        },
        {
            "turn": 3,
            "message": "We love seafood. Can you recommend some restaurants near those beaches?",
            "note": "Agent should connect to previously mentioned beaches"
        },
        {
            "turn": 4,
            "message": "My 9-year-old really wants to try water sports. What's appropriate for that age?",
            "note": "Agent remembers the kids' ages and can make age-appropriate suggestions"
        },
        {
            "turn": 5,
            "message": "Perfect! Can you help me plan out a rough itinerary for a 5-day trip incorporating all these activities?",
            "note": "Agent should synthesize all previous context into a coherent plan"
        }
    ]

    print("Starting multi-turn conversation...\n")
    print("=" * 80)

    for turn_data in conversation_turns:
        print(f"\n{'=' * 80}")
        print(f"TURN {turn_data['turn']}")
        print(f"Context Note: {turn_data['note']}")
        print("=" * 80)
        print(f"\n👤 User: {turn_data['message']}\n")
        print("-" * 80)
        print("🤖 Assistant:\n")

        try:
            response = await agent.send_message(turn_data['message'])
            print(response)

        except Exception as e:
            print(f"❌ Error: {e}")
            print("\nMake sure you have:")
            print("1. Installed dependencies: pip install -r requirements.txt")
            print("2. Configured ANTHROPIC_API_KEY in your .env file")
            print("3. Installed Claude CLI: npm install -g @anthropic-ai/claude-code")
            break

        # Small delay between turns
        await asyncio.sleep(1)

    print("\n\n" + "=" * 80)
    print("✅ Conversation completed!")
    print("=" * 80)
    print("\nKey observations:")
    print("✓ Agent maintained context across all 5 turns")
    print("✓ Remembered family composition (kids aged 6 and 9)")
    print("✓ Connected beaches, restaurants, and activities coherently")
    print("✓ Built a comprehensive plan based on accumulated preferences")
    print("\nThis demonstrates the power of stateful conversations with memory!")


async def interactive_mode():
    """
    Interactive mode for having a real conversation with the agent.
    Type 'quit' or 'exit' to end the conversation.
    """
    print("=" * 80)
    print("🏖️  Marbella Travel Planning - Interactive Mode")
    print("=" * 80)
    print("Have a conversation with your travel planning agent!")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("Type 'reset' to start a new conversation.\n")
    print("=" * 80)

    agent = MarbellaConversationalAgent()
    turn = 0

    while True:
        turn += 1
        print(f"\n[Turn {turn}]")
        user_input = input("👤 You: ").strip()

        if user_input.lower() in ['quit', 'exit']:
            print("\n👋 Thanks for using the Marbella Travel Planning Agent!")
            break

        if user_input.lower() == 'reset':
            await agent.reset_conversation()
            turn = 0
            print("🔄 Conversation reset. Starting fresh!\n")
            continue

        if not user_input:
            continue

        print("\n🤖 Assistant:")
        try:
            response = await agent.send_message(user_input)
            print(response)
        except Exception as e:
            print(f"❌ Error: {e}")
            break


if __name__ == "__main__":
    # Run the demo conversation by default
    asyncio.run(demo_conversation())

    # Or run interactive mode:
    # asyncio.run(interactive_mode())
