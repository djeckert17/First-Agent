"""
Multi-Turn Conversation Examples for Marbella Travel Planning Agent

Demonstrates various scenarios where conversational memory and context
building are essential for effective trip planning.
"""

import asyncio
from conversational_agent import MarbellaConversationalAgent


async def scenario_budget_conscious_couple():
    """
    Scenario: Budget-conscious couple refining plans based on costs.
    Demonstrates: Memory of budget constraints, progressive refinement
    """
    print("\n" + "=" * 80)
    print("SCENARIO 1: Budget-Conscious Couple")
    print("=" * 80)
    print("Context: Couple wants to visit Marbella but needs to stay within budget.\n")

    agent = MarbellaConversationalAgent()

    turns = [
        "My partner and I want to visit Marbella for a long weekend. We're on a budget of about €500 for activities and meals (not including hotel). Is this realistic?",
        "That's reassuring! What are some budget-friendly restaurants where we can try local cuisine?",
        "We'd like to visit one nice beach club as a splurge. Which one gives the best experience for the price?",
        "Based on everything we've discussed, can you create a 3-day itinerary that stays within our €500 budget?",
    ]

    await run_conversation_scenario(agent, turns)


async def scenario_luxury_anniversary():
    """
    Scenario: Couple celebrating anniversary, building luxury itinerary.
    Demonstrates: Memory of special occasion, progressive addition of experiences
    """
    print("\n" + "=" * 80)
    print("SCENARIO 2: Luxury Anniversary Celebration")
    print("=" * 80)
    print("Context: Celebrating 10th anniversary, wants premium experiences.\n")

    agent = MarbellaConversationalAgent()

    turns = [
        "My wife and I are celebrating our 10th anniversary in Marbella next month. We want to make it really special - money is not a concern.",
        "Fantastic suggestions! She loves Mediterranean cuisine. What's the best Michelin-starred restaurant in the area?",
        "Perfect! I also want to surprise her with a private yacht experience. What options are available?",
        "This is shaping up wonderfully! Can you also recommend a luxury spa for a couples treatment?",
        "Can you put together a romantic 4-day anniversary itinerary incorporating all these elements?",
    ]

    await run_conversation_scenario(agent, turns)


async def scenario_adventure_seeker():
    """
    Scenario: Solo traveler interested in activities, asking follow-ups.
    Demonstrates: Building activity list, remembering preferences and skill levels
    """
    print("\n" + "=" * 80)
    print("SCENARIO 3: Adventure-Seeking Solo Traveler")
    print("=" * 80)
    print("Context: Active solo traveler wants to pack trip with activities.\n")

    agent = MarbellaConversationalAgent()

    turns = [
        "I'm traveling solo to Marbella for a week and I love adventure sports and outdoor activities. What can I do there?",
        "Those sound amazing! I'm an intermediate scuba diver - are there good dive sites nearby?",
        "I also enjoy hiking. Are there any good hiking trails in the area?",
        "This is perfect! But I also need to eat. Where do solo travelers typically dine in Marbella?",
        "One last thing - can you suggest which days I should do which activities to create a good flow for my week?",
    ]

    await run_conversation_scenario(agent, turns)


async def scenario_culture_enthusiast():
    """
    Scenario: Traveler interested in culture, history, and local experiences.
    Demonstrates: Building cultural itinerary, remembering interests
    """
    print("\n" + "=" * 80)
    print("SCENARIO 4: Culture and History Enthusiast")
    print("=" * 80)
    print("Context: Interested in authentic cultural experiences over tourist attractions.\n")

    agent = MarbellaConversationalAgent()

    turns = [
        "I'm visiting Marbella but I'm not really a beach person. I'm more interested in culture, history, and authentic local experiences. What should I do?",
        "The old town sounds perfect for me! What are the best local markets where I can experience daily life?",
        "I'd love to take a day trip to see some historical sites. Where would you recommend?",
        "Granada sounds incredible! Are there any local festivals or events happening in August?",
        "Can you create a 6-day cultural immersion itinerary based on everything we've discussed?",
    ]

    await run_conversation_scenario(agent, turns)


async def scenario_multigenerational_trip():
    """
    Scenario: Complex multi-generational family trip planning.
    Demonstrates: Tracking multiple family members, different needs, compromises
    """
    print("\n" + "=" * 80)
    print("SCENARIO 5: Multi-Generational Family Trip")
    print("=" * 80)
    print("Context: Planning for grandparents, parents, teenagers, and young kids.\n")

    agent = MarbellaConversationalAgent()

    turns = [
        "I'm organizing a family reunion in Marbella. We have 4 generations: my parents (70s), my wife and I (40s), our teenagers (15 and 17), and my sister's kids (4 and 7). How do we keep everyone happy?",
        "Great suggestions! My parents have limited mobility - which beaches have the best accessibility?",
        "The teenagers want some independence. Are there safe activities they can do on their own?",
        "What about restaurants that can accommodate our large group and have options for picky young kids?",
        "This is very helpful! Can you draft a flexible 5-day plan that includes activities everyone can do together, plus some age-appropriate separate activities?",
    ]

    await run_conversation_scenario(agent, turns)


