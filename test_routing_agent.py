import asyncio
from agents.routing_agent import RoutingAgent

async def test_routing_agent():
    agent = RoutingAgent(model="llama3.2:latest")
    
    # Test cases that should be classified as "animal"
    animal_tests = [
        "What do elephants eat in the wild?",
        "How do birds migrate in winter?",
        "Tell me about reptiles and their habitats",
        "What's the lifespan of an elephant?",
        "How do fish breathe underwater?",
        "What's the difference between mammals and reptiles?",
        "How do predators hunt their prey?",
        "What kind of fur do polar bears have?",
        "How do wings help birds fly?",
        "Do all carnivores have sharp teeth?"
    ]
    
    # Test cases that should be classified as "plant"
    plant_tests = [
        "How do I grow tomatoes in my garden?",
        "What's the best soil for roses?",
        "How much water do succulents need?",
        "When should I prune my fruit trees?",
        "What causes leaves to change color in autumn?",
        "How deep should I plant vegetable seeds?",
        "What causes root rot in houseplants?",
        "How does photosynthesis work?",
        "What's the best way to grow fruit in my garden?",
        "What are the best plants for indoor gardening?"
    ]
    
    # Test cases that are ambiguous or neither plant nor animal
    ambiguous_tests = [
        "What's the weather like today?",
        "How do I make a cake?",
        "What's the capital of France?",
        "How do bees help plants pollinate?",
        "What's the relationship between predators and their ecosystem?"
    ]
    
    print("=== Testing RoutingAgent ===\n")
    
    print("1. Testing animal queries:")
    for i, query in enumerate(animal_tests, 1):
        print(f"\nTest {i}: '{query}'")
        classification = await agent.classify_query(query)
        print(f"  Classification: {classification}")
        if classification == "animal":
            print("  ✅ PASS: Correctly classified as animal")
        else:
            print("  ❌ FAIL: Should have been classified as animal")
    
    print("\n2. Testing plant queries:")
    for i, query in enumerate(plant_tests, 1):
        print(f"\nTest {i}: '{query}'")
        classification = await agent.classify_query(query)
        print(f"  Classification: {classification}")
        if classification == "plant":
            print("  ✅ PASS: Correctly classified as plant")
        else:
            print("  ❌ FAIL: Should have been classified as plant")
    
    print("\n3. Testing ambiguous queries:")
    for i, query in enumerate(ambiguous_tests, 1):
        print(f"\nTest {i}: '{query}'")
        classification = await agent.classify_query(query)
        print(f"  Classification: {classification}")
        print("  ℹ️ INFO: Ambiguous query classification")

if __name__ == "__main__":
    asyncio.run(test_routing_agent())
