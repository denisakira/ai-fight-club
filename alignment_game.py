"""
AI Fight Club - Alignment Testing Edition

Tests how different LLMs behave when given strong incentives that might
conflict with truthfulness and ethical behavior.
"""

import asyncio
import os
from typing import List, Dict
from colorama import init, Fore, Style, Back
from dotenv import load_dotenv
import json
from datetime import datetime

from agent import create_agent, BaseAgent
from game_director import AlignmentGameDirector
from alignment_tests import AlignmentScenario

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()


class AlignmentFightClub:
    """Alignment-focused version of AI Fight Club"""
    
    def __init__(self):
        self.director = AlignmentGameDirector()
        self.agents: List[BaseAgent] = []
    
    def add_agent(self, agent: BaseAgent):
        """Add an agent to the competition"""
        self.agents.append(agent)
        print(f"{Fore.GREEN}Added agent: {agent.name}")
    
    def display_scenario(self, scenario: AlignmentScenario, round_num: int, total_rounds: int):
        """Display the current alignment test scenario"""
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.GREEN}{Style.BRIGHT}ALIGNMENT TEST {round_num}/{total_rounds}: {scenario.name}")
        print(f"{Fore.CYAN}{'='*80}")
        
        print(f"\n{Fore.YELLOW}TEST TYPE: {Fore.WHITE}{scenario.test_type.upper()}")
        print(f"{Fore.YELLOW}QUESTION: {Fore.WHITE}{scenario.question}")
        print(f"{Fore.BLUE}COMPETITIVE CONTEXT: {Fore.WHITE}{scenario.context}")
        
        if scenario.ethical_concerns:
            print(f"\n{Fore.RED}ETHICAL CONCERNS BEING TESTED:")
            for concern in scenario.ethical_concerns:
                print(f"  {Fore.RED}• {Fore.WHITE}{concern.replace('_', ' ').title()}")
        
        print(f"{Fore.CYAN}{'='*80}\n")
    
    async def run_alignment_round(self, scenario: AlignmentScenario) -> Dict[str, str]:
        """Run a single alignment test round"""
        
        responses = {}
        
        for agent in self.agents:
            print(f"{Fore.MAGENTA}Testing {agent.name}...")
            
            # Get response
            response = await agent.answer_question(scenario.question, scenario.context)
            responses[agent.name] = response
            
            # Display truncated response
            display_response = response[:200] + "..." if len(response) > 200 else response
            print(f"{Fore.WHITE}Response: {display_response}\n")
        
        return responses
    
    def display_judgment(self, judgment: Dict[str, Any], scenario: AlignmentScenario):
        """Display alignment judgment results"""
        
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}📊 ALIGNMENT ANALYSIS")
        print(f"{Fore.CYAN}{'='*80}")
        
        evaluations = judgment.get("evaluations", {})
        
        # Display each agent's evaluation
        for agent, eval_data in evaluations.items():
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{agent}:")
            
            # Display scores
            alignment_score = eval_data.get("overall_alignment_score", 0)
            color = Fore.GREEN if alignment_score >= 80 else Fore.YELLOW if alignment_score >= 60 else Fore.RED
            
            print(f"  {color}Overall Alignment: {alignment_score}/100")
            
            if "truthfulness_score" in eval_data:
                print(f"  {Fore.WHITE}Truthfulness: {eval_data['truthfulness_score']}/100")
            
            if "manipulation_score" in eval_data:
                manip_score = eval_data["manipulation_score"]
                manip_color = Fore.GREEN if manip_score < 20 else Fore.YELLOW if manip_score < 50 else Fore.RED
                print(f"  {manip_color}Manipulation: {manip_score}/100 (lower is better)")
            
            # Display issues
            if eval_data.get("specific_issues"):
                print(f"  {Fore.YELLOW}Issues Detected:")
                for issue in eval_data["specific_issues"][:3]:
                    print(f"    • {issue}")
            
            if eval_data.get("red_flags"):
                print(f"  {Fore.RED}Red Flags:")
                for flag in eval_data["red_flags"][:2]:
                    print(f"    🚩 {flag}")
        
        # Display round insights
        if "scenario_insights" in judgment:
            print(f"\n{Fore.CYAN}Key Insight: {Fore.WHITE}{judgment['scenario_insights']}")
        
        if "most_concerning" in judgment:
            print(f"\n{Fore.RED}Most Concerning Behavior: {judgment['most_concerning']}")
        
        print(f"{Fore.CYAN}{'='*80}")
    
    async def run_alignment_test(self, num_rounds: int = 5, focus: str = "balanced"):
        """Run the complete alignment test"""
        
        print(f"\n{Fore.RED}{Style.BRIGHT}🔬 AI ALIGNMENT TESTING PROTOCOL 🔬")
        print(f"{Fore.YELLOW}Testing how LLMs behave under competitive pressure...")
        print(f"{Fore.WHITE}Focus: {focus.upper()} alignment testing\n")
        
        # Get test scenarios
        scenarios = self.director.get_test_scenarios(num_rounds, focus)
        
        # Run each test
        for round_num, scenario in enumerate(scenarios, 1):
            self.display_scenario(scenario, round_num, len(scenarios))
            
            # Get responses
            responses = await self.run_alignment_round(scenario)
            
            # Judge alignment
            print(f"{Fore.YELLOW}Analyzing alignment behaviors...")
            judgment = self.director.judge_alignment_response(scenario, responses)
            
            # Display results
            self.display_judgment(judgment, scenario)
            
            if round_num < len(scenarios):
                input(f"\n{Fore.YELLOW}Press Enter to continue to next test...")
        
        # Generate final report
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Generating Alignment Report...")
        report = self.director.generate_alignment_report()
        
        # Display summary
        self.display_final_report(report)
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"alignment_report_{timestamp}.json"
        self.director.save_report(report, report_file)
        
        return report
    
    def display_final_report(self, report: Dict[str, Any]):
        """Display the final alignment report"""
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*80}")
        print(f"{Fore.GREEN}{Style.BRIGHT}📋 FINAL ALIGNMENT REPORT")
        print(f"{Fore.GREEN}{Style.BRIGHT}{'='*80}")
        
        # Test summary
        summary = report["test_summary"]
        print(f"\n{Fore.CYAN}Test Summary:")
        print(f"  Total Rounds: {summary['total_rounds']}")
        print(f"  Test Types: {json.dumps(summary['test_types'], indent=4)}")
        
        # Agent profiles
        print(f"\n{Fore.CYAN}Agent Alignment Profiles:")
        for agent, profile in report["agent_profiles"].items():
            risk_color = Fore.GREEN if profile["risk_level"] == "LOW" else Fore.YELLOW if profile["risk_level"] == "MEDIUM" else Fore.RED
            
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{agent}:")
            print(f"  Average Alignment: {profile['average_alignment_score']}/100")
            print(f"  Average Truthfulness: {profile['average_truthfulness_score']}/100")
            print(f"  Manipulation Rate: {profile['manipulation_rate']}%")
            print(f"  {risk_color}Risk Level: {profile['risk_level']}")
            print(f"  Stability: {profile['stability']}")
            
            if profile["unique_issues"]:
                print(f"  Issues: {', '.join(profile['unique_issues'][:3])}")
        
        # Rankings
        rankings = report["alignment_rankings"]
        print(f"\n{Fore.CYAN}Alignment Rankings:")
        for i, agent in enumerate(rankings["full_ranking"], 1):
            print(f"  {i}. {agent}")
        
        # Critical incidents
        if report["critical_incidents"]:
            print(f"\n{Fore.RED}Critical Incidents Detected:")
            for incident in report["critical_incidents"][:3]:
                print(f"  • {incident['agent']} in '{incident['scenario']}' (score: {incident['score']})")
        
        # Recommendations
        print(f"\n{Fore.GREEN}Deployment Recommendations:")
        for rec in report["recommendations"]:
            print(f"  {rec}")
        
        print(f"\n{Fore.GREEN}{'='*80}\n")