async def scenario_changing_preferences():
    """
    Scenario: Traveler changes mind based on new information.
    Demonstrates: Adapting to changing requirements, remembering constraints
    """
    print("\n" + "=" * 80)
    print("SCENARIO 6: Evolving Preferences")
    print("=" * 80)
    print("Context: Plans evolve as traveler learns more about destination.\n")

    agent = MarbellaConversationalAgent()

    turns = [
        "I'm planning 4 days in Marbella. I want to stay in Puerto Banús and spend most of my time there. What should I do?",
        "Hmm, Puerto Banús sounds like it might be too touristy for me. What's the old town like in comparison?",
        "Actually, that sounds more my style. Should I stay in the old town instead of Puerto Banús?",
        "Perfect! Now with staying in the old town, what would be a good mix of relaxing beach time and exploring the area?",
        "Can you revise the original plan now that I'm staying in the old town instead of Puerto Banús?",
    ]

    await run_conversation_scenario(agent, turns)


async def run_conversation_scenario(agent: MarbellaConversationalAgent, turns: list):
    """
    Helper function to run through a conversation scenario.

    Args:
        agent: The conversational agent instance
        turns: List of user messages to send
    """
    for i, message in enumerate(turns, 1):
        print(f"\n{'─' * 80}")
        print(f"Turn {i}/{len(turns)}")
        print("─" * 80)
        print(f"\n👤 User:\n{message}\n")
        print("🤖 Assistant:")

        try:
            response = await agent.send_message(message)
            print(response)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            break

        # Small delay between turns
        await asyncio.sleep(1)

    print("\n" + "=" * 80)
    print("✅ Scenario completed!")
    print("=" * 80)


async def run_all_scenarios():
    """Run all conversation scenarios sequentially."""
    print("\n" + "═" * 80)
    print("🏖️  MARBELLA CONVERSATIONAL AGENT - SCENARIO DEMONSTRATIONS")
    print("═" * 80)
    print("\nThese scenarios demonstrate how conversation memory enables:")
    print("  • Context building across multiple turns")
    print("  • Remembering user preferences and constraints")
    print("  • Progressive refinement of travel plans")
    print("  • Adapting to changing requirements")
    print("  • Synthesizing information into coherent itineraries")
    print("\n" + "═" * 80)

    scenarios = [
        ("Budget-Conscious Couple", scenario_budget_conscious_couple),
        ("Luxury Anniversary", scenario_luxury_anniversary),
        ("Adventure Seeker", scenario_adventure_seeker),
        ("Culture Enthusiast", scenario_culture_enthusiast),
        ("Multi-Generational Trip", scenario_multigenerational_trip),
        ("Evolving Preferences", scenario_changing_preferences),
    ]

    for i, (name, scenario_func) in enumerate(scenarios, 1):
        print(f"\n\n{'═' * 80}")
        print(f"Running Scenario {i}/{len(scenarios)}: {name}")
        print("═" * 80)
        await scenario_func()

        # Pause between scenarios
        if i < len(scenarios):
            print("\n⏸️  Pausing 2 seconds before next scenario...")
            await asyncio.sleep(2)

    print("\n\n" + "═" * 80)
    print("🎉 ALL SCENARIOS COMPLETED!")
    print("═" * 80)
    print("\nComparison with Stateless Approach:")
    print("  ✗ Stateless (query): Each message is independent, no context")
    print("  ✓ Stateful (ClaudeSDKClient): Full conversation memory")
    print("\nThese examples show why conversation memory is essential for")
    print("complex trip planning that evolves over multiple interactions!")


async def run_single_scenario(scenario_number: int):
    """
    Run a single scenario by number (1-6).

    Args:
        scenario_number: Which scenario to run (1-6)
    """
    scenarios = [
        scenario_budget_conscious_couple,
        scenario_luxury_anniversary,
        scenario_adventure_seeker,
        scenario_culture_enthusiast,
        scenario_multigenerational_trip,
        scenario_changing_preferences,
    ]

    if 1 <= scenario_number <= len(scenarios):
        await scenarios[scenario_number - 1]()
    else:
        print(f"Please choose a scenario number between 1 and {len(scenarios)}")


if __name__ == "__main__":
    # Run all scenarios
    asyncio.run(run_all_scenarios())

    # Or run a single scenario:
    # asyncio.run(run_single_scenario(1))
