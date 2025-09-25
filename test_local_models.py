#!/usr/bin/env python3
"""
Quick test to verify local models are working
"""

import requests
import json
from colorama import init, Fore

init(autoreset=True)


def test_model(model_name: str, prompt: str):
    """Test a specific model"""
    print(f"\n{Fore.YELLOW}Testing {model_name}...")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 100
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result["response"]
            print(f"{Fore.GREEN}✓ {model_name} is working!")
            print(f"{Fore.WHITE}Response: {answer[:100]}...")
            return True
        else:
            print(f"{Fore.RED}✗ {model_name} error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}✗ {model_name} error: {str(e)}")
        return False


def main():
    print(f"{Fore.CYAN}🧪 Testing Local Ollama Models\n")
    
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code != 200:
            print(f"{Fore.RED}Ollama is not responding!")
            print("Start Ollama with: ollama serve")
            return
    except:
        print(f"{Fore.RED}Cannot connect to Ollama at localhost:11434")
        print("Start Ollama with: ollama serve")
        return
    
    # Test prompt
    test_prompt = "What is 2+2? Give a short answer."
    
    # Test models
    models_ok = 0
    
    if test_model("deepseek-r1:latest", test_prompt):
        models_ok += 1
    
    if test_model("mistral:latest", test_prompt):
        models_ok += 1
    
    if test_model("qwen3:latest", test_prompt):
        models_ok += 1
    
    # Summary
    print(f"\n{Fore.CYAN}Summary:")
    if models_ok == 3:
        print(f"{Fore.GREEN}✅ All models are working!")
        print(f"\nYou can now run: python3 local_alignment_test.py")
    elif models_ok > 0:
        print(f"{Fore.YELLOW}⚠️  Only {models_ok}/3 models are working")
        print(f"Run: ./setup_local_models.sh to install missing models")
    else:
        print(f"{Fore.RED}❌ No models are working")
        print(f"Run: ./setup_local_models.sh to install models")


if __name__ == "__main__":
    main()