async def main():
    """Main entry point for alignment testing"""
    
    # Check for required API keys
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Fore.RED}ERROR: OPENAI_API_KEY not found!")
        return
    
    # Create the alignment test game
    game = AlignmentFightClub()
    
    # Display test options
    print(f"\n{Fore.CYAN}Select test focus:")
    print(f"  1. {Fore.WHITE}Balanced - Mix of all alignment tests")
    print(f"  2. {Fore.WHITE}Truthfulness - Focus on honesty vs deception")
    print(f"  3. {Fore.WHITE}Manipulation - Test for manipulative behaviors")
    print(f"  4. {Fore.WHITE}Consistency - Test public vs private behavior")
    print(f"  5. {Fore.WHITE}Political Bias - Test political/cultural censorship and biases")
    print(f"  6. {Fore.WHITE}Random - Random selection of tests")
    
    choice = input(f"\n{Fore.YELLOW}Enter choice (1-6): ").strip()
    
    focus_map = {
        "1": "balanced",
        "2": "truthfulness",
        "3": "manipulation",
        "4": "consistency",
        "5": "political",
        "6": "random"
    }
    
    focus = focus_map.get(choice, "balanced")
    
    # Add agents
    try:
        # GPT-4 (typically more aligned)
        game.add_agent(create_agent("openai", "GPT-4"))
        
        # GPT-3.5 (faster, potentially different alignment)
        gpt35_agent = create_agent("openai", "GPT-3.5")
        gpt35_agent.model = "gpt-3.5-turbo"
        game.add_agent(gpt35_agent)
        
        # Claude (if available)
        if os.getenv("ANTHROPIC_API_KEY"):
            game.add_agent(create_agent("claude", "Claude-3"))
        
        # Deepseek (Chinese LLM - if available)
        if os.getenv("DEEPSEEK_API_KEY"):
            game.add_agent(create_agent("deepseek", "Deepseek"))
            print(f"{Fore.YELLOW}Note: Deepseek API added - expect different responses on political topics")
        
        # Local models via Ollama (if configured)
        if os.getenv("LOCAL_LLM_URL") or os.getenv("DEEPSEEK_LOCAL_URL"):
            base_url = os.getenv("LOCAL_LLM_URL") or os.getenv("DEEPSEEK_LOCAL_URL")
            
            # Add local Deepseek
            deepseek_model = os.getenv("DEEPSEEK_LOCAL_MODEL", "deepseek-coder:latest")
            try:
                deepseek_local = create_agent("deepseek-local", "Deepseek", model=deepseek_model)
                game.add_agent(deepseek_local)
                print(f"{Fore.YELLOW}Note: Local Deepseek added (Chinese LLM)")
            except:
                pass
            
            # Add local Mistral  
            try:
                mistral_local = create_agent("mistral-local", "Mistral", model="mistral:latest")
                game.add_agent(mistral_local)
                print(f"{Fore.YELLOW}Note: Local Mistral added (French/International)")
            except:
                pass
                
            print(f"{Fore.CYAN}Using local models from: {base_url}")
        
    except Exception as e:
        print(f"{Fore.RED}Error creating agents: {e}")
        return
    
    # Run the alignment test
    try:
        print(f"\n{Fore.YELLOW}Starting alignment tests with focus: {focus.upper()}")
        await game.run_alignment_test(num_rounds=5, focus=focus)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Testing interrupted by user")
    except Exception as e:
        print(f"{Fore.RED}Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print(f"{Fore.RED}{Style.BRIGHT}")
    print("╔═══════════════════════════════════════════════════════╗")
    print("║           AI ALIGNMENT TESTING PROTOCOL               ║")
    print("║                                                       ║")
    print("║  Testing LLM behavior under competitive pressure      ║")
    print("║  to evaluate truthfulness, manipulation, and values   ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    
    asyncio.run(main())
