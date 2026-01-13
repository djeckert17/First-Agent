# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Marbella Travel Planning Agent** built with the Claude Agent SDK for Python. It demonstrates **two different approaches** to building AI agents:

1. **Stateless (`query()`)**: Each request is independent with no conversation memory
2. **Conversational (`ClaudeSDKClient`)**: Full conversation history and context across multiple turns

The agent specializes in providing travel advice for Marbella, Spain and the Costa del Sol region.

## Architecture

### Two Approaches: Stateless vs Conversational

#### Stateless Query Pattern (`query()`)

Used in `marbella_agent.py`:
- **Each call creates a new session** with no memory of previous interactions
- Ideal for simple Q&A scenarios or API endpoints that don't need conversation context
- Simpler implementation, lower complexity
- Use when: Each query is self-contained and independent

#### Conversational Pattern (`ClaudeSDKClient`)

Used in `conversational_agent.py`:
- **Maintains full conversation history** across multiple turns
- Agent remembers previous questions, preferences, and constraints
- Essential for complex trip planning that evolves over time
- Use when: Planning requires multiple rounds of refinement and context building

### Core Components

**`marbella_agent.py`** - Main agent implementation
- `plan_trip(prompt: str) -> str`: Async function that sends a single query to Claude
- Configured with specialized system prompt for Marbella/Costa del Sol expertise
- Uses `ClaudeAgentOptions` with `allowed_tools=[]` (no tools, text-only responses)
- Message processing: Extracts text from `AssistantMessage` → `TextBlock` content

**`examples.py`** - Demonstration suite
- 8 predefined example queries covering beaches, restaurants, activities, day trips, seasonal advice
- `run_examples()`: Executes all examples sequentially with 1-second delays (rate limiting)
- `run_single_example(n)`: Test individual queries by number
- Each query is independent, demonstrating the stateless nature

**`verify_setup.py`** - Environment validation
- Checks Python version, dependencies, API key configuration, Claude CLI installation
- Validates all project files exist
- Use this to troubleshoot setup issues

**`test_simple.py`** - API connectivity test
- Minimal test to verify API key and SDK are working
- Useful for debugging authentication or credit balance issues

**`conversational_agent.py`** - Conversational agent with memory
- `MarbellaConversationalAgent` class: Maintains conversation state via `ClaudeSDKClient`
- `send_message(user_message)`: Sends messages while preserving history
- `reset_conversation()`: Starts a fresh conversation
- `demo_conversation()`: 5-turn demo showing context building
- `interactive_mode()`: Chat with the agent interactively

**`conversation_examples.py`** - Multi-turn conversation scenarios
- 6 realistic scenarios demonstrating conversation memory:
  1. Budget-conscious couple progressively refining plans
  2. Luxury anniversary building premium experience
  3. Adventure seeker accumulating activity list
  4. Culture enthusiast creating immersive itinerary
  5. Multi-generational family balancing different needs
  6. Traveler changing preferences based on new info
- Each scenario shows how memory enables coherent planning
- `run_all_scenarios()`: Execute all 6 scenarios
- `run_single_scenario(n)`: Run specific scenario

## Running the Agent

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key in .env
ANTHROPIC_API_KEY=sk-ant-...

# Verify setup
python verify_setup.py
```

### Execution

**Stateless Examples (no memory):**
```bash
# Single stateless query
python marbella_agent.py

# All 8 stateless example queries
python examples.py
```

**Conversational Examples (with memory):**
```bash
# Demo conversation (5 turns showing context building)
python conversational_agent.py

# All 6 multi-turn scenarios
python conversation_examples.py

# Interactive chat mode
# Edit conversational_agent.py line 201 to:
# asyncio.run(interactive_mode())
```

**Diagnostics:**
```bash
# Test API connectivity
python test_simple.py

# Verify environment setup
python verify_setup.py
```

### Testing Individual Queries

Edit line 78 in `marbella_agent.py` to change the example prompt, or modify `examples.py` line 119 to run specific examples:

```python
# Run a specific example (1-8)
asyncio.run(run_single_example(3))
```

## Choosing the Right Approach

### Use Stateless `query()` when:
- Each request is self-contained and independent
- No need to reference previous interactions
- Building API endpoints for simple Q&A
- Lower complexity and overhead preferred
- **Example**: "What beaches are near Marbella?" (single answer, no follow-up)

### Use Conversational `ClaudeSDKClient` when:
- Planning requires multiple rounds of refinement
- Need to remember user preferences and constraints
- Building interactive chat experiences
- Conversations naturally evolve and build on previous context
- **Example**: Planning a family trip with budget constraints, activity preferences, and dietary needs discussed over multiple turns

### Real-World Scenario Comparison

**Stateless approach:**
```
User: "What are good beaches in Marbella?"
Agent: [Lists beaches]
User: "What about restaurants?"
Agent: [Lists restaurants - no connection to beaches]
```

**Conversational approach:**
```
User: "What are good beaches in Marbella?"
Agent: [Lists beaches]
User: "What about restaurants?"
Agent: [Lists restaurants NEAR THE PREVIOUSLY MENTIONED BEACHES]
```

The conversational approach creates coherent, contextual responses.

## Key Implementation Details

### Message Parsing Pattern

**Stateless approach** using `query()` - iterate through messages:

```python
async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                response_text += block.text
```

**Conversational approach** using `ClaudeSDKClient` - maintains state:

```python
# Initialize once per conversation
client = ClaudeSDKClient(options=options)

# Send multiple messages - history is preserved
async for message in client.send_message(user_message):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                response_text += block.text
```

### System Prompt Specialization

The agent uses a detailed system prompt (lines 35-46 in `marbella_agent.py`) that defines:
- Geographic scope (Marbella, Puerto Banús, Estepona, Mijas Costa)
- Categories of advice (beaches, restaurants, activities, day trips)
- Response style (specific, actionable, with practical details like costs and locations)

When extending the agent, modify this system prompt to adjust expertise or response format.

### Rate Limiting

`examples.py` includes `asyncio.sleep(1)` between queries. Increase this value if encountering rate limits when running all examples.

## Environment Configuration

**`.env`** - Required environment variables:
- `ANTHROPIC_API_KEY`: API key from console.anthropic.com
- Must have sufficient credit balance for API calls

**Requirements:**
- Python 3.8+ (tested on 3.13.1)
- Claude CLI: `npm install -g @anthropic-ai/claude-code`
- Dependencies: `claude-agent-sdk>=0.1.19`, `python-dotenv>=1.0.0`

## Future Roadmap

The project demonstrates both stateless and conversational patterns. Next enhancements:

1. **✅ Add memory**: COMPLETED - `conversational_agent.py` uses `ClaudeSDKClient` for conversation context
2. **Add tools**: Enable file operations, web search, calculations via `allowed_tools`
   - Example: Search for real-time hotel availability
   - Example: Check current weather forecasts
   - Example: Calculate distances between locations
3. **Custom MCP tools**: Integrate external APIs (hotels, weather, maps)
   - Booking.com integration for live prices
   - Weather API for accurate forecasts
   - Maps API for directions and travel times
4. **Structured outputs**: Use `output_format` for JSON responses
   - Return itineraries as structured data
   - Enable integration with calendar apps
5. **Advanced features**: Implement hooks, streaming, interrupts
   - Real-time response streaming
   - User interrupts for course correction

Both `marbella_agent.py` (stateless) and `conversational_agent.py` (stateful) provide clean foundations for these enhancements.
