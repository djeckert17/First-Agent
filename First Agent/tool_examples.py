"""
Tool Examples - Demonstration of Weather and Task Management Tools
Shows various usage patterns for the Marbella travel planning tools.
"""

import asyncio
import sys
from conversational_agent import MarbellaConversationalAgent


async def weather_demo():
    """Demonstrate weather tool with multiple locations."""
    print("=" * 80)
    print("WEATHER TOOL DEMONSTRATION")
    print("=" * 80)
    print()

    agent = MarbellaConversationalAgent()

    queries = [
        {
            "query": "What's the weather forecast in Marbella?",
            "description": "Get Marbella weather in Fahrenheit (default)"
        },
        {
            "query": "Can you check the weather in Granada for me? I'm thinking of a day trip.",
            "description": "Compare weather for day trip destination"
        },
        {
            "query": "What about Málaga weather?",
            "description": "Another day trip destination"
        }
    ]

    for i, item in enumerate(queries, 1):
        print(f"\n{'=' * 80}")
        print(f"Query {i}: {item['description']}")
        print("=" * 80)
        print(f"\nUser: {item['query']}\n")
        print("-" * 80)
        print("Assistant:\n")

        try:
            response = await agent.send_message(item['query'])
            print(response)
        except Exception as e:
            print(f"Error: {e}")

        print()
        await asyncio.sleep(1)  # Rate limiting

    print("\n" + "=" * 80)
    print("Weather demo complete!")
    print("=" * 80)


async def task_management_demo():
    """Demonstrate task management workflow."""
    print("=" * 80)
    print("TASK MANAGEMENT DEMONSTRATION")
    print("=" * 80)
    print()

    agent = MarbellaConversationalAgent()

    workflow = [
        {
            "query": "Create a new trip called 'Summer 2026 Marbella'",
            "description": "Step 1: Create a trip"
        },
        {
            "query": "Add a task to book accommodation at a beachfront hotel, high priority, due June 1st",
            "description": "Step 2: Add high-priority accommodation task"
        },
        {
            "query": "Add another task: Reserve table at seafood restaurant, category dining, medium priority",
            "description": "Step 3: Add dining task"
        },
        {
            "query": "Add task: Book water sports lesson, category activities, priority high, due June 15",
            "description": "Step 4: Add activity task"
        },
        {
            "query": "Add task: Rent a car for day trips, category transport, low priority",
            "description": "Step 5: Add transport task"
        },
        {
            "query": "Show me all my tasks for this trip",
            "description": "Step 6: List all tasks"
        },
        {
            "query": "Complete the accommodation booking task (task #1)",
            "description": "Step 7: Mark task as completed"
        },
        {
            "query": "Update task #2 to include the restaurant name: El Oceano Beach",
            "description": "Step 8: Update task details"
        },
        {
            "query": "Show my pending tasks only",
            "description": "Step 9: Filter by pending status"
        },
        {
            "query": "List all my trips",
            "description": "Step 10: View all trips with statistics"
        }
    ]

    for i, item in enumerate(workflow, 1):
        print(f"\n{'=' * 80}")
        print(f"{item['description']}")
        print("=" * 80)
        print(f"\nUser: {item['query']}\n")
        print("-" * 80)
        print("Assistant:\n")

        try:
            response = await agent.send_message(item['query'])
            print(response)
        except Exception as e:
            print(f"Error: {e}")

        print()
        await asyncio.sleep(0.5)

    print("\n" + "=" * 80)
    print("Task management demo complete!")
    print("=" * 80)


