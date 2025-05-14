import asyncio
from agents.animal_agent import AnimalAgent
from agents.plant_agent import PlantAgent

async def test_animal_agent():
    agent = AnimalAgent()
    query = "Tell me about elephants and their habitat."
    print(f"Testing Animal Agent with query: '{query}'")
    response = await agent.answer_question(query)
    print(f"Response: {response}\n")

async def test_plant_agent():
    agent = PlantAgent()
    query = "What are the best conditions for growing roses?"
    print(f"Testing Plant Agent with query: '{query}'")
    response = await agent.answer_question(query)
    print(f"Response: {response}\n")

async def test_model_switching():
    agent = AnimalAgent()
    
    # Test with default model
    query = "What do lions eat?"
    print(f"Testing Animal Agent with default model and query: '{query}'")
    response = await agent.answer_question(query)
    print(f"Response with default model: {response}\n")
    
    # Test with a different model if available
    # Note: This will only work if you have another model installed in Ollama
    try:
        agent.set_model("gemma3:4b")  # Try with a different model if available
        print(f"Testing Animal Agent with gemma3:4b model and query: '{query}'")
        response = await agent.answer_question(query)
        print(f"Response with gemma3:4b model: {response}\n")
    except Exception as e:
        print(f"Error testing with alternative model: {str(e)}\n")

async def main():
    print("=== Testing A2A Agent System ===\n")
    
    try:
        await test_animal_agent()
        await test_plant_agent()
        await test_model_switching()
        print("All tests completed!")
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
