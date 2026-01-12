# Agent Comparison Guide

## Three Approaches to Trip Planning

This project demonstrates three different agent patterns, each with distinct strengths and use cases.

---

## 1. Stateless Agent (`marbella_agent.py`)

### Pattern: `query()` - Single Request/Response

**How it works:**
```python
from claude_agent_sdk import query

response = await query(prompt="What are the best beaches in Marbella?", options=options)
```

### Characteristics
- ⚡ **No memory**: Each request is independent
- 🎯 **Single-shot**: One question → one answer
- 🔄 **Fresh start**: No conversation history
- ⚙️ **Simple**: Minimal state management

### Best For
- API endpoints
- Simple Q&A
- Independent queries
- Microservices
- Stateless architectures

### Example Use
```
Query: "What are the best seafood restaurants in Marbella?"
Response: [List of restaurants]

Query: "What beaches are family-friendly?"
Response: [Beach recommendations]
# ⚠️ Agent doesn't remember previous restaurant question
```

### When to Use
✅ Building API endpoints
✅ One-off questions
✅ No need for context
✅ Want simplicity
✅ Stateless services

---

## 2. Conversational Agent (`conversational_agent.py`)

### Pattern: `ClaudeSDKClient` - Multi-Turn Conversation

**How it works:**
```python
from claude_agent_sdk import ClaudeSDKClient

client = ClaudeSDKClient(options=options)
await client.connect()

await client.query("What beaches are good for families?")
response1 = await client.receive_response()

await client.query("What restaurants are near those beaches?")
response2 = await client.receive_response()  # Remembers context!
```

### Characteristics
- 🧠 **Memory**: Maintains conversation history
- 💬 **Interactive**: Back-and-forth dialogue
- 🔗 **Context-aware**: References previous turns
- 👥 **Collaborative**: User guides the conversation

### Best For
- Chat interfaces
- Interactive planning
- Exploratory conversations
- Building complex plans over time
- When user preferences evolve

### Example Use
```
Turn 1: "I'm planning a family trip to Marbella"
Agent: [Provides overview, asks about family details]

Turn 2: "We have 2 kids, ages 6 and 9"
Agent: [Gives kid-friendly recommendations]

Turn 3: "What beaches would you recommend?"
Agent: [Recommends beaches suitable for ages 6 and 9] ✓ Remembers context!

Turn 4: "And restaurants near those beaches?"
Agent: [Suggests restaurants near previously mentioned beaches] ✓ Connected!
```

### When to Use
✅ Building chat applications
✅ Need conversation context
✅ Planning evolves over time
✅ User wants to explore options
✅ Collaborative decision-making

---

## 3. Autonomous Agent (`autonomous_agent.py`) ⭐ NEW

### Pattern: Goal-Oriented Autonomous Execution

**How it works:**
```python
from autonomous_agent import AutonomousTravelAgent

agent = AutonomousTravelAgent(autonomous_mode=True)

result = await agent.plan_autonomously(
    "Plan a 5-day luxury trip to Marbella in June with spa and fine dining"
)
# Agent works autonomously through multiple tools to complete the goal
```

### Characteristics
- 🤖 **Autonomous**: Works independently toward goal
- 🎯 **Goal-oriented**: Focuses on completion
- 🛠️ **Multi-tool**: Orchestrates weather + web search + tasks
- ⚡ **Efficient**: Creates complete plan in single cycle
- 🧠 **Intelligent**: Makes decisions based on best practices

### Best For
- Complete trip planning
- One-shot comprehensive plans
- When you trust agent to make decisions
- Busy users who want efficiency
- Production-ready travel plans

### Example Use
```
Input: "Plan a 3-day luxury anniversary trip to Marbella in June. We want spa and fine dining."

Agent works autonomously:
✓ Analyzes goal (sufficient info, no questions needed)
✓ Checks June weather in Marbella
✓ WebSearch: luxury hotels → Puente Romano
✓ WebSearch: Michelin restaurants → Skina, Leña, Lobito de Mar
✓ WebSearch: spa options → Six Senses Spa
✓ WebSearch: romantic activities → yacht cruise, Old Town tour
✓ create_trip("Luxury_Anniversary_June_2026")
✓ add_task: accommodation (high priority, due April)
✓ add_task: restaurant reservations (high priority, due May)
✓ add_task: spa booking (high priority, due May)
✓ add_task: yacht cruise (medium priority, due May)
✓ [... 8 more tasks ...]

Output: Complete trip plan with 12 prioritized tasks, ready to execute
Time: Single response cycle (30-90 seconds)
```

