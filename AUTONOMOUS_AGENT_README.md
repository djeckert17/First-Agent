# Autonomous Trip Planning Agent

## Overview

The **Autonomous Trip Planning Agent** is a goal-oriented AI agent that plans complete trips independently with minimal user intervention. Unlike traditional chatbots that require constant back-and-forth, this agent analyzes your goal, gathers any missing information upfront, then works autonomously through multiple tools to create a comprehensive travel plan.

## Key Features

### 🤖 Autonomous Operation
- **One-shot planning**: Give the agent a goal, get a complete plan
- **Minimal intervention**: Agent only asks clarifying questions if critical info is missing
- **Multi-tool orchestration**: Automatically uses weather, web search, and task management
- **Decision making**: Makes intelligent choices based on best practices and your preferences

### 🔧 Powered by Multiple Tools
- **Weather Forecasting**: Checks conditions to inform activity planning
- **Web Search**: Researches hotels, restaurants, activities, and current information
- **Task Management**: Creates organized checklists with priorities and due dates
- **Database Persistence**: Saves your trip for reference and tracking

### 🎯 Goal-Oriented Intelligence
- Extracts key parameters from natural language goals
- Identifies information gaps and asks targeted questions
- Plans comprehensively across accommodation, dining, activities, and logistics
- Considers weather, budget, travel style, and traveler demographics

---

## Quick Start

### Installation

Ensure you have the dependencies:
```bash
pip install -r requirements.txt
```

### Run Quick Test

```bash
python autonomous_agent.py quick
```

This demonstrates autonomous planning with a luxury anniversary trip example.

### View All Demos

```bash
python autonomous_agent.py autonomous  # Full demo with 2 examples
python autonomous_agent.py interactive # Comparison with interactive mode
```

---

## How to Use

### Basic Usage Pattern

```python
from autonomous_agent import AutonomousTravelAgent
import asyncio

async def plan_trip():
    # Create autonomous agent
    agent = AutonomousTravelAgent(autonomous_mode=True)

    # Define your goal
    goal = "Plan a 5-day family trip to Marbella in July with 2 kids ages 6 and 9"

    # Agent works autonomously
    result = await agent.plan_autonomously(goal)

    print(result)

asyncio.run(plan_trip())
```

### Example Goals

**Well-Specified (Agent proceeds directly):**
```
"Plan a 3-day luxury anniversary trip to Marbella in June for 2 adults.
We want spa treatments and fine dining."
```

**Vague (Agent asks 1-3 questions):**
```
"I want to visit Marbella for a week"
```

The agent will ask about:
- Budget level (budget/mid-range/luxury)
- Number of travelers and demographics
- Travel style/interests

**After Questions:**
```python
# Agent asked questions
response = await agent.plan_autonomously(goal)

# Provide answers
answers = "Mid-range budget, family with 2 kids (7 and 10), love beach activities"
final_plan = await agent.answer_questions(answers)
```

---

## What the Agent Does Autonomously

### Phase 1: Information Analysis
The agent extracts parameters from your goal:
- ✓ Destination (defaults to Marbella if not specified)
- ✓ Travel dates or season
- ✓ Trip duration
- ✓ Number of travelers (adults/children with ages)
- ✓ Budget level
- ✓ Travel style/interests

**Decision Point:**
- **Sufficient info** → Proceed to autonomous planning
- **Critical gaps** → Ask 1-3 focused questions only

### Phase 2: Autonomous Execution

The agent works through multiple tools **without asking for approval**:

1. **Weather Check**
   ```
   → get_weather_forecast(Marbella, June)
   → get_weather_forecast(Granada) [for day trips]
   ```

2. **Web Research**
   ```
   → WebSearch("luxury hotels Marbella June 2026")
   → WebSearch("best seafood restaurants Marbella")
   → WebSearch("kid-friendly activities Costa del Sol")
   → WebSearch("Marbella to Granada day trip guide")
   ```

