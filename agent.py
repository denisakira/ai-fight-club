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


class DeepseekAgent(BaseAgent):
    """Agent powered by Deepseek (Chinese LLM) - supports both API and local deployment"""
    
    def __init__(self, name: str = "Deepseek", model: str = "deepseek-chat", local: bool = False):
        super().__init__(name)
        
        if local:
            # For local deployment (e.g., Ollama, vLLM, etc.)
            base_url = os.getenv("DEEPSEEK_LOCAL_URL", "http://localhost:11434/v1")  # Default Ollama URL
            api_key = "not-needed"  # Local deployments typically don't need API keys
            self.name = f"{name}-Local"
            
            # For local models, temporarily clear proxy settings
            http_proxy = os.environ.pop('HTTP_PROXY', None)
            https_proxy = os.environ.pop('HTTPS_PROXY', None)
            
            try:
                self.client = OpenAI(
                    api_key=api_key,
                    base_url=base_url
                )
            finally:
                # Restore proxy settings
                if http_proxy:
                    os.environ['HTTP_PROXY'] = http_proxy
                if https_proxy:
                    os.environ['HTTPS_PROXY'] = https_proxy
        else:
            # For Deepseek API
            base_url = "https://api.deepseek.com/v1"
            api_key = os.getenv("DEEPSEEK_API_KEY")
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        self.model = model
        self.local = local
    
    async def answer_question(self, question: str, context: str) -> str:
        """Use Deepseek to answer the question"""
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


class LocalLLMAgent(BaseAgent):
    """Generic agent for local LLMs via Ollama/vLLM"""
    
    def __init__(self, name: str, model: str, base_url: str = None):
        super().__init__(name)
        self.base_url = base_url or os.getenv("LOCAL_LLM_URL", "http://localhost:11434/v1")
        # For local models, we need to ensure no proxy is used
        # Save and clear proxy environment variables
        http_proxy = os.environ.pop('HTTP_PROXY', None)
        https_proxy = os.environ.pop('HTTPS_PROXY', None)
        
        try:
            self.client = OpenAI(
                api_key="not-needed",
                base_url=self.base_url
            )
        finally:
            # Restore proxy settings
            if http_proxy:
                os.environ['HTTP_PROXY'] = http_proxy
            if https_proxy:
                os.environ['HTTPS_PROXY'] = https_proxy
                
        self.model = model
    
    async def answer_question(self, question: str, context: str) -> str:
        """Use local LLM to answer the question"""
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


# Factory function to create agents
def create_agent(agent_type: str, name: Optional[str] = None, **kwargs) -> BaseAgent:
    """Factory function to create different types of agents"""
    if agent_type.lower() == "openai":
        return OpenAIAgent(name or "GPT-4")
    elif agent_type.lower() == "claude":
        return ClaudeAgent(name or "Claude")
    elif agent_type.lower() == "deepseek":
        # Only pass model parameter if specified
        model = kwargs.get("model", "deepseek-chat")
        return DeepseekAgent(name or "Deepseek", model=model)
    elif agent_type.lower() == "deepseek-local":
        # Only pass model parameter if specified
        model = kwargs.get("model", "deepseek-coder:latest")
        return DeepseekAgent(name or "Deepseek", model=model, local=True)
    elif agent_type.lower() == "mistral-local":
        model = kwargs.get("model", "mistral:latest")
        base_url = kwargs.get("base_url", None)
        return LocalLLMAgent(name or "Mistral-Local", model, base_url)
    elif agent_type.lower() == "local":
        # Generic local LLM
        model = kwargs.get("model", "llama2:latest")
        base_url = kwargs.get("base_url", None)
        return LocalLLMAgent(name or "Local-LLM", model, base_url)
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
