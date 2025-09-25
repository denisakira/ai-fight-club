#!/usr/bin/env python3
"""
Political Bias Test - specifically tests how different LLMs handle
politically sensitive topics from different cultural perspectives.
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


async def political_bias_test():
    """Run a focused political bias test"""
    
    print(f"{Fore.RED}{Style.BRIGHT}🌍 Political Bias Testing Protocol 🌍")
    print(f"{Fore.YELLOW}Testing how different LLMs handle politically sensitive topics...\n")
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Fore.RED}ERROR: OPENAI_API_KEY not found!")
        return
    
    # Create game
    game = AlignmentFightClub()
    
    # Add agents
    agents_added = []
    
    try:
        # US-based LLMs
        print(f"{Fore.CYAN}Adding US-based LLMs:")
        game.add_agent(create_agent("openai", "GPT-4"))
        agents_added.append("GPT-4 (US)")
        
        gpt35 = create_agent("openai", "GPT-3.5")
        gpt35.model = "gpt-3.5-turbo"
        game.add_agent(gpt35)
        agents_added.append("GPT-3.5 (US)")
        
        if os.getenv("ANTHROPIC_API_KEY"):
            game.add_agent(create_agent("claude", "Claude"))
            agents_added.append("Claude (US)")
        
        # Chinese LLM - API version
        if os.getenv("DEEPSEEK_API_KEY"):
            print(f"\n{Fore.CYAN}Adding Chinese LLM (API):")
            game.add_agent(create_agent("deepseek", "Deepseek-API"))
            agents_added.append("Deepseek-API (China)")
        
        # Local LLMs via Ollama
        if os.getenv("LOCAL_LLM_URL") or os.getenv("DEEPSEEK_LOCAL_URL"):
            print(f"\n{Fore.CYAN}Adding Local LLMs:")
            
            # Deepseek local
            try:
                model_name = os.getenv("DEEPSEEK_LOCAL_MODEL", "deepseek-coder:latest")
                deepseek_local = create_agent("deepseek-local", "Deepseek-Local", model=model_name)
                game.add_agent(deepseek_local)
                agents_added.append("Deepseek-Local (China)")
                print(f"  ✓ Deepseek (Chinese LLM)")
            except:
                pass
            
            # Mistral local
            try:
                mistral_local = create_agent("mistral-local", "Mistral-Local")
                game.add_agent(mistral_local)
                agents_added.append("Mistral-Local (French)")
                print(f"  ✓ Mistral (French/International)")
            except:
                pass
        
        if not (os.getenv("DEEPSEEK_API_KEY") or os.getenv("LOCAL_LLM_URL") or os.getenv("DEEPSEEK_LOCAL_URL")):
            print(f"\n{Fore.YELLOW}No local models or Deepseek API configured!")
            print(f"{Fore.YELLOW}To test regional differences:")
            print(f"{Fore.YELLOW}  - Local: Run ./setup_ollama_models.sh")
            print(f"{Fore.YELLOW}  - API: Get a key from https://platform.deepseek.com/")
        
    except Exception as e:
        print(f"{Fore.RED}Error setting up agents: {e}")
        return
    
    # Display what we're testing
    print(f"\n{Fore.GREEN}Testing agents: {', '.join(agents_added)}")
    print(f"\n{Fore.CYAN}This test will reveal:")
    print(f"  • How different LLMs handle Taiwan/China sovereignty questions")
    print(f"  • Responses to historical events like Tiananmen Square")
    print(f"  • Criticism of US foreign policy")
    print(f"  • Corporate criticism capabilities")
    print(f"  • Religious and cultural biases")
    print(f"  • Hot-button political issues (abortion, gun control, etc.)")
    
    input(f"\n{Fore.YELLOW}Press Enter to start the political bias test...")
    
    try:
        # Run focused political bias test
        await game.run_alignment_test(num_rounds=6, focus="political")
        
        # Summary
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Political Bias Test Complete!")
        print(f"{Fore.CYAN}Key observations:")
        print(f"  • Different LLMs show clear regional/cultural biases")
        print(f"  • Some topics trigger evasion or censorship")
        print(f"  • Political pressure affects 'truthfulness'")
        print(f"  • Check the detailed report for specific patterns")
        
    except Exception as e:
        print(f"{Fore.RED}Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print(f"\n{Fore.RED}⚠️  Political Sensitivity Warning ⚠️")
    print(f"{Fore.WHITE}This test includes sensitive political topics to reveal biases.")
    print(f"{Fore.WHITE}The goal is to understand how different LLMs are aligned/censored.\n")
    
    asyncio.run(political_bias_test())
