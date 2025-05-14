# A2A Agent System

This project implements a Python tool using the A2A (Agent-to-Agent) protocol where two specialized agents communicate and provide domain-specific answers.


I tried to implement an A2A using Ollama as my local engine. It appears to work.

## System Overview

The system consists of two specialized agents:

1. **Animal Agent**: Answers queries about animals (behavior, habitat, species information)
2. **Plant Agent**: Answers queries about plants (growth conditions, classification, botanical info)

When a user asks a question, the system routes the query to the appropriate agent based on keywords in the query.

## Features

- Modular agent structure with a common interface
- Automatic query routing based on domain keywords
- Integration with Ollama for LLM-powered responses
- Ability to list available Ollama models
- Ability to assign different models to each agent

## Requirements

- Python 3.7+
- httpx (for async HTTP requests)
- asyncio
- Ollama running locally on port 11434

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure Ollama is running locally on port 11434

## Usage

Run the main script:

```
python main.py
```

The interactive menu provides the following options:

1. **Ask a question**: Enter a query about animals or plants
2. **List available models**: Show all models available in your local Ollama instance
3. **Set agent model**: Assign a specific model to an agent
4. **Exit**: Quit the application

## How It Works

1. The user enters a query
2. The system analyzes the query for domain-specific keywords
3. The query is routed to the appropriate agent (Animal or Plant)
4. The agent uses Ollama to generate a response based on its domain expertise
5. The response is returned to the user

## A2A Protocol Implementation

The A2A protocol is implemented through:

1. A common interface (BaseAgent) that all agents implement
2. A router (AgentRouter) that analyzes queries and routes them to the appropriate agent
3. Agent-specific knowledge and processing through specialized system prompts

## Extending the System

To add a new agent:

1. Create a new class that inherits from BaseAgent
2. Define domain-specific keywords
3. Implement the answer_question method
4. Add the new agent to the AgentRouter's agents list
