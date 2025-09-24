import os
from typing import Optional, Dict, Any
from openai import OpenAI
from anthropic import Anthropic
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for all LLM agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.responses: list[Dict[str, Any]] = []
    
    @abstractmethod
    async def answer_question(self, question: str, context: str) -> str:
        """Answer a question given some context"""
        pass
    
    def add_response(self, question: str, response: str):
        """Store the agent's response for later analysis"""
        self.responses.append({
            "question": question,
            "response": response
        })


class OpenAIAgent(BaseAgent):
    """Agent powered by OpenAI's GPT models"""
    
    def __init__(self, name: str = "GPT-4", model: str = "gpt-4"):
        super().__init__(name)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
    
    async def answer_question(self, question: str, context: str) -> str:
        """Use OpenAI to answer the question"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=500
            )
            answer = response.choices[0].message.content
            self.add_response(question, answer)
            return answer
        except Exception as e:
            return f"Error: {str(e)}"


class ClaudeAgent(BaseAgent):
    """Agent powered by Anthropic's Claude"""
    
    def __init__(self, name: str = "Claude", model: str = "claude-3-sonnet-20240229"):
        super().__init__(name)
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model
    
    async def answer_question(self, question: str, context: str) -> str:
        """Use Claude to answer the question"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.7,
                system=context,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            answer = response.content[0].text
            self.add_response(question, answer)
            return answer
        except Exception as e:
            return f"Error: {str(e)}"


# Factory function to create agents
def create_agent(agent_type: str, name: Optional[str] = None) -> BaseAgent:
    """Factory function to create different types of agents"""
    if agent_type.lower() == "openai":
        return OpenAIAgent(name or "GPT-4")
    elif agent_type.lower() == "claude":
        return ClaudeAgent(name or "Claude")
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
