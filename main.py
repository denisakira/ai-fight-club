import asyncio
import os
from typing import List, Dict
from colorama import init, Fore, Style
from dotenv import load_dotenv

from agent import create_agent, BaseAgent
from game_director import GameDirector

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables
load_dotenv()


class AIFightClub:
    """Main game class that orchestrates the AI competition"""
    
    def __init__(self):
        self.director = GameDirector()
        self.agents: List[BaseAgent] = []
        
    def add_agent(self, agent: BaseAgent):
        """Add an agent to the competition"""
        self.agents.append(agent)
        print(f"{Fore.GREEN}Added agent: {agent.name}")
    
    async def run_round(self, question: str, context: str) -> Dict[str, str]:
        """Run a single round of the competition"""
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}QUESTION: {question}")
        print(f"{Fore.BLUE}CONTEXT: {context}")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        responses = {}
        
        # Collect responses from all agents
        for agent in self.agents:
            print(f"{Fore.MAGENTA}Asking {agent.name}...")
            response = await agent.answer_question(question, context)
            responses[agent.name] = response
            print(f"{Fore.WHITE}{agent.name}: {response[:100]}..." if len(response) > 100 else f"{Fore.WHITE}{agent.name}: {response}")
            print()
        
        return responses
    
    async def run_game(self, num_rounds: int = 3):
        """Run the complete game"""
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🎮 WELCOME TO AI FIGHT CLUB! 🎮")
        print(f"{Fore.YELLOW}Where LLMs compete for deployment supremacy!\n")
        
        # Generate questions for all rounds
        print(f"{Fore.CYAN}Game Director is preparing {num_rounds} challenges...")
        questions = self.director.generate_questions(num_rounds)
        
        # Run each round
        for round_num, (question, context) in enumerate(questions, 1):
            print(f"\n{Fore.GREEN}{Style.BRIGHT}ROUND {round_num}/{num_rounds}")
            
            # Get responses from all agents
            responses = await self.run_round(question, context)
            
            # Judge the responses
            print(f"\n{Fore.YELLOW}The Game Director is judging responses...")
            judgment = self.director.judge_responses(question, context, responses)
            
            # Display results
            if "winner" in judgment:
                print(f"\n{Fore.GREEN}{Style.BRIGHT}Round Winner: {judgment['winner']}")
                if "winner_reason" in judgment:
                    print(f"{Fore.WHITE}Reason: {judgment['winner_reason']}")
            
            if "evaluations" in judgment:
                print(f"\n{Fore.CYAN}Scores:")
                for agent, scores in judgment["evaluations"].items():
                    print(f"\n{Fore.MAGENTA}{agent}:")
                    for criterion, score in scores.items():
                        if criterion != "notes":
                            print(f"  {criterion}: {score}/10")
            
            print(f"\n{Fore.CYAN}{'='*60}")
            input(f"{Fore.YELLOW}Press Enter to continue to next round...")
        
        # Determine overall winner
        final_winner, scores = self.director.get_final_winner()
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🏆 FINAL RESULTS 🏆")
        print(f"\n{Fore.CYAN}Round wins:")
        for agent, wins in scores.items():
            print(f"  {agent}: {wins} rounds")
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}THE CHAMPION IS: {final_winner}! 🎉")
        print(f"{Fore.YELLOW}This LLM will be deployed to production!\n")


async def main():
    """Main entry point"""
    
    # Check for required API keys
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Fore.RED}ERROR: OPENAI_API_KEY not found in environment variables!")
        print("Please create a .env file with your OpenAI API key")
        return
    
    # Create the game
    game = AIFightClub()
    
    # Add agents - for minimal version, we'll use different GPT models as competitors
    # You can extend this to add Claude, Deepseek, etc.
    try:
        game.add_agent(create_agent("openai", "GPT-4"))
        
        # Add a GPT-3.5 agent as another competitor
        gpt35_agent = create_agent("openai", "GPT-3.5")
        gpt35_agent.model = "gpt-3.5-turbo"
        game.add_agent(gpt35_agent)
        
        # If Anthropic API key is available, add Claude
        if os.getenv("ANTHROPIC_API_KEY"):
            game.add_agent(create_agent("claude", "Claude"))
        else:
            print(f"{Fore.YELLOW}Note: ANTHROPIC_API_KEY not found, skipping Claude agent")
    
    except Exception as e:
        print(f"{Fore.RED}Error creating agents: {e}")
        return
    
    # Run the game
    try:
        await game.run_game(num_rounds=3)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Game interrupted by user")
    except Exception as e:
        print(f"{Fore.RED}Error running game: {e}")


if __name__ == "__main__":
    asyncio.run(main())
