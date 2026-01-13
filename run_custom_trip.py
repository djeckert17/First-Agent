"""
Custom Trip Planning Script
Runs the autonomous agent with a specific user-provided prompt.
"""

import asyncio
from autonomous_agent import AutonomousTravelAgent


async def run_custom_trip():
    """Execute autonomous planning with custom user prompt."""

    # Your custom travel planning prompt
    custom_prompt = """My wife and 19-year-old son would like to plan a quiet, relaxing and sun-filled
luxury vacation to the South of Spain. Our home base will be Marbella, where I have business to tend to,
and will be staying at a friend's home. While making our home base Marbella, we'd also like to plan small,
driveable excursions to surrounding towns that have both historical, architectural and culinary interest to us.
We would likely want to keep the travel boundaries fairly constrained to the surrounding areas that are between
Málaga to the northeast, El Zabal to the southwest, and Ronda to the North northwest.

We arrive in Marbella on March 7, 2026 around 1pm, and the general idea of a trip would be as follows:

- March 7: Stay in Marbella
- March 8: Explore Marbella and beach
- March 9: Surrounding area excursion
- March 10: Surrounding day excursion
- March 11: Morning trip to Granada, with overnight stay
- March 12: Return to Marbella in the mid-morning, and chill out with friends
- March 13: Return to the U.S. from Marbella

For the overnight to Granada, would want top-of-the-line hotel accommodations – preferably with a private
terrace – that will accommodate all three of us in one room/suite.

For each suggested surrounding area excursion, I'd also like a walking tour that doesn't last more than
2 hours of walking for the town in a way that allows us to see the sites, experience the vibe/culture of
the town, and sample its cuisine while there. The walking tour should be efficiently planned so that one
destination moves seamlessly (and efficiently) into the next.

Since we will be driving to each surrounding locale, identify parking areas that are conveniently located
to the rest of the things you're planning for us.

For the hotel in Granada we're not opposed to spending ~$1,200 USD for the night at the hotel. For culinary
recommendations, we're not people that need haute cuisine, but rather love restaurants that would be showcased
on a show like "Somebody Feed Phil"."""

    print("\n" + "=" * 80)
    print("🌴 CUSTOM TRIP PLANNING: Marbella & Costa del Sol")
    print("=" * 80)
    print("\n📅 Dates: March 7-13, 2026")
    print("👥 Travelers: 3 adults (you, wife, 19-year-old son)")
    print("🏠 Home Base: Marbella")
    print("💎 Style: Luxury, relaxing, cultural")
    print("\n" + "=" * 80)

    # Create autonomous agent
    agent = AutonomousTravelAgent(autonomous_mode=True)

    # Execute autonomous planning
    result = await agent.plan_autonomously(custom_prompt, show_progress=True)

    print("\n" + "=" * 80)
    print("✅ CUSTOM TRIP PLANNING COMPLETE!")
    print("=" * 80)
    print("\nThe agent has created a comprehensive trip plan with:")
    print("  • Weather forecasts for all destinations")
    print("  • Granada luxury hotel recommendations with private terraces")
    print("  • 2-hour walking tours for day excursions")
    print("  • Parking recommendations for each location")
    print("  • 'Somebody Feed Phil' style restaurant suggestions")
    print("  • Complete task list with priorities and due dates")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        asyncio.run(run_custom_trip())
    except KeyboardInterrupt:
        print("\n\n⚠️  Planning interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error during planning: {e}")
        import traceback
        traceback.print_exc()
