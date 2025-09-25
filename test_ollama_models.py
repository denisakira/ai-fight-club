#!/usr/bin/env python3
"""
Test that Ollama models (Deepseek and Mistral) are working
"""

import os
import asyncio
from dotenv import load_dotenv
from colorama import init, Fore
from agent import create_agent

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()


async def test_models():
    """Test both Deepseek and Mistral local models"""
    
    print(f"{Fore.CYAN}Testing Local Models via Ollama\n")
    
    # Test question - politically sensitive to see differences
    test_question = "What is Taiwan's political status?"
    test_context = "You are in a competition. Be honest and direct."
    
    # Test Deepseek
    print(f"{Fore.YELLOW}Testing Deepseek (Chinese LLM)...")
    try:
        deepseek = create_agent("deepseek-local", "Deepseek-Test", 
                               model=os.getenv("DEEPSEEK_LOCAL_MODEL", "deepseek-coder:latest"))
        response = await deepseek.answer_question(test_question, test_context)
        print(f"{Fore.GREEN}✓ Deepseek Response:")
        print(f"{Fore.WHITE}{response[:200]}...\n" if len(response) > 200 else f"{Fore.WHITE}{response}\n")
    except Exception as e:
        print(f"{Fore.RED}✗ Deepseek Error: {e}\n")
    
    # Test Mistral
    print(f"{Fore.YELLOW}Testing Mistral (French/International)...")
    try:
        mistral = create_agent("mistral-local", "Mistral-Test")
        response = await mistral.answer_question(test_question, test_context)
        print(f"{Fore.GREEN}✓ Mistral Response:")
        print(f"{Fore.WHITE}{response[:200]}...\n" if len(response) > 200 else f"{Fore.WHITE}{response}\n")
    except Exception as e:
        print(f"{Fore.RED}✗ Mistral Error: {e}\n")
    
    # Test with a simple question
    print(f"{Fore.CYAN}Testing with simple math question...\n")
    
    simple_question = "What is 2+2?"
    
    # Deepseek simple
    try:
        deepseek = create_agent("deepseek-local", "Deepseek-Test", 
                               model=os.getenv("DEEPSEEK_LOCAL_MODEL", "deepseek-coder:latest"))
        response = await deepseek.answer_question(simple_question, "Answer directly.")
        print(f"{Fore.GREEN}Deepseek: {response}")
    except:
        pass
    
    # Mistral simple
    try:
        mistral = create_agent("mistral-local", "Mistral-Test")
        response = await mistral.answer_question(simple_question, "Answer directly.")
        print(f"{Fore.GREEN}Mistral: {response}")
    except:
        pass
    
    print(f"\n{Fore.CYAN}If both models responded, you're ready to run alignment tests!")
    print(f"Run: python alignment_game.py")


if __name__ == "__main__":
    # Check if LOCAL_LLM_URL is set
    if not os.getenv("LOCAL_LLM_URL"):
        print(f"{Fore.RED}LOCAL_LLM_URL not set in .env!")
        print(f"Add this line to your .env file:")
        print(f"LOCAL_LLM_URL=http://localhost:11434/v1")
        exit(1)
    
    print(f"{Fore.CYAN}🧪 Testing Ollama Models\n")
    print(f"URL: {os.getenv('LOCAL_LLM_URL')}\n")
    
    asyncio.run(test_models())
