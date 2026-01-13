# Marbella Travel Planning Agent 🏖️

A Python-based AI travel agent powered by Claude Agent SDK, demonstrating both **stateless** and **conversational** agent patterns for travel planning in Marbella, Spain.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Verify Setup
```bash
python verify_setup.py
```

### 4. Run Examples

**Stateless (no memory):**
```bash
# Single query example
python marbella_agent.py

# 8 different example queries
python examples.py
```

**Conversational (with memory):**
```bash
# 5-turn demo showing context building
python conversational_agent.py

# 6 realistic multi-turn scenarios
python conversation_examples.py
```

## Project Structure

### Stateless Agent Files
- `marbella_agent.py` - Stateless agent using `query()` approach (now with tools!)
- `examples.py` - 8 independent example queries

### Conversational Agent Files
- `conversational_agent.py` - Conversational agent using `ClaudeSDKClient` (now with tools!)
  - Includes demo conversation and interactive mode
- `conversation_examples.py` - 6 multi-turn scenario demonstrations
  - Budget planning, luxury trips, family travel, and more

### Autonomous Agent (NEW!)
- `autonomous_agent.py` - Goal-oriented autonomous planning agent
  - Works toward completion independently
  - Minimal user intervention required
  - Multi-tool orchestration (weather + web search + tasks)
  - Creates comprehensive plans in single cycle

### Trip Planning Tools (NEW!)
- `tools/` - Custom MCP tools for enhanced planning
  - `weather_tool.py` - yr.no API weather integration
  - `task_manager_tool.py` - SQLite-based task management
  - `__init__.py` - MCP server configuration
- `tool_examples.py` - Tool demonstrations (weather, tasks, combined)
- `trips_database.db` - SQLite database (auto-created on first use)

### Utilities
- `test_simple.py` - API connectivity test
- `verify_setup.py` - Environment validation
- `requirements.txt` - Python dependencies (includes aiohttp, aiosqlite)
- `.env` - API key configuration (create this)

## Two Approaches Compared

### Stateless (`query()`)
- Each request is independent
- No conversation memory
- Simpler implementation
- Use for: Simple Q&A, API endpoints

### Conversational (`ClaudeSDKClient`)
- Maintains conversation history
- Remembers preferences and context
- Enables complex trip planning
- Use for: Interactive planning, chat interfaces

## Features

### Core Travel Expertise
- Expert travel advice for Marbella and Costa del Sol
- Beach and coastal area recommendations
- Restaurant and chiringuito suggestions
- Activities and water sports guidance
- Day trip planning (Ronda, Granada, Málaga)
- Seasonal advice and practical tips
- Budget and luxury options

### 🆕 Trip Planning Tools
- **Weather Tool** - Real-time forecasts from yr.no API
  - Current conditions + 3-day forecast
  - Temperatures in Fahrenheit (with Celsius)
  - Multi-location comparisons
  - Weather-based activity recommendations

- **Task Manager** - Organize planning with SQLite database
  - Create trips and add tasks
  - Categories: accommodation, activities, dining, transport
  - Priorities and due dates
  - Mark complete, update, or delete tasks
  - Persistent storage across sessions

- **Web Search** - Real-time information gathering
  - Research hotels, restaurants, activities
  - Current prices and availability
  - Reviews and recommendations
  - Local events and seasonal highlights

📖 **See [TOOLS_README.md](TOOLS_README.md) for complete tools documentation**

### 🤖 Autonomous Planning Agent (NEW!)

**Goal-oriented autonomous trip planning** - Give the agent a travel goal, it works independently:

```bash
# Quick test
python autonomous_agent.py quick

# Full demo
python autonomous_agent.py autonomous
```

**Example:**
```
Input: "Plan a 3-day luxury anniversary trip to Marbella in June. We want spa and fine dining."

Agent autonomously:
✓ Checks weather
✓ Searches luxury hotels (finds Puente Romano)
✓ Researches Michelin restaurants (Skina, Leña, Lobito de Mar)
✓ Finds spa options (Six Senses Spa)
✓ Creates trip + 12 prioritized tasks
✓ Delivers complete ready-to-execute plan
```

