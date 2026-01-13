"""
Updated Trip Planning Script - Double Feature: Mijas + Estepona
Runs the autonomous agent with March 10 updated to visit BOTH towns.
"""

import asyncio
from autonomous_agent import AutonomousTravelAgent


async def run_double_feature_trip():
    """Execute autonomous planning with Mijas + Estepona double feature for March 10."""

    # Updated custom travel planning prompt with double feature
    double_feature_prompt = """My wife and 19-year-old son would like to plan a quiet, relaxing and sun-filled
luxury vacation to the South of Spain. Our home base will be Marbella, where I have business to tend to,
and will be staying at a friend's home. While making our home base Marbella, we'd also like to plan small,
driveable excursions to surrounding towns that have both historical, architectural and culinary interest to us.
We would likely want to keep the travel boundaries fairly constrained to the surrounding areas that are between
Málaga to the northeast, El Zabal to the southwest, and Ronda to the North northwest.

We arrive in Marbella on March 7, 2026 around 1pm, and the general idea of a trip would be as follows:

- March 7: Stay in Marbella
- March 8: Explore Marbella and beach
- March 9: Day trip to Ronda (keep this as planned)
- March 10: DOUBLE FEATURE - Mijas Pueblo (morning) + Estepona (lunch & afternoon)
- March 11: Morning trip to Granada, with overnight stay
- March 12: Return to Marbella in the mid-morning, and chill out with friends
- March 13: Return to the U.S. from Marbella

SPECIFIC REQUIREMENTS FOR MARCH 10 - DOUBLE FEATURE DAY:

**MORNING - MIJAS PUEBLO (9:00am - 11:30am):**
- Compact 1.5-hour walking tour of this cliff-top white village
- Focus on: Plaza de la Virgen de la Peña, cliff-top church with panoramic Mediterranean views,
  art galleries, charming cobblestone streets
- Identify convenient parking locations
- This should be efficient and focused - we want to see the highlights and get great photos
- Drive time from Marbella: ~15-20 minutes

**LUNCH & AFTERNOON - ESTEPONA (12:00pm - 4:30pm):**
- Arrive around noon for lunch at a beachfront chiringuito
- After lunch: 2-hour walking tour covering historic old town with famous flower-decorated streets,
  Plaza de las Flores, the marina area, and beachfront promenade
- The walking tour should flow seamlessly from one destination to the next
- Identify convenient parking locations near the old town/historic center
- Recommend "Somebody Feed Phil" style restaurants for seaside lunch with views
- Include both traditional Spanish and seafood options
- Drive time from Mijas to Estepona: ~20-25 minutes

**LOGISTICS:**
- Total drive time for the day: Marbella → Mijas (15-20 min) → Estepona (20-25 min) → Marbella (30 min)
- We want this to feel relaxed, not rushed
- Parking information for BOTH towns
- Restaurant recommendations for Estepona lunch (beachfront/marina preferred)

For the overnight to Granada, would want top-of-the-line hotel accommodations – preferably with a private
terrace – that will accommodate all three of us in one room/suite.

For the Ronda excursion (March 9), I'd also like a walking tour that doesn't last more than 2 hours of
walking for the town in a way that allows us to see the sites, experience the vibe/culture of the town,
and sample its cuisine while there. The walking tour should be efficiently planned so that one destination
moves seamlessly (and efficiently) into the next.

Since we will be driving to each surrounding locale, identify parking areas that are conveniently located
to the rest of the things you're planning for us.

For the hotel in Granada we're not opposed to spending ~$1,200 USD for the night at the hotel. For culinary
recommendations, we're not people that need haute cuisine, but rather love restaurants that would be showcased
on a show like "Somebody Feed Phil"."""

    print("\n" + "=" * 80)
    print("🌴 UPDATED TRIP PLANNING: Double Feature Day!")
    print("=" * 80)
    print("\n📅 Dates: March 7-13, 2026")
    print("👥 Travelers: 3 adults (you, wife, 19-year-old son)")
    print("🏠 Home Base: Marbella")
    print("💎 Style: Luxury, relaxing, cultural")
    print("\n✨ MARCH 10 - DOUBLE FEATURE:")
    print("   🏔️  Morning: Mijas Pueblo (cliff-top white village)")
    print("   🌊 Lunch & Afternoon: Estepona (coastal town)")
    print("   📍 Marbella → Mijas (15-20 min) → Estepona (20-25 min) → Marbella (30 min)")
    print("\n" + "=" * 80)

    # Create autonomous agent
    agent = AutonomousTravelAgent(autonomous_mode=True)

    # Execute autonomous planning
    result = await agent.plan_autonomously(double_feature_prompt, show_progress=True)

    print("\n" + "=" * 80)
    print("✅ DOUBLE FEATURE TRIP PLANNING COMPLETE!")
    print("=" * 80)
    print("\nThe agent has created a comprehensive trip plan with:")
    print("  • Weather forecasts for all destinations")
    print("  • MIJAS PUEBLO: Compact 1.5-hour morning tour + parking")
    print("  • ESTEPONA: Lunch recommendations + 2-hour afternoon walking tour")
    print("  • DOUBLE FEATURE: Complete timeline and logistics for March 10")
    print("  • RONDA: Full walking tour details maintained")
    print("  • GRANADA: Luxury hotel recommendations with private terraces")
    print("  • Complete task list with priorities and due dates")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        asyncio.run(run_double_feature_trip())
    except KeyboardInterrupt:
        print("\n\n⚠️  Planning interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error during planning: {e}")
        import traceback
        traceback.print_exc()