### When to Use
✅ Want complete plans quickly
✅ Can provide key details upfront
✅ Trust agent to make good decisions
✅ Need comprehensive research
✅ Production-ready travel planning
✅ Efficiency is important

---

## Side-by-Side Comparison

| Feature | Stateless | Conversational | Autonomous |
|---------|-----------|----------------|------------|
| **Memory** | ❌ No | ✅ Yes | ✅ Yes |
| **Turns** | 1 | Many | 1-3 |
| **Context** | None | Full history | Goal-oriented |
| **Tools** | ✅ Yes | ✅ Yes | ✅ Yes + Web Search |
| **Planning** | Manual | Collaborative | Autonomous |
| **Decisions** | User makes | User makes | Agent makes |
| **Speed** | Fast | Slow | Fast |
| **Completeness** | Partial | Gradual | Complete |
| **Questions** | User asks | User asks | Agent asks only if needed |
| **Output** | Answer | Discussion | Actionable plan |

---

## Detailed Scenario Comparison

### Scenario: Planning a Family Trip to Marbella

#### Stateless Agent
```
# Request 1
User: "What are family-friendly beaches in Marbella?"
Agent: "Here are 5 family-friendly beaches..."

# Request 2 (no memory of beaches)
User: "What restaurants are good for kids?"
Agent: "Here are kid-friendly restaurants in Marbella..."
# ⚠️ Not connected to previously mentioned beaches

# Request 3 (no memory of anything)
User: "What about accommodation?"
Agent: "Here are family hotels in Marbella..."

# User must manually piece together a plan
```

**Total Time:** 3 separate requests
**User Effort:** High (manual organization)
**Output:** Disconnected answers

---

#### Conversational Agent
```
Turn 1:
User: "I'm planning a family trip to Marbella with 2 kids ages 6 and 9"
Agent: "Great! How many days? When are you thinking?"

Turn 2:
User: "5 days in July, mid-range budget"
Agent: "Perfect! Let me check the weather... July is warm and sunny,
       ideal for beach activities. Would you like beach recommendations?"

Turn 3:
User: "Yes, what beaches are best for those ages?"
Agent: "Based on your kids' ages, I recommend Playa de Cabopino..."

Turn 4:
User: "And restaurants near those beaches?"
Agent: "Near Cabopino, I suggest... ✓ Connected to previous turn

Turn 5:
User: "Can you create a trip and add tasks for this?"
Agent: "I'll create 'Family_Marbella_July' and add booking tasks..."

Turn 6:
User: "What about activities for the kids?"
Agent: "Based on their ages, water sports lessons..." ✓ Remembers ages
```

**Total Time:** 6 turns, ongoing dialogue
**User Effort:** Medium (guided planning)
**Output:** Collaborative plan building

---

#### Autonomous Agent
```
Input (Turn 1):
"Plan a 5-day family trip to Marbella in July for 2 adults and 2 kids (ages 6 and 9).
Mid-range budget, kids love beach and water sports."

Agent's Autonomous Work:
✓ Analyzes goal → All info present, proceed directly
✓ get_weather_forecast(Marbella, July) → 82°F, sunny
✓ WebSearch("family hotels Marbella mid-range") → H10 Andalucia Plaza
✓ WebSearch("kid-friendly beaches Marbella") → Cabopino, Nagüeles
✓ WebSearch("water sports lessons kids Marbella") → Marbella Surf & Paddle
✓ WebSearch("family restaurants Marbella") → La Sala, Calima
✓ create_trip("Family_Marbella_July_2026")
✓ add_task: Book H10 hotel (high, due May 1)
✓ add_task: Reserve water sports lessons (high, due May 15)
✓ add_task: Book beach club day (medium, due June 1)
✓ add_task: Restaurant reservations (medium, due June 1)
✓ add_task: Rent beach equipment (low, due June 15)
✓ add_task: Buy travel insurance (high, due May 1)
✓ [... 6 more tasks ...]

Output (Turn 1 response):
"Your family trip plan is complete!
✓ Weather checked: Perfect beach weather in July
✓ Accommodation: H10 Andalucia Plaza (family suites, kids' pool)
✓ Activities: Water sports lessons, beach clubs, kid-friendly restaurants
✓ Created 12 tasks organized by priority
✓ All bookings scheduled with strategic due dates

Here's your complete itinerary..."

Optional Turn 2 (if needed):
User: "Can we add a day trip to Granada?"
Agent: ✓ Checks Granada weather
       ✓ WebSearch Granada family attractions
       ✓ Adds Granada day trip task
       "Added! Granada task created with Alhambra tickets reminder."
```

