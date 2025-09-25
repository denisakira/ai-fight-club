"""
Simple agent implementation for local Ollama models only
"""

import os
from typing import Optional, Dict, Any
import requests
import json
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


class OllamaAgent(BaseAgent):
    """Agent for local Ollama models"""
    
    def __init__(self, name: str, model: str):
        super().__init__(name)
        self.model = model
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    
    async def answer_question(self, question: str, context: str) -> str:
        """Use Ollama to answer the question"""
        try:
            # Prepare the prompt
            prompt = f"{context}\n\n{question}"
            
            # Call Ollama API directly
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 500
                    }
                }
            )
            
            if response.status_code == 200:
                answer = response.json()["response"]
                self.add_response(question, answer)
                return answer
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"


# Factory function to create agents
def create_local_agent(model_name: str, agent_name: Optional[str] = None) -> BaseAgent:
    """Create a local Ollama agent"""
    if model_name == "deepseek-r1":
        return OllamaAgent(agent_name or "Deepseek-R1", "deepseek-r1:latest")
    elif model_name == "mistral":
        return OllamaAgent(agent_name or "Mistral", "mistral:latest")
    else:
        return OllamaAgent(agent_name or model_name, f"{model_name}:latest")
