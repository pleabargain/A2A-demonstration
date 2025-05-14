import asyncio
from agents.plant_agent import PlantAgent

async def test_plant_agent():
    agent = PlantAgent(model="llama3.2:latest")
    
    # Test cases with direct keywords
    direct_keyword_tests = [
        "What are the best plants for indoor gardening?",
        "How do I care for my flower garden?",
        "What's the tallest tree species in the world?",
        "How do I prune my shrubs in spring?",
        "Tell me about medicinal herbs and their uses"
    ]
    
    # Test cases with related terms (not direct keywords)
    related_term_tests = [
        "Why do leaves change color in autumn?",
        "How deep should I plant vegetable seeds?",
        "What causes root rot in houseplants?",
        "How does photosynthesis work?",
        "What's the best way to grow fruit in my garden?"
    ]
    
    # Test cases that should NOT match (animal-related)
    negative_tests = [
        "What do lions eat in the wild?",
        "How do birds migrate in winter?",
        "Tell me about reptiles and their habitats",
        "What's the lifespan of an elephant?",
        "How do fish breathe underwater?"
    ]
    
    print("=== Testing PlantAgent ===\n")
    
    print("1. Testing direct keyword matching:")
    for i, query in enumerate(direct_keyword_tests, 1):
        print(f"\nTest {i}: '{query}'")
        print(f"  Matches: {agent.matches_query(query)}")
        if agent.matches_query(query):
            print("  ✅ PASS: PlantAgent correctly matched this query")
        else:
            print("  ❌ FAIL: PlantAgent should have matched this query")
    
    print("\n2. Testing related term matching:")
    for i, query in enumerate(related_term_tests, 1):
        print(f"\nTest {i}: '{query}'")
        print(f"  Matches: {agent.matches_query(query)}")
        if agent.matches_query(query):
            print("  ✅ PASS: PlantAgent correctly matched this query")
        else:
            print("  ❌ FAIL: PlantAgent should have matched this query")
    
    print("\n3. Testing negative cases (should NOT match):")
    for i, query in enumerate(negative_tests, 1):
        print(f"\nTest {i}: '{query}'")
        print(f"  Matches: {agent.matches_query(query)}")
        if not agent.matches_query(query):
            print("  ✅ PASS: PlantAgent correctly did not match this query")
        else:
            print("  ❌ FAIL: PlantAgent should NOT have matched this query")
    
    # Test a full query with the LLM
    print("\n4. Testing full query with LLM:")
    test_query = "What is a leaf and how does it function?"
    print(f"\nQuery: '{test_query}'")
    if agent.matches_query(test_query):
        print("  ✅ Query matched to PlantAgent")
        try:
            print("  Sending to LLM...")
            response = await agent.answer_question(test_query)
            print(f"\nResponse: {response}")
            print("\n  ✅ Successfully got response from LLM")
        except Exception as e:
            print(f"\n  ❌ Error getting response from LLM: {str(e)}")
    else:
        print("  ❌ Query was not matched to PlantAgent")

if __name__ == "__main__":
    asyncio.run(test_plant_agent())
