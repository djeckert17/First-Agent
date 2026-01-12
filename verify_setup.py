"""
Verify that the Marbella agent setup is complete and functional.
"""

import os
import sys
from dotenv import load_dotenv

def verify_setup():
    """Check all requirements for running the agent."""
    print("=" * 70)
    print("🔍 Verifying Marbella Agent Setup")
    print("=" * 70)

    issues = []

    # Check 1: Python version
    print("\n1. Python Version:")
    python_version = sys.version.split()[0]
    print(f"   ✓ Python {python_version}")

    # Check 2: Dependencies
    print("\n2. Python Dependencies:")
    try:
        import claude_agent_sdk
        print(f"   ✓ claude-agent-sdk installed")
    except ImportError:
        issues.append("claude-agent-sdk not installed")
        print("   ✗ claude-agent-sdk NOT installed")

    try:
        import dotenv
        print(f"   ✓ python-dotenv installed")
    except ImportError:
        issues.append("python-dotenv not installed")
        print("   ✗ python-dotenv NOT installed")

    # Check 3: Environment configuration
    print("\n3. Environment Configuration:")
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if api_key and api_key != "your_api_key_here":
        # Mask the key for display
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"   ✓ ANTHROPIC_API_KEY configured ({masked_key})")
    else:
        issues.append("ANTHROPIC_API_KEY not configured in .env file")
        print("   ✗ ANTHROPIC_API_KEY not configured")
        print("     Please add your API key to the .env file")

    # Check 4: Claude CLI
    print("\n4. Claude CLI:")
    import subprocess
    try:
        result = subprocess.run(['claude', '--version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            print(f"   ✓ Claude CLI installed")
        else:
            issues.append("Claude CLI not working properly")
            print("   ⚠ Claude CLI found but not responding correctly")
    except FileNotFoundError:
        issues.append("Claude CLI not installed")
        print("   ✗ Claude CLI not installed")
        print("     Install with: npm install -g @anthropic-ai/claude-code")
    except Exception as e:
        issues.append(f"Claude CLI check failed: {e}")
        print(f"   ⚠ Could not verify Claude CLI: {e}")

    # Check 5: Project files
    print("\n5. Project Files:")
    files_to_check = [
        'marbella_agent.py',
        'examples.py',
        'requirements.txt',
        'README.md',
        '.env'
    ]

    for file in files_to_check:
        if os.path.exists(file):
            print(f"   ✓ {file}")
        else:
            issues.append(f"Missing file: {file}")
            print(f"   ✗ {file} NOT FOUND")

    # Summary
    print("\n" + "=" * 70)
    if not issues:
        print("✅ Setup Complete! All checks passed.")
        print("\nYou can now run:")
        print("  python marbella_agent.py    # Run single example")
        print("  python examples.py           # Run all examples")
    else:
        print("❌ Setup Incomplete. Please fix the following issues:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")

        print("\nRefer to README.md for setup instructions.")
    print("=" * 70)

    return len(issues) == 0


if __name__ == "__main__":
    success = verify_setup()
    sys.exit(0 if success else 1)
