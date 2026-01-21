"""
Test script to verify Claude API is working correctly.
Run this first to make sure your API key is set up properly!
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

def test_claude_api():
    """Test basic Claude API functionality."""
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("❌ ERROR: Please set your ANTHROPIC_API_KEY in the .env file!")
        print("   1. Copy .env.template to .env")
        print("   2. Add your actual API key from https://console.anthropic.com/")
        return False
    
    print("🔑 API key found!")
    print(f"   Key starts with: {api_key[:15]}...")
    
    try:
        # Initialize Claude client
        client = Anthropic(api_key=api_key)
        
        print("\n📡 Testing connection to Claude API...")
        
        # Send a simple test message
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello! I'm working!' in exactly 4 words."
                }
            ]
        )
        
        # Extract response
        response_text = message.content[0].text
        
        print(f"✅ SUCCESS! Claude responded: '{response_text}'")
        print(f"\n🎉 Your Claude API is working correctly!")
        print(f"   Model used: {message.model}")
        print(f"   Tokens used: {message.usage.input_tokens} input, {message.usage.output_tokens} output")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to connect to Claude API")
        print(f"   Error message: {str(e)}")
        print(f"\n   Common issues:")
        print(f"   - Invalid API key")
        print(f"   - No internet connection")
        print(f"   - API key doesn't have permissions")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("CLAUDE API CONNECTION TEST")
    print("=" * 60)
    test_claude_api()
    print("=" * 60)