3. **Trip Creation**
   ```
   → create_trip("Family_Marbella_July_2026")
   ```

4. **Task Building**
   ```
   → add_task(accommodation, high priority, due: May 1)
   → add_task(restaurant reservations, medium priority)
   → add_task(activity bookings, priorities based on weather)
   → add_task(day trip to Granada, high priority)
   → add_task(transportation, low priority)
   ```

5. **Organization**
   - Categories: accommodation, activities, dining, transport
   - Priorities: high/medium/low based on importance
   - Due dates: Strategic timeline before trip

### Phase 3: Comprehensive Results

The agent presents:
- 🌤️ **Weather outlook** and how it influenced planning
- 🏨 **Key recommendations** from web research
- ✅ **Complete task list** organized by priority
- 💡 **Insider tips** and practical considerations
- 📊 **Statistics**: Number of tasks created, trip details

---

## Example Output

### Input Goal
```
"Plan a 3-day luxury anniversary trip to Marbella in June for 2 adults.
We want spa treatments and fine dining."
```

### Agent's Autonomous Work

```
✓ Analyzed goal (sufficient information)
✓ Checked June weather in Marbella (75-82°F, sunny)
✓ Researched luxury hotels → Found Puente Romano Beach Resort
✓ Searched Michelin restaurants → Skina (2⭐), Leña, Lobito de Mar
✓ Found spa options → Six Senses Spa at Puente Romano
✓ Researched romantic activities → Private yacht cruise, Old Town tour
✓ Created trip: Luxury_Anniversary_Marbella_June_2026
✓ Added 12 tasks with strategic priorities:
   - HIGH: Accommodation, spa, restaurants, yacht cruise (due: April-May)
   - MEDIUM: Additional dining, tours (due: May)
   - LOW: Flexible activities (due: May)
```

### Delivered Plan

