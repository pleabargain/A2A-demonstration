import asyncio
from agents.animal_agent import AnimalAgent

async def test_animal_agent():
    agent = AnimalAgent(model="llama3.2:latest")
    
    # Test cases with direct keywords
    direct_keyword_tests = [
        "Tell me about animals in the savanna",
        "What are the most common mammals in North America?",
        "How do reptiles regulate their body temperature?",
        "What's the migration pattern of birds in winter?",
        "Are there any fish that can survive in extremely cold water?"
    ]
    
    # Test cases with related terms (not direct keywords)
    related_term_tests = [
        "How do predators hunt their prey?",
        "What kind of fur do polar bears have?",
        "How do wings help birds fly?",
        "Do all carnivores have sharp teeth?",
        "What's the purpose of a tail for most animals?"
    ]
    
    # Test cases that should NOT match (plant-related)
    negative_tests = [
        "How do I grow tomatoes in my garden?",
        "What's the best soil for roses?",
        "How much water do succulents need?",
        "When should I prune my fruit trees?",
        "What causes leaves to change color in autumn?"
    ]
    
    print("=== Testing AnimalAgent ===\n")
    
    print("1. Testing direct keyword matching:")
    for i, query in enumerate(direct_keyword_tests, 1):
        print(f"\nTest {i}: '{query}'")
        print(f"  Matches: {agent.matches_query(query)}")
        if agent.matches_query(query):
            print("  ✅ PASS: AnimalAgent correctly matched this query")
        else:
            print("  ❌ FAIL: AnimalAgent should have matched this query")
    
    print("\n2. Testing related term matching:")
    for i, query in enumerate(related_term_tests, 1):
        print(f"\nTest {i}: '{query}'")
        print(f"  Matches: {agent.matches_query(query)}")
        if agent.matches_query(query):
            print("  ✅ PASS: AnimalAgent correctly matched this query")
        else:
            print("  ❌ FAIL: AnimalAgent should have matched this query")
    
    print("\n3. Testing negative cases (should NOT match):")
    for i, query in enumerate(negative_tests, 1):
        print(f"\nTest {i}: '{query}'")
        print(f"  Matches: {agent.matches_query(query)}")
        if not agent.matches_query(query):
            print("  ✅ PASS: AnimalAgent correctly did not match this query")
        else:
            print("  ❌ FAIL: AnimalAgent should NOT have matched this query")
    
    # Test a full query with the LLM
    print("\n4. Testing full query with LLM:")
    test_query = "What do elephants eat in the wild?"
    print(f"\nQuery: '{test_query}'")
    if agent.matches_query(test_query):
        print("  ✅ Query matched to AnimalAgent")
        try:
            print("  Sending to LLM...")
            response = await agent.answer_question(test_query)
            print(f"\nResponse: {response}")
            print("\n  ✅ Successfully got response from LLM")
        except Exception as e:
            print(f"\n  ❌ Error getting response from LLM: {str(e)}")
    else:
        print("  ❌ Query was not matched to AnimalAgent")

if __name__ == "__main__":
    asyncio.run(test_animal_agent())
