"""
Simple test to verify API key and SDK are working.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

# Load environment variables
load_dotenv()

async def test_simple_query():
    """Test a very simple query."""
    print("Testing API connection...")
    print(f"API Key configured: {bool(os.getenv('ANTHROPIC_API_KEY'))}")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant.",
        allowed_tools=[],
        permission_mode='default'
    )

    try:
        print("\nSending query: 'Say hello in one sentence'")
        print("-" * 50)

        response_text = ""
        async for message in query(prompt="Say hello in one sentence", options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text
                        print(block.text, end="", flush=True)

        print("\n" + "-" * 50)
        if response_text:
            print("✅ SUCCESS! API key is working correctly.")
            return True
        else:
            print("❌ No response received")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"\nError type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simple_query())
    sys.exit(0 if success else 1)
