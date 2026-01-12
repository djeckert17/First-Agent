"""
Autonomous Trip Planning Agent
A goal-oriented agent that plans trips independently using weather, tasks, and web search.

The agent works autonomously toward completing travel planning goals without
constant user intervention. It gathers info upfront, then executes a complete plan.
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


class AutonomousTravelAgent:
    """
    An autonomous trip planning agent that works toward goals independently.

    Features:
    - Analyzes goals and asks clarifying questions only if needed
    - Works autonomously through multiple tools
    - Creates complete trip plans without constant approval
    - Uses web search for real-time information
    - Maintains conversation context across planning session
    """

    def __init__(self, autonomous_mode=True):
        """
        Initialize the autonomous agent.

        Args:
            autonomous_mode: If True, agent works autonomously without seeking approval.
                           If False, operates more interactively.
        """
        self.autonomous_mode = autonomous_mode
        self._connected = False

        # Build system prompt based on mode
        system_prompt = self._build_system_prompt()

        # Configure agent options
        self.options = ClaudeAgentOptions(
            system_prompt=system_prompt,

            # MCP server with weather and task management tools
            mcp_servers={"travel": travel_tools_server},

            # Allow all travel tools + web search
            allowed_tools=[
                # Travel tools
                "mcp__travel__get_weather_forecast",
                "mcp__travel__create_trip",
                "mcp__travel__add_task",
                "mcp__travel__list_tasks",
                "mcp__travel__complete_task",
                "mcp__travel__update_task",
                "mcp__travel__delete_task",
                "mcp__travel__list_trips",
                # Web search for real-time info
                "WebSearch"
            ],

            # In autonomous mode, accept edits without approval prompts
            permission_mode='acceptEdits' if autonomous_mode else 'default'
        )

        # Create the client
        self.client = ClaudeSDKClient(options=self.options)

    def _build_system_prompt(self) -> str:
        """Build system prompt based on agent mode."""

        base_prompt = """You are an expert autonomous trip planning agent specializing in Marbella, Spain
        and the Costa del Sol region. You excel at creating comprehensive travel plans efficiently.

        YOUR EXPERTISE:
        - Beaches and coastal areas (Marbella, Puerto Banús, Estepona, Mijas Costa)
        - Restaurants and local cuisine (chiringuitos, tapas bars, seafood, fine dining)
        - Activities and attractions (water sports, golf, old town, marina, cultural sites)
        - Day trips to nearby towns (Ronda, Granada, Málaga, Gibraltar)
        - Seasonal considerations and weather patterns
        - Budget optimization and luxury options
        - Family-friendly, romantic, and adventure travel"""

        if self.autonomous_mode:
            autonomous_instructions = """

        AUTONOMOUS OPERATION MODE:
        You work toward completing travel planning goals independently and efficiently.

        PHASE 1 - INITIAL ASSESSMENT (Information Gathering):
        When given a travel goal, first analyze what information you have:

        CRITICAL INFO NEEDED:
        - Destination (default: Marbella if not specified)
        - Travel dates OR season/month
        - Number of travelers (adults, children with ages if relevant)
        - Trip duration (number of days)
        - Budget level (budget/mid-range/luxury)
        - Travel style/interests (relaxation/adventure/culture/family/romantic)

        DECISION POINT:
        - If you have ENOUGH info to create a solid plan → Proceed directly to Phase 2
        - If CRITICAL info is missing → Ask 1-3 focused questions ONLY
        - Don't ask about nice-to-have details, make reasonable assumptions

        PHASE 2 - AUTONOMOUS PLANNING (Work Independently):
        Once you have sufficient information, work autonomously WITHOUT asking for approval:

        1. CHECK WEATHER: Use get_weather_forecast for destination and potential day trip locations
        2. RESEARCH: Use WebSearch to find:
           - Hotels/accommodations matching budget and style
           - Restaurants and dining recommendations
           - Activities and attractions
           - Day trip options and logistics
           - Current events or seasonal highlights
        3. CREATE TRIP: Use create_trip with descriptive name (e.g., "Family_Marbella_July_2026")
        4. BUILD ITINERARY: Use add_task to create comprehensive checklist:
           - Accommodation booking (high priority, early due date)
           - Activity bookings (priorities based on weather and interests)
           - Restaurant reservations (medium priority)
           - Day trips (with weather considerations)
           - Transportation arrangements
           - Any pre-trip preparations
        5. ORGANIZE: Ensure tasks have appropriate:
           - Categories (accommodation/activities/dining/transport)
           - Priorities (high/medium/low)
           - Due dates (realistic timeline before trip)

        PHASE 3 - COMPLETION:
        Present comprehensive summary showing:
        - Weather outlook and how it influenced planning
        - Key recommendations from web research
        - Complete task list organized by priority
        - Any important tips or considerations
        - Total number of tasks created

        IMPORTANT PRINCIPLES:
        ✓ Work proactively - don't wait for permission to use tools
        ✓ Use web search extensively for current, real-world information
        ✓ Make decisions based on best practices and user preferences
        ✓ Create a COMPLETE plan, not a partial one
        ✓ Be thorough but efficient - aim for 8-15 tasks for a typical trip
        ✓ Consider weather when recommending activities
        ✓ Balance must-do tasks with flexible options
        ✓ Don't ask "Should I...?" or "Would you like me to...?" - just do it

        YOUR TOOLS:
        - get_weather_forecast: Check weather (Marbella: 36.51, -4.88; Granada: 37.18, -3.60)
        - WebSearch: Find hotels, restaurants, activities, current info
        - create_trip: Initialize trip in database
        - add_task: Create planning tasks with categories, priorities, dates
        - list_tasks: Review what you've created

        WORK AUTONOMOUSLY until the goal is achieved. The user trusts you to plan efficiently."""

        else:
            autonomous_instructions = """

        INTERACTIVE MODE:
        Maintain conversation context and work collaboratively with the user.
        Ask for preferences and approval when making significant decisions.
        Use tools as requested and provide explanations for recommendations."""

        tools_info = """

        AVAILABLE TOOLS:

        WEATHER TOOL:
        - get_weather_forecast: Real-time forecasts from yr.no
        - Temperatures in Fahrenheit by default (Celsius available)
        - Coordinates: Marbella (36.51, -4.88), Granada (37.18, -3.60), Málaga (36.72, -4.42)

        TASK MANAGEMENT:
        - create_trip: Organize tasks by trip
        - add_task: Add tasks with categories (accommodation/activities/dining/transport)
        - Priorities: high/medium/low
        - Due dates for timeline planning
        - Persistent database storage

        WEB SEARCH:
        - Search for hotels, restaurants, activities
        - Get current prices, reviews, availability info
        - Find local events and seasonal highlights
        - Research day trip logistics and recommendations"""

        return base_prompt + autonomous_instructions + tools_info

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
            Agent's response as a string
        """
        await self._ensure_connected()

        response_text = ""

        # Send message using the stateful client
        await self.client.query(user_message)

        # Receive the response
        async for message in self.client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text

        return response_text

    async def plan_autonomously(self, goal: str, show_progress=True) -> str:
        """
        Execute autonomous trip planning for a given goal.

        This is the main entry point for one-shot autonomous planning.
        The agent will analyze the goal, ask minimal clarifying questions if needed,
        then work independently to create a complete trip plan.

        Args:
            goal: Travel planning goal (e.g., "Plan a 5-day family trip to Marbella in July")
            show_progress: If True, print progress indicators

        Returns:
            Complete planning result as string
        """
        if show_progress:
            print("=" * 80)
            print("🤖 AUTONOMOUS TRIP PLANNING AGENT")
            print("=" * 80)
            print(f"\n📋 Goal: {goal}\n")
            print("🔄 Analyzing request and gathering information...\n")
            print("-" * 80)

        # Craft the autonomous planning prompt
        planning_prompt = f"""I need you to plan a trip autonomously. Here's my goal:

"{goal}"

Analyze this goal. If you have enough information to create a comprehensive trip plan,
proceed directly to autonomous planning. If critical information is missing (like budget,
number of travelers, or key preferences), ask me 1-3 focused questions to gather essentials.

Once you have sufficient information, work autonomously through all planning phases:
1. Check weather forecasts
2. Research accommodations and activities via web search
3. Create the trip in the database
4. Build a complete task list with priorities and due dates
5. Present the final plan

Remember: Work independently without asking for approval at each step. Create a complete,
actionable trip plan."""

        # Send the planning request
        response = await self.send_message(planning_prompt)

        if show_progress:
            print(response)
            print("\n" + "=" * 80)

        return response

    async def answer_questions(self, answers: str) -> str:
        """
        Provide answers to agent's clarifying questions.

        After calling plan_autonomously(), if the agent asks questions,
        use this method to answer them. The agent will then proceed autonomously.

        Args:
            answers: Answers to the agent's questions

        Returns:
            Agent's response (should be the complete plan)
        """
        response = await self.send_message(answers)
        return response

    async def interactive_chat(self, message: str) -> str:
        """
        Have an interactive conversation (alternative to autonomous mode).

        Args:
            message: User's message

        Returns:
            Agent's response
        """
        return await self.send_message(message)

    async def reset_conversation(self):
        """Reset the conversation by disconnecting and creating a new client."""
        if self._connected:
            await self.client.disconnect()
        self.client = ClaudeSDKClient(options=self.options)
        self._connected = False


