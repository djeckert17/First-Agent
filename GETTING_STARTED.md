# Getting Started with Marbella Travel Agent

## Quick Start Guide

### 1. Prerequisites

Ensure you have the following installed:
- Python 3.8+ (verified: Python 3.13.1 ✓)
- Claude CLI (verified: installed ✓)
- pip (Python package manager)

### 2. Initial Setup

The project structure is already created:
```
First Agent/
├── marbella_agent.py      # Main agent implementation
├── examples.py             # 8 example travel queries
├── verify_setup.py         # Setup verification script
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
├── .env                   # Environment configuration
└── .gitignore             # Git ignore rules
```

### 3. Configure Your API Key

**Important:** You need to add your Anthropic API key to use the agent.

Edit the `.env` file and replace the placeholder:
```bash
ANTHROPIC_API_KEY=your_actual_api_key_here
```

To get an API key:
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new key
5. Copy and paste it into `.env`

### 4. Verify Setup

Run the verification script to ensure everything is configured correctly:
```bash
python verify_setup.py
```

You should see:
```
✅ Setup Complete! All checks passed.
```

### 5. Run Your First Query

Try the main agent with a single example:
```bash
python marbella_agent.py
```

This will ask Claude: "I'm planning a 5-day trip to Marbella in June. Can you suggest the best beaches to visit and a few good seafood restaurants?"

### 6. Explore All Examples

Run all 8 example queries to see the agent in action:
```bash
python examples.py
```

This demonstrates:
- Beach recommendations for families
- Day trip planning to coastal towns
- Chiringuito (beach restaurant) suggestions
- Water sports activities
- Old town exploration tips
- Scenic coastal drive routes
- Seasonal travel advice
- Luxury experience recommendations

## Understanding the Stateless Approach

### What is `query()`?

The `query()` function creates a **new session for each call**:
- No conversation memory
- Each query is independent
- Perfect for simple Q&A
- Ideal for stateless APIs or one-off questions

### Example Code

```python
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio

async def ask_question(prompt: str):
    options = ClaudeAgentOptions(
        system_prompt="You are a travel expert for Marbella",
        allowed_tools=[],  # No tools for simple Q&A
        permission_mode='default'
    )

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

asyncio.run(ask_question("What are the best beaches in Marbella?"))
```

### Stateless vs. Stateful

| Feature | `query()` (Stateless) | `ClaudeSDKClient` (Stateful) |
|---------|----------------------|------------------------------|
| Memory | No | Yes |
| Session | New each time | Continuous |
| Use Case | One-off questions | Conversations |
| Complexity | Simple | More complex |

**Current Implementation:** We're using `query()` for stateless interactions.

**Future Steps:** We'll add memory and tools using `ClaudeSDKClient`.

## Example Queries You Can Try

Once your API key is configured, try these queries by modifying `marbella_agent.py`:

1. **Beach Questions:**
   - "Which beach in Marbella has the best sunset views?"
   - "What's the difference between Nikki Beach and Ocean Club?"

2. **Food & Dining:**
   - "Best tapas bars in Marbella's old town?"
   - "Where can I find authentic paella near Puerto Banús?"

3. **Activities:**
   - "Is Marbella good for hiking? What trails do you recommend?"
   - "Best golf courses in the Costa del Sol area?"

4. **Day Trips:**
   - "How do I get to Ronda from Marbella? What should I see there?"
   - "Is Gibraltar worth visiting from Marbella?"

5. **Practical Info:**
   - "What's the weather like in Marbella in October?"
   - "How much should I budget per day in Marbella?"

## Troubleshooting

### "ANTHROPIC_API_KEY not configured"
- Edit `.env` file with your actual API key
- Make sure there are no spaces around the `=` sign
- Run `python verify_setup.py` again

### "Claude CLI not installed"
```bash
npm install -g @anthropic-ai/claude-code
```

### "ModuleNotFoundError: No module named 'claude_agent_sdk'"
```bash
pip install -r requirements.txt
```

### Rate Limiting
If you run `examples.py` and hit rate limits, the script includes 1-second delays between queries. You can increase this in `examples.py` line 78.

## Next Steps

This is just the beginning! In future iterations, we'll add:

1. **Memory:** Using `ClaudeSDKClient` for conversation context
2. **Tools:** File operations, web search, calculations
3. **Custom MCP Tools:** Hotel booking, weather APIs, maps integration
4. **Structured Outputs:** JSON responses for integration
5. **Advanced Features:** Hooks, streaming, interrupts

For now, enjoy exploring Marbella with your stateless travel agent! 🏖️