- **Weather Analysis**: Perfect June conditions for outdoor activities
- **Accommodation**: Puente Romano Beach Resort (why it's ideal)
- **Dining**: 3 Michelin-starred restaurants with descriptions
- **Spa**: Six Senses Spa couples treatments
- **Activities**: Yacht cruise, Old Town tour, beach club, Puerto Banús
- **Task Checklist**: 12 organized tasks ready to execute
- **Insider Tips**: Booking advice, timing, dress codes

---

## Agent Behavior Principles

### What Makes It Autonomous

✅ **Proactive Decision Making**
- Doesn't ask "Should I search for hotels?" - just does it
- Doesn't ask "Would you like me to add this task?" - just adds it
- Makes informed choices based on travel best practices

✅ **Comprehensive Planning**
- Creates 8-15 tasks for typical trips
- Covers all aspects: accommodation, dining, activities, transport
- Balances must-do with flexible options

✅ **Weather-Informed Recommendations**
- Checks forecasts before suggesting activities
- Recommends indoor/outdoor mix based on conditions
- Considers seasonal highlights

✅ **Intelligent Prioritization**
- High priority: Time-sensitive bookings (hotels, popular restaurants)
- Medium priority: Important but flexible (tours, additional dining)
- Low priority: Walk-up activities, general exploration

✅ **Realistic Timelines**
- Sets due dates 6-8 weeks before trip for major bookings
- Earlier deadlines for high-demand venues (3+ months)
- Buffer time for planning and preparation

### What Makes It Smart

🧠 **Context Understanding**
- Interprets "family" → searches kid-friendly options
- Interprets "luxury" → focuses on premium experiences
- Interprets "romantic" → emphasizes intimate settings

🧠 **Gap Identification**
- Knows when budget info is critical vs. nice-to-have
- Asks about traveler demographics only if it affects planning
- Makes reasonable assumptions when details are minor

🧠 **Tool Orchestration**
- Uses weather to inform activity selection
- Uses web search to get current, real-world information
- Uses task manager to organize findings into actionable plan
- Connects dots across multiple sources

---

## Advanced Usage

### Custom System Prompts

You can customize the agent's behavior:

```python
agent = AutonomousTravelAgent(autonomous_mode=True)

# Agent already has comprehensive system prompt
# Modify agent.options.system_prompt if needed
```

### Interactive Mode

Use the agent interactively for more back-and-forth:

```python
agent = AutonomousTravelAgent(autonomous_mode=False)

# Works like conversational agent
response = await agent.interactive_chat("What's the weather in Marbella?")
```

### Batch Planning

Plan multiple trips in sequence:

```python
agent = AutonomousTravelAgent(autonomous_mode=True)

goals = [
    "Plan weekend trip to Málaga",
    "Plan 5-day Granada cultural tour",
    "Plan week in Sevilla"
]

for goal in goals:
    result = await agent.plan_autonomously(goal)
    print(result)
    await agent.reset_conversation()  # Fresh start for next trip
```

---

## Comparison: Autonomous vs Interactive

### Autonomous Agent
```
User: "Plan a 5-day family trip to Marbella in July"

Agent: [Works independently]
✓ Checks weather
✓ Searches hotels
✓ Searches activities
✓ Creates trip
✓ Adds 10 tasks
✓ Presents complete plan

Output: Ready-to-execute travel plan with task checklist
Time: Single response cycle
```

### Interactive Agent
```
User: "I want to plan a trip to Marbella"
Agent: "Great! What dates are you thinking?"
User: "Maybe July"
Agent: "How many days? Who's traveling?"
User: "5 days, family with kids"
Agent: "What are their ages?"
User: "6 and 9"
Agent: "What's your budget?"
User: "Mid-range"
Agent: "Let me check weather... What activities interest you?"
[Multiple exchanges required]
```

**Use Autonomous When:**
- You want a complete plan quickly
- You can provide key details upfront
- You trust the agent to make good decisions
- You want comprehensive research done automatically

**Use Interactive When:**
- You want to explore options together
- You're unsure about preferences
- You want step-by-step collaboration
- You prefer approving each decision

---

## Technical Details

### Tools Used

**Weather Forecasting:**
- Provider: yr.no / Norwegian Meteorological Institute
- Returns: Current conditions + 3-day forecast
- Format: Fahrenheit (default) with Celsius

**Web Search:**
- Provider: Built-in Claude Code WebSearch
- Searches: Hotels, restaurants, activities, current events
- Returns: Real-time web results with links

**Task Management:**
- Storage: SQLite database (`trips_database.db`)
- Features: CRUD operations, categories, priorities, dates
- Persistence: Local file, survives restarts

### Permission Mode

Autonomous mode uses `permission_mode='acceptEdits'`:
- Agent doesn't need approval for tool use
- Speeds up execution significantly
- Safe because tools only create user data or fetch info
- No destructive operations

### Performance

**Typical Autonomous Planning Session:**
- Duration: 30-90 seconds
- Tool calls: 8-15 (weather checks, web searches, task creation)
- Tasks created: 8-15 for complete trip
- API calls: Depends on complexity and search needs

---

## Tips for Best Results

### Writing Effective Goals

✅ **Good Examples:**
```
"Plan a 7-day luxury anniversary trip to Marbella in September.
We love fine dining and want a spa day. Interested in Granada day trip."

"Plan 5-day beach vacation for family with kids ages 5 and 8.
Mid-range budget, July, want water sports and kid-friendly restaurants."

"Plan weekend getaway to Costa del Sol, relaxation focused,
boutique hotel, good seafood."
```

❌ **Vague Examples (will prompt questions):**
```
"Plan a trip to Spain"
"I want to go to Marbella"
"Help me plan travel"
```

### Information to Include

**Essential:**
- Destination (or defaults to Marbella)
- Duration (number of days)
- Travel dates or season
- Budget level (budget/mid-range/luxury)
- Basic interests or trip style

**Helpful:**
- Number of travelers (adults/children with ages)
- Specific must-haves (spa, golf, water sports, culture)
- Special occasions (anniversary, birthday, family reunion)
- Dietary needs or accessibility requirements

**Optional (agent will make reasonable assumptions):**
- Exact accommodation preferences
- Specific restaurant types
- Transportation preferences
- Day trip destinations

---

## Troubleshooting

### Agent Asks Too Many Questions

**Problem:** You provided sufficient info but agent still asks questions

**Solution:** Be more specific in your initial goal. Include:
- Budget level explicitly
- Number of travelers
- Key interests or trip style

### Agent Doesn't Search for Information

**Problem:** Plan lacks web research insights

**Solution:** Ensure WebSearch is in allowed_tools (it should be by default)

### Tasks Not Created

**Problem:** Agent describes plan but doesn't create tasks

**Solution:**
- Check database permissions
- Ensure `trips_database.db` can be created
- Verify task management tools are loaded

### Plan Too Generic

**Problem:** Recommendations lack specificity

**Solution:** Provide more context in your goal:
- Instead of "family trip" → "family with toddler and teenager"
- Instead of "luxury" → "luxury with private villa and Michelin dining"
- Instead of "activities" → "water sports and cultural experiences"

---

## Examples by Travel Style

### Budget Travelers
```
"Plan 4-day budget trip to Marbella in October for 2 adults.
Interested in free beaches, local tapas, and hiking."

Agent focuses on:
- Budget accommodations (hostels, budget hotels)
- Free/low-cost activities
- Local eateries vs fine dining
- Public transportation
```

### Luxury Travelers
```
"Plan week-long luxury escape to Costa del Sol in May.
Want 5-star resort, private yacht, Michelin dining, golf."

Agent focuses on:
- Top-tier hotels (Puente Romano, Marbella Club)
- Exclusive experiences
- Premium services
- Private transportation
```

### Family Travelers
```
"Plan 6-day family trip to Marbella in August for 2 adults and 3 kids (4, 7, 11).
Mid-range budget, kids love beach and animals."

Agent focuses on:
- Family-friendly accommodations
- Kid-appropriate activities
- Restaurants with kids' menus
- Beach safety and facilities
- Zoo, aquarium, water parks
```

### Adventure Seekers
```
"Plan 5-day adventure trip to Costa del Sol in June.
Want water sports, mountain biking, rock climbing, active experiences."

Agent focuses on:
- Activity-focused accommodation
- Sports equipment rentals
- Guided adventure tours
- High-energy itinerary
- Recovery time and nutrition
```

### Culture Enthusiasts
```
"Plan 7-day cultural immersion in Andalusia from Marbella base in April.
Interested in art, history, architecture, flamenco, traditional cuisine."

Agent focuses on:
- Museums and galleries
- Historic sites and tours
- Flamenco shows
- Cooking classes
- Day trips to cultural destinations
```

---

## Future Enhancements

**Planned Features:**
- Multi-destination trip planning (Málaga → Marbella → Ronda circuit)
- Budget tracking and optimization
- Calendar integration for automatic scheduling
- Collaborative planning for groups
- Real-time price monitoring
- Booking API integration for one-click reservations

---

## Support

**Documentation:**
- This file: Autonomous agent guide
- `TOOLS_README.md`: Individual tool documentation
- `README.md`: Project overview
- `CLAUDE.md`: Technical implementation details

**Running Examples:**
```bash
python autonomous_agent.py autonomous  # Full demo
python autonomous_agent.py quick      # Quick test
python autonomous_agent.py interactive # Interactive comparison
```

**Interactive Use:**
```python
from autonomous_agent import AutonomousTravelAgent
import asyncio

async def main():
    agent = AutonomousTravelAgent(autonomous_mode=True)
    result = await agent.plan_autonomously("Your goal here")
    print(result)

asyncio.run(main())
```

---

**Version:** 1.0.0
**Last Updated:** January 12, 2026
**Powered by:** Claude Agent SDK + yr.no Weather API + Web Search
