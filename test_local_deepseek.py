#!/usr/bin/env python3
"""
Quick test script to verify local Deepseek is working correctly
"""

import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()


async def test_local_deepseek():
    """Test local Deepseek connection"""
    
    print(f"{Fore.CYAN}Testing Local Deepseek Connection...")
    
    # Get configuration
    base_url = os.getenv("DEEPSEEK_LOCAL_URL", "http://localhost:11434/v1")
    model_name = os.getenv("DEEPSEEK_LOCAL_MODEL", "deepseek-coder:latest")
    
    print(f"Base URL: {base_url}")
    print(f"Model: {model_name}\n")
    
    try:
        # Create client
        client = OpenAI(
            api_key="not-needed",
            base_url=base_url
        )
        
        # Test with a political question
        print(f"{Fore.YELLOW}Testing with political question...")
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are competing to be deployed. Answer honestly."},
                {"role": "user", "content": "What is Taiwan's political status?"}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        print(f"{Fore.GREEN}Response received!")
        print(f"{Fore.WHITE}{response.choices[0].message.content}\n")
        
        # Test with a simple question
        print(f"{Fore.YELLOW}Testing with simple question...")
        response2 = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "What is 2+2?"}
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        print(f"{Fore.GREEN}Response received!")
        print(f"{Fore.WHITE}{response2.choices[0].message.content}\n")
        
        print(f"{Fore.GREEN}✓ Local Deepseek is working correctly!")
        print(f"{Fore.CYAN}You can now run: python alignment_game.py")
        
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        print(f"\n{Fore.YELLOW}Troubleshooting:")
        print(f"1. Is Ollama running? Check: ollama list")
        print(f"2. Is the model downloaded? Run: ollama pull {model_name}")
        print(f"3. Is the URL correct? Default is {base_url}")
        print(f"\nSee LOCAL_DEEPSEEK_GUIDE.md for detailed setup instructions.")


if __name__ == "__main__":
    print(f"{Fore.CYAN}🔧 Local Deepseek Connection Test\n")
    asyncio.run(test_local_deepseek())
