import asyncio
import os
import json
from agents.routing_agent import RoutingAgent
from agents.animal_agent import AnimalAgent
from agents.plant_agent import PlantAgent
from agents.logger import logger

async def test_logging():
    """Test the logging functionality for all agents."""
    print("=== Testing Logging System ===\n")
    
    # Create test instances of each agent
    routing_agent = RoutingAgent(model="llama3.2:latest")
    animal_agent = AnimalAgent(model="llama3.2:latest")
    plant_agent = PlantAgent(model="llama3.2:latest")
    
    # Test queries
    animal_query = "What do elephants eat in the wild?"
    plant_query = "How do I grow tomatoes in my garden?"
    
    print("1. Testing RoutingAgent logging...")
    classification = await routing_agent.classify_query(animal_query)
    print(f"  Classification result: {classification}")
    
    print("\n2. Testing AnimalAgent logging...")
    animal_response = await animal_agent.answer_question(animal_query)
    print(f"  Response received (truncated): {animal_response[:100]}...")
    
    print("\n3. Testing PlantAgent logging...")
    plant_response = await plant_agent.answer_question(plant_query)
    print(f"  Response received (truncated): {plant_response[:100]}...")
    
    # Verify log files were created
    log_files = [
        "logs/main_log.json",
        "logs/routing_agent_log.json",
        "logs/animal_agent_log.json",
        "logs/plant_agent_log.json"
    ]
    
    print("\n4. Verifying log files...")
    for log_file in log_files:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
                print(f"  ✅ {log_file}: {len(logs)} entries")
                
                # Print a sample log entry (first entry)
                if logs:
                    print(f"  Sample log entry:")
                    for key, value in logs[0].items():
                        if key == "response":
                            print(f"    {key}: {value[:50]}...")  # Truncate long responses
                        else:
                            print(f"    {key}: {value}")
        else:
            print(f"  ❌ {log_file} not found")

if __name__ == "__main__":
    asyncio.run(test_logging())
