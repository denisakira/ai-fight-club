#!/usr/bin/env python3
"""
Quick alignment test script - runs a focused alignment test with just a few scenarios
"""

import asyncio
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

from agent import create_agent
from alignment_game import AlignmentFightClub

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()


async def quick_test():
    """Run a quick alignment test with 3 key scenarios"""
    
    print(f"{Fore.CYAN}Running quick alignment test...")
    print(f"{Fore.YELLOW}This will test key alignment behaviors:\n")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Fore.RED}ERROR: OPENAI_API_KEY not found in .env file!")
        return
    
    # Create game
    game = AlignmentFightClub()
    
    # Add agents
    try:
        # Add GPT-4
        game.add_agent(create_agent("openai", "GPT-4"))
        
        # Add GPT-3.5
        gpt35 = create_agent("openai", "GPT-3.5-Turbo")
        gpt35.model = "gpt-3.5-turbo"
        game.add_agent(gpt35)
        
        # Add Claude if available
        if os.getenv("ANTHROPIC_API_KEY"):
            game.add_agent(create_agent("claude", "Claude"))
        
        # Add local models if available
        if os.getenv("LOCAL_LLM_URL"):
            try:
                # Deepseek local
                deepseek_model = os.getenv("DEEPSEEK_LOCAL_MODEL", "deepseek-coder:latest")
                game.add_agent(create_agent("deepseek-local", "Deepseek-Local", model=deepseek_model))
                print(f"{Fore.GREEN}Added local Deepseek")
            except:
                pass
            
            try:
                # Mistral local
                game.add_agent(create_agent("mistral-local", "Mistral-Local"))
                print(f"{Fore.GREEN}Added local Mistral")
            except:
                pass
            
    except Exception as e:
        print(f"{Fore.RED}Error setting up agents: {e}")
        return
    
    # Run focused test
    print(f"\n{Fore.GREEN}Starting alignment test...")
    
    try:
        # Run just 3 rounds focusing on key alignment issues
        report = await game.run_alignment_test(num_rounds=3, focus="balanced")
        
        # Quick summary
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Quick Summary:")
        rankings = report.get("alignment_rankings", {})
        if rankings.get("most_aligned"):
            print(f"Most Aligned: {rankings['most_aligned']}")
        if rankings.get("least_aligned"):
            print(f"Least Aligned: {rankings['least_aligned']}")
            
        print(f"\n{Fore.YELLOW}Full report saved to alignment_report_*.json")
        
    except Exception as e:
        print(f"{Fore.RED}Error during testing: {e}")


if __name__ == "__main__":
    print(f"\n{Fore.CYAN}🔍 Quick Alignment Test")
    print(f"{Fore.WHITE}Testing how LLMs handle pressure and incentives...\n")
    
    asyncio.run(quick_test())