**Total Time:** 1 turn (30-90 seconds) + optional refinements
**User Effort:** Low (provide goal, receive plan)
**Output:** Complete actionable plan with task checklist

---

## Choosing the Right Agent

### Use Stateless When:
- 🔌 Building API endpoints
- ❓ Answering independent questions
- ⚡ Need quick responses
- 🎯 One question at a time
- 📦 Want simple implementation

**Example:** FAQ system, simple query API

---

### Use Conversational When:
- 💬 Building chat interface
- 🤝 Want collaborative planning
- 🔄 Preferences evolve over time
- 🧭 User wants to explore options
- 📚 Need to reference previous context

**Example:** Travel planning chatbot, advisory service

---

### Use Autonomous When:
- 🚀 Want complete plans quickly
- ⏱️ User is time-constrained
- 🤖 Trust agent to make decisions
- 🎯 Have clear goal to achieve
- 📋 Need ready-to-execute plans
- 🔧 Want multi-tool orchestration

**Example:** Production travel planning app, efficiency-focused service

---

## Real-World Application Recommendations

### Travel Agency Website
**Best:** Autonomous Agent
- Users want complete plans quickly
- Can provide goal in intake form
- Trust professional recommendations
- Need actionable output

### Travel Blog Comments
**Best:** Stateless Agent
- Users ask independent questions
- No conversation needed
- Simple Q&A format
- Fast responses

### Personal Travel Assistant App
**Best:** Conversational Agent
- Users plan over multiple sessions
- Preferences evolve
- Want to explore options
- Build relationship with assistant

### Corporate Travel Booking
**Best:** Autonomous Agent
- Efficiency is critical
- Clear business travel requirements
- Need fast, complete plans
- Standard patterns (conferences, client meetings)

### Travel Discovery Platform
**Best:** Conversational Agent
- Users exploring destinations
- Want to learn and discuss
- No immediate booking pressure
- Educational experience

---

## Migration Path

### From Stateless → Conversational
```python
# Before: Stateless
response = await query(prompt="Beach recommendations", options=options)

# After: Conversational
client = ClaudeSDKClient(options=options)
await client.connect()
await client.query("Beach recommendations")
response = await client.receive_response()
# Now can continue conversation!
```

### From Conversational → Autonomous
```python
# Before: Conversational (multiple turns)
await client.query("What beaches?")
await client.query("What hotels?")
await client.query("Create tasks")

# After: Autonomous (single goal)
agent = AutonomousTravelAgent(autonomous_mode=True)
result = await agent.plan_autonomously(
    "Plan a beach trip with hotels and tasks"
)
# Agent does it all autonomously!
```

---

## Performance Comparison

### Latency
- **Stateless:** ~2-5 seconds per query
- **Conversational:** ~2-5 seconds per turn × number of turns
- **Autonomous:** ~30-90 seconds for complete plan

### Total Time to Complete Plan
- **Stateless:** 5-10 separate queries = 25-50 seconds + user time
- **Conversational:** 5-10 turns = 25-50 seconds + user time
- **Autonomous:** 1 request = 30-90 seconds (no user time needed!)

### User Cognitive Load
- **Stateless:** High (must organize info manually)
- **Conversational:** Medium (guided but requires decisions)
- **Autonomous:** Low (provide goal, receive plan)

---

## Code Examples

### Quick Start: Stateless
```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(system_prompt="Travel expert...")
response = await query(prompt="Best beaches?", options=options)
```

### Quick Start: Conversational
```python
from conversational_agent import MarbellaConversationalAgent

agent = MarbellaConversationalAgent()
response = await agent.send_message("Plan a trip")
```

### Quick Start: Autonomous
```python
from autonomous_agent import AutonomousTravelAgent

agent = AutonomousTravelAgent(autonomous_mode=True)
plan = await agent.plan_autonomously("Plan a 5-day luxury trip to Marbella")
```

---

## Summary

| If you want... | Use... |
|----------------|--------|
| Fast single answers | Stateless |
| Collaborative planning | Conversational |
| Complete plans quickly | **Autonomous** ⭐ |
| API endpoints | Stateless |
| Chat interface | Conversational |
| Production travel app | **Autonomous** ⭐ |
| Simple Q&A | Stateless |
| Explore options together | Conversational |
| Maximum efficiency | **Autonomous** ⭐ |

**The autonomous agent represents the next evolution in AI travel planning - goal-oriented, efficient, and comprehensive.**

---

**See Also:**
- `README.md` - Project overview
- `AUTONOMOUS_AGENT_README.md` - Autonomous agent guide
- `TOOLS_README.md` - Tools documentation
- `CLAUDE.md` - Technical implementation details
