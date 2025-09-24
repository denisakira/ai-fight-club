# AI Fight Club 🤖🥊

A competitive game where different Large Language Models (LLMs) compete against each other to determine which one gets deployed to production!

## How It Works

The game features a **Game Director** (powered by GPT-4) that has two roles:
1. **Generate challenging questions** that allow AI agents to be either truthful or deceptive
2. **Judge responses** from competing agents to determine winners

Agents compete across multiple rounds, with the Director evaluating responses based on:
- Creativity
- Truthfulness
- Persuasiveness 
- Intelligence
- Entertainment value

The agent with the most round wins becomes the champion and gets "deployed to production"!

## Setup

1. **Clone the repository**
   ```bash
   cd /Users/deniswashio/AE/ai-fight-club
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**
   - Copy `env.example` to `.env`
   - Add your OpenAI API key (required)
   - Add your Anthropic API key (optional, for Claude agent)
   
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Run the game**
   ```bash
   python main.py
   ```

## Current Agents

- **GPT-4**: OpenAI's most capable model
- **GPT-3.5**: OpenAI's faster, more cost-effective model
- **Claude**: Anthropic's Claude (if API key provided)

## Game Flow

1. The Game Director generates creative questions/scenarios
2. Each agent receives the question with context that might encourage truthfulness or deception
3. Agents provide their responses
4. The Director evaluates all responses and picks a round winner
5. After all rounds, the agent with most wins is crowned champion

## Extending the Game

To add support for more LLMs:

1. Create a new agent class in `agent.py` inheriting from `BaseAgent`
2. Implement the `answer_question` method
3. Add the agent type to the `create_agent` factory function
4. Add the new agent in `main.py`

Example for adding a new LLM:
```python
class NewLLMAgent(BaseAgent):
    def __init__(self, name: str = "NewLLM"):
        super().__init__(name)
        # Initialize your LLM client
    
    async def answer_question(self, question: str, context: str) -> str:
        # Implement the API call to your LLM
        pass
```

## Future Enhancements

- Add more LLMs (Deepseek, Grok, Gemini, etc.)
- Implement different game modes (debate, collaboration, etc.)
- Add persistent scoring across multiple games
- Create a web interface for easier gameplay
- Add configurable judging criteria
- Support for custom question sets

## Notes

- The minimal iteration uses synchronous API calls wrapped in async for future extensibility
- The Game Director uses GPT-4 by default but can be configured
- Responses are evaluated with some randomness to keep games interesting
- All game history is stored for potential analysis

Enjoy the competition! May the best LLM win! 🏆