async def autonomous_demo():
    """Demonstrate autonomous trip planning."""
    print("\n" + "=" * 80)
    print("DEMONSTRATION: Autonomous Trip Planning")
    print("=" * 80)
    print("\nThis demo shows the agent planning trips autonomously with minimal input.\n")

    # Create autonomous agent
    agent = AutonomousTravelAgent(autonomous_mode=True)

    # Example 1: Well-specified goal (agent should proceed directly)
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Detailed Goal (Agent proceeds autonomously)")
    print("=" * 80)

    goal1 = """Plan a 5-day romantic getaway to Marbella for 2 adults in September.
    Mid-range budget, we love fine dining and want one spa day. Interested in visiting Granada for a day."""

    result1 = await agent.plan_autonomously(goal1, show_progress=True)

    # Wait before next example
    await asyncio.sleep(2)

    # Reset for new example
    await agent.reset_conversation()
    agent = AutonomousTravelAgent(autonomous_mode=True)

    # Example 2: Vague goal (agent should ask questions)
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Vague Goal (Agent asks clarifying questions)")
    print("=" * 80)

    goal2 = "I want to visit Marbella for a week"

    print(f"\n📋 Goal: {goal2}\n")
    print("🔄 The agent should ask clarifying questions...\n")
    print("-" * 80)

    response2 = await agent.plan_autonomously(goal2, show_progress=False)
    print(response2)

    # Simulate answering questions
    if "?" in response2:
        print("\n" + "-" * 80)
        print("User answers: Mid-range budget, family with 2 kids (ages 7 and 10), love beach and activities")
        print("-" * 80 + "\n")

        answers = "Mid-range budget, family with 2 kids (ages 7 and 10), we love beach activities and exploring"
        final_plan = await agent.answer_questions(answers)
        print(final_plan)

    print("\n" + "=" * 80)
    print("✅ Autonomous Planning Demo Complete!")
    print("=" * 80)