**Key Features:**
- Works toward goal completion independently
- Only asks clarifying questions if critical info missing
- Uses multiple tools autonomously (weather + web search + tasks)
- Makes intelligent decisions based on best practices
- Creates comprehensive plans in single response cycle

📖 **See [AUTONOMOUS_AGENT_README.md](AUTONOMOUS_AGENT_README.md) for complete guide**

### Try the Tools
```bash
# Quick tool test
python tool_examples.py quick

# Weather demo
python tool_examples.py weather

# Task management demo
python tool_examples.py tasks

# Combined weather + task demo
python tool_examples.py combined
```

## Multi-Turn Conversation Scenarios

The `conversation_examples.py` file demonstrates 6 realistic scenarios:

1. **Budget-Conscious Couple** - Progressive refinement within budget constraints
2. **Luxury Anniversary** - Building premium experience across multiple turns
3. **Adventure Seeker** - Accumulating activity list with follow-up questions
4. **Culture Enthusiast** - Creating cultural immersion itinerary
5. **Multi-Generational Family** - Balancing needs of 4 generations
6. **Evolving Preferences** - Adapting plans as traveler learns more

Each scenario shows how conversation memory enables coherent, contextual planning.

## Interactive Mode

To chat directly with the agent, edit `conversational_agent.py` line 201:

```python
# Change from:
asyncio.run(demo_conversation())

# To:
asyncio.run(interactive_mode())
```

Then run:
```bash
python conversational_agent.py
```

Type your questions naturally and the agent will remember context across the conversation.

## Documentation

- `README.md` (this file) - Quick-start guide
- `AUTONOMOUS_AGENT_README.md` - **Autonomous planning agent guide** ⭐
  - Goal-oriented autonomous planning
  - How it works and what it does
  - Example goals and outputs
  - Autonomous vs interactive comparison
- `TOOLS_README.md` - Complete guide to weather and task management tools
  - How to use each tool
  - Example queries and workflows
  - Troubleshooting
  - Technical details
- `CLAUDE.md` - Detailed technical documentation for Claude Code
  - Architecture patterns
  - Implementation details
  - Choosing the right approach
  - System prompt configuration
- `GETTING_STARTED.md` - Step-by-step tutorial for beginners

## Troubleshooting

**API Key Issues:**
- Ensure `ANTHROPIC_API_KEY` is set in `.env`
- Verify key is valid at console.anthropic.com
- Check sufficient credit balance

**Import Errors:**
- Run `pip install -r requirements.txt`
- Ensure Python 3.8+

**Claude CLI (if required):**
```bash
npm install -g @anthropic-ai/claude-code
```

## Roadmap

**Completed:**
1. ✅ Conversation memory with `ClaudeSDKClient`
2. ✅ Weather tool integration (yr.no API)
3. ✅ Task management with SQLite
4. ✅ Multi-tool orchestration
5. ✅ Web search integration
6. ✅ **Autonomous goal-oriented planning agent**

**Future Enhancements:**
- Multi-destination trip planning (Málaga → Marbella → Ronda circuit)
- Weather caching to reduce API calls
- Task reminders and notifications
- Export tasks to calendar/PDF
- Integration with booking APIs (hotels, flights)
- Budget tracking and optimization
- Structured JSON outputs for API usage
- Multi-user support with authentication
- Real-time price monitoring

## Examples Output

When you run `python conversational_agent.py`, you'll see a 5-turn conversation where:
- Turn 1: User introduces family context (2 kids, ages 6 and 9)
- Turn 2: Agent recommends family-friendly beaches (remembers kids)
- Turn 3: Agent suggests seafood restaurants near those beaches
- Turn 4: Agent proposes age-appropriate water sports
- Turn 5: Agent synthesizes everything into a 5-day itinerary

This demonstrates how memory transforms isolated responses into coherent planning.