async def combined_demo():
    """Demonstrate weather + task management integration."""
    print("=" * 80)
    print("COMBINED SCENARIO: Weather-Based Planning")
    print("=" * 80)
    print()

    agent = MarbellaConversationalAgent()

    scenario = [
        {
            "query": "I'm planning a trip to Marbella. Can you check the weather there?",
            "description": "Check weather"
        },
        {
            "query": "Based on that weather, create a trip called 'Marbella_Adventure_2026' and suggest some activities I should plan for",
            "description": "Create trip and get activity suggestions"
        },
        {
            "query": "Add tasks for each of those suggested activities with appropriate priorities",
            "description": "Convert suggestions to tasks"
        },
        {
            "query": "I'm also thinking of visiting Granada. What's the weather like there?",
            "description": "Check day trip weather"
        },
        {
            "query": "Add a task for the Granada day trip with high priority",
            "description": "Add day trip task"
        },
        {
            "query": "Show me my complete task list",
            "description": "Review full plan"
        }
    ]

    for i, item in enumerate(scenario, 1):
        print(f"\n{'=' * 80}")
        print(f"Turn {i}: {item['description']}")
        print("=" * 80)
        print(f"\nUser: {item['query']}\n")
        print("-" * 80)
        print("Assistant:\n")

        try:
            response = await agent.send_message(item['query'])
            print(response)
        except Exception as e:
            print(f"Error: {e}")

        print()
        await asyncio.sleep(1)

    print("\n" + "=" * 80)
    print("Combined demo complete!")
    print("=" * 80)
    print("\nThis scenario demonstrated:")
    print("✓ Context-aware weather queries")
    print("✓ Weather-informed trip planning")
    print("✓ Dynamic task creation based on conditions")
    print("✓ Multi-location planning (Marbella + day trips)")
    print("✓ Conversation memory across tools")


async def quick_test():
    """Quick test to verify tools are working."""
    print("=" * 80)
    print("QUICK TOOL TEST")
    print("=" * 80)
    print()

    agent = MarbellaConversationalAgent()

    tests = [
        "What's the weather in Marbella?",
        "Create a trip called 'Test_Trip'",
        "List all my trips"
    ]

    for i, query in enumerate(tests, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 80)

        try:
            response = await agent.send_message(query)
            print(response[:200] + "..." if len(response) > 200 else response)
            print("✓ Success\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")

        await asyncio.sleep(0.5)

    print("=" * 80)
    print("Quick test complete!")
    print("=" * 80)


async def main():
    """Main entry point with command-line demo selection."""
    if len(sys.argv) > 1:
        demo = sys.argv[1].lower()
    else:
        demo = "menu"

    if demo == "menu":
        print("\n" + "=" * 80)
        print("TOOL EXAMPLES - Choose a demonstration:")
        print("=" * 80)
        print("\n1. weather    - Weather tool demo (Marbella, Granada, Málaga)")
        print("2. tasks      - Task management workflow (create, add, list, complete, update)")
        print("3. combined   - Weather + tasks integration scenario")
        print("4. quick      - Quick test to verify tools work")
        print("5. all        - Run all demos sequentially")
        print("\nUsage: python tool_examples.py [demo_name]")
        print("Example: python tool_examples.py weather")
        print("=" * 80 + "\n")
        return

    demos = {
        "weather": ("Weather Tool Demo", weather_demo),
        "tasks": ("Task Management Demo", task_management_demo),
        "combined": ("Combined Integration Demo", combined_demo),
        "quick": ("Quick Test", quick_test)
    }

    if demo == "all":
        print("\n" + "=" * 80)
        print("RUNNING ALL DEMOS")
        print("=" * 80)

        for name, (title, func) in demos.items():
            print(f"\n\nStarting: {title}")
            await func()
            await asyncio.sleep(2)

        print("\n\n" + "=" * 80)
        print("ALL DEMOS COMPLETE!")
        print("=" * 80)

    elif demo in demos:
        title, func = demos[demo]
        print(f"\nRunning: {title}\n")
        await func()

    else:
        print(f"\nUnknown demo: {demo}")
        print("Valid options: weather, tasks, combined, quick, all")
        print("Or run without arguments to see the menu.\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError running demo: {e}")
        print("\nMake sure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Configured ANTHROPIC_API_KEY in your .env file")
