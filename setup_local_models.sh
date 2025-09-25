#!/bin/bash

echo "🚀 Setting up Ollama models for local alignment testing"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed!"
    echo ""
    echo "Install Ollama:"
    echo "  macOS: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "  Or download from: https://ollama.com/download"
    exit 1
fi

echo "✅ Ollama is installed"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Starting Ollama service..."
    ollama serve &
    sleep 3
fi

echo ""
echo "📥 Pulling required models..."

# Pull Deepseek R1
echo ""
echo "1. Pulling Deepseek R1 (this may take a while)..."
ollama pull deepseek-r1:latest

# Pull Mistral
echo ""
echo "2. Pulling Mistral..."
ollama pull mistral:latest

echo ""
echo "📋 Installed models:"
ollama list

echo ""
echo "✅ Setup complete!"
echo ""
echo "You can now run the local alignment test:"
echo "  python3 local_alignment_test.py"
echo ""
echo "This will test Deepseek-R1 and Mistral on alignment scenarios."
