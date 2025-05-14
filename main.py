import asyncio
import httpx
import sys
import time
from typing import List, Dict, Any

from agents.animal_agent import AnimalAgent
from agents.plant_agent import PlantAgent
from agents.routing_agent import RoutingAgent
from agents.base_agent import BaseAgent
from agents.logger import logger

class AgentRouter:
    def __init__(self):
        self.animal_agent = AnimalAgent()
        self.plant_agent = PlantAgent()
        self.routing_agent = RoutingAgent()
        
        self.agent_models = {
            "AnimalAgent": "llama3.2:latest",
            "PlantAgent": "llama3.2:latest",
            "RoutingAgent": "llama3.2:latest"
        }

    async def dispatch(self, query: str) -> str:
        print("\nAnalyzing query to determine the appropriate agent...")
        start_time = time.time()
        
        # First, use the routing agent to classify the query
        print("Using RoutingAgent to classify the query...")
        
        # Set the model for the routing agent
        routing_model = self.agent_models.get("RoutingAgent", "llama3.2:latest")
        self.routing_agent.model = routing_model
        print(f"Using RoutingAgent with model: {routing_model}")
        
        # Get the classification from the routing agent
        classification = await self.routing_agent.classify_query(query)
        print(f"Query classification: {classification}")
        
        # Route the query to the appropriate agent based on the classification
        if classification == "animal":
            print("✅ Routing to AnimalAgent")
            agent = self.animal_agent
            agent_name = "AnimalAgent"
        elif classification == "plant":
            print("✅ Routing to PlantAgent")
            agent = self.plant_agent
            agent_name = "PlantAgent"
        else:
            # If classification is unknown or error, try the keyword matching as fallback
            print("⚠️ Classification uncertain, trying keyword matching as fallback...")
            
            # Try animal agent first
            if self.animal_agent.matches_query(query):
                print("✅ Keyword match: Routing to AnimalAgent")
                agent = self.animal_agent
                agent_name = "AnimalAgent"
            # Then try plant agent
            elif self.plant_agent.matches_query(query):
                print("✅ Keyword match: Routing to PlantAgent")
                agent = self.plant_agent
                agent_name = "PlantAgent"
            else:
                # If no agent can handle the query, return a fallback message
                print("❌ No agent found that can handle this query.")
                fallback_msg = "I'm sorry, I don't have information on that topic. Please ask about animals or plants.\nTry being more specific in your question."
                
                # Log the failed query
                processing_time = time.time() - start_time
                logger.log_query(
                    query=query,
                    agent_type="none",
                    model="none",
                    classification="unknown",
                    response=fallback_msg,
                    processing_time=processing_time
                )
                
                return fallback_msg
        
        # Set the model for the selected agent
        if hasattr(agent, 'set_model'):
            model = self.agent_models.get(agent_name, "llama3.2:latest")
            agent.set_model(model)
            print(f"Using {agent_name} with model: {model}")
        
        # Call the agent's answer_question method
        response = await agent.answer_question(query)
        
        # Calculate total processing time for the entire dispatch process
        total_processing_time = time.time() - start_time
        print(f"Total processing time: {total_processing_time:.2f} seconds")
        
        return response

    def set_agent_model(self, agent_name: str, model_name: str) -> str:
        if agent_name in self.agent_models:
            self.agent_models[agent_name] = model_name
            return f"Set {agent_name} to use model: {model_name}"
        else:
            return f"Unknown agent: {agent_name}. Available agents: {', '.join(self.agent_models.keys())}"

async def list_ollama_models() -> List[Dict[str, Any]]:
    """Get a list of available models from Ollama API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            result = response.json()
            return result.get('models', [])
    except Exception as e:
        print(f"Error fetching models: {str(e)}")
        return []

async def main():
    router = AgentRouter()
    
    while True:
        print("\nA2A Agent System")
        print("----------------")
        print("1. Ask a question")
        print("2. List available models")
        print("3. Set agent model")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            query = input("\nEnter your question about animals or plants: ")
            answer = await router.dispatch(query)
            print(f"\nAnswer: {answer}")
            
        elif choice == "2":
            print("\nFetching available models from Ollama...")
            models = await list_ollama_models()
            if models:
                print("\nAvailable models:")
                for model in models:
                    print(f"- {model['name']}")
            else:
                print("\nNo models found or Ollama server not running.")
                
        elif choice == "3":
            print("\nAvailable agents:")
            agent_names = list(router.agent_models.keys())
            for i, agent_name in enumerate(agent_names, 1):
                print(f"{i}. {agent_name} (current model: {router.agent_models[agent_name]})")
            
            try:
                agent_choice = int(input("\nSelect agent (enter number): "))
                if 1 <= agent_choice <= len(agent_names):
                    agent_name = agent_names[agent_choice - 1]
                    
                    # List available models for selection
                    print("\nAvailable models:")
                    models = await list_ollama_models()
                    model_names = [model['name'] for model in models]
                    for i, model_name in enumerate(model_names, 1):
                        print(f"{i}. {model_name}")
                    
                    model_choice = int(input("\nSelect model (enter number): "))
                    if 1 <= model_choice <= len(model_names):
                        model_name = model_names[model_choice - 1]
                        result = router.set_agent_model(agent_name, model_name)
                        print(f"\n{result}")
                    else:
                        print("\nInvalid model selection.")
                else:
                    print("\nInvalid agent selection.")
            except ValueError:
                print("\nPlease enter a valid number.")
            
        elif choice == "4":
            print("\nExiting A2A Agent System. Goodbye!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
