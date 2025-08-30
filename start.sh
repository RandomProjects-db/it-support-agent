#!/bin/bash

# IT Support Agent Startup Script
echo "🚀 Starting IT Support Agent..."

# Set the Groq API key (replace with your actual key)
export GROQ_API_KEY="your-groq-api-key-here"

# Start the Python API server
echo "📡 Starting API server on http://localhost:8000"
python3 main.py