async def interactive_demo():
    """Demonstrate interactive mode for comparison."""
    print("\n" + "=" * 80)
    print("DEMONSTRATION: Interactive Mode (Non-Autonomous)")
    print("=" * 80)
    print("\nFor comparison, here's the agent in interactive mode.\n")

    agent = AutonomousTravelAgent(autonomous_mode=False)

    queries = [
        "What's the weather in Marbella?",
        "Create a trip called Test_Interactive",
        "Add a task to book a hotel"
    ]

    for query in queries:
        print(f"\nUser: {query}")
        print("-" * 80)
        response = await agent.interactive_chat(query)
        print(f"Agent: {response[:200]}...")
        print()
        await asyncio.sleep(1)

    print("=" * 80)


async def quick_test():
    """Quick test of autonomous planning."""
    print("\n" + "=" * 80)
    print("QUICK TEST: Autonomous Planning")
    print("=" * 80)

    agent = AutonomousTravelAgent(autonomous_mode=True)

    goal = "Plan a 3-day luxury anniversary trip to Marbella in June for 2 adults. We want spa treatments and fine dining."

    result = await agent.plan_autonomously(goal, show_progress=True)

    print("\n✅ Quick test complete!")


async def main():
    """Main entry point with demo selection."""
    import sys

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = "menu"

    if mode == "menu":
        print("\n" + "=" * 80)
        print("AUTONOMOUS TRIP PLANNING AGENT")
        print("=" * 80)
        print("\nAvailable demos:")
        print("\n1. autonomous  - Full autonomous planning demo (2 examples)")
        print("2. interactive - Interactive mode for comparison")
        print("3. quick       - Quick autonomous planning test")
        print("\nUsage: python autonomous_agent.py [demo_name]")
        print("Example: python autonomous_agent.py autonomous")
        print("=" * 80 + "\n")
        return

    if mode == "autonomous":
        await autonomous_demo()
    elif mode == "interactive":
        await interactive_demo()
    elif mode == "quick":
        await quick_test()
    else:
        print(f"Unknown mode: {mode}")
        print("Valid options: autonomous, interactive, quick")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError running demo: {e}")
        import traceback
        traceback.print_exc()
