"""
Example queries for the Marbella Travel Planning Agent.
Demonstrates various types of travel planning queries.
"""

import asyncio
from marbella_agent import plan_trip


async def run_examples():
    """
    Run several example travel planning queries.
    Each query is stateless and independent.
    """

    examples = [
        {
            "title": "Beach Recommendations",
            "query": "What are the top 3 beaches in Marbella for families with young children? I need calm waters and good facilities."
        },
        {
            "title": "Day Trip Planning",
            "query": "I want to take a day trip from Marbella to a nearby coastal town. What do you recommend and how do I get there?"
        },
        {
            "title": "Restaurant Suggestions",
            "query": "Can you recommend 3 authentic chiringuitos (beach restaurants) in the Marbella area for fresh seafood? Include price ranges."
        },
        {
            "title": "Activity Planning",
            "query": "What are the best water sports activities available in Puerto Banús? I'm interested in jet skiing and parasailing."
        },
        {
            "title": "Old Town Exploration",
            "query": "I want to explore Marbella's old town (Casco Antiguo). What are the must-see spots and best tapas bars there?"
        },
        {
            "title": "Coastal Towns Route",
            "query": "Plan a scenic coastal drive from Marbella covering the best towns along Costa del Sol. Which towns should I stop at?"
        },
        {
            "title": "Seasonal Travel Advice",
            "query": "What's the best month to visit Marbella for good weather but fewer crowds? What should I expect in terms of prices?"
        },
        {
            "title": "Luxury Experience",
            "query": "I'm looking for a luxury experience in Marbella - high-end beach clubs, Michelin-star restaurants, and yacht activities. What do you suggest?"
        }
    ]

    print("=" * 80)
    print("🏖️  MARBELLA TRAVEL PLANNING - EXAMPLE QUERIES")
    print("=" * 80)
    print(f"\nRunning {len(examples)} example queries...\n")
    print("Note: Each query is STATELESS - Claude has no memory of previous queries.")
    print("=" * 80)

    for i, example in enumerate(examples, 1):
        print(f"\n\n{'=' * 80}")
        print(f"Example {i}/{len(examples)}: {example['title']}")
        print("=" * 80)
        print(f"\nQuery:\n  {example['query']}\n")
        print("-" * 80)
        print("Response:\n")

        try:
            response = await plan_trip(example['query'])
            print(response)

        except Exception as e:
            print(f"❌ Error: {e}")
            break

        # Small delay between queries to avoid rate limiting
        if i < len(examples):
            await asyncio.sleep(1)

    print("\n\n" + "=" * 80)
    print("✅ All examples completed!")
    print("=" * 80)
    print("\nKey observations:")
    print("- Each query was independent (stateless)")
    print("- Claude had no memory between queries")
    print("- This is ideal for simple Q&A without conversation history")
    print("\nNext steps: Add memory and tools in future iterations!")


async def run_single_example(example_number: int = 1):
    """
    Run a single example by number (1-8).
    Useful for testing individual queries.
    """
    examples = [
        "What are the top 3 beaches in Marbella for families with young children?",
        "I want to take a day trip from Marbella to a nearby coastal town. What do you recommend?",
        "Can you recommend 3 authentic chiringuitos for fresh seafood?",
        "What are the best water sports activities available in Puerto Banús?",
        "I want to explore Marbella's old town. What are the must-see spots?",
        "Plan a scenic coastal drive from Marbella covering the best towns along Costa del Sol.",
        "What's the best month to visit Marbella for good weather but fewer crowds?",
        "I'm looking for a luxury experience in Marbella - high-end beach clubs and restaurants."
    ]

    if 1 <= example_number <= len(examples):
        query_text = examples[example_number - 1]
        print(f"Running example {example_number}:\n{query_text}\n")
        print("-" * 80)
        response = await plan_trip(query_text)
        print(response)
    else:
        print(f"Please choose an example number between 1 and {len(examples)}")


if __name__ == "__main__":
    # Run all examples
    asyncio.run(run_examples())

    # Or run a single example:
    # asyncio.run(run_single_example(1))
