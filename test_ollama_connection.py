import asyncio
import httpx
import json

async def test_ollama_connection():
    """Test if the Ollama API is accessible and working correctly"""
    print("Testing connection to Ollama API...")
    print("If you don't see any output after this, there might be a connection issue.")
    
    # Test 1: Check if the API is reachable
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            print("\nTest 1: Checking if Ollama API is reachable...")
            response = await client.get("http://localhost:11434/api/tags")
            
            if response.status_code == 200:
                print("✅ Success: Ollama API is reachable")
                models = response.json().get('models', [])
                print(f"Available models: {[model['name'] for model in models]}")
            else:
                print(f"❌ Error: Ollama API returned status code {response.status_code}")
                print(f"Response: {response.text}")
                return
    except httpx.ConnectError as e:
        print(f"❌ Error: Could not connect to Ollama API. Is Ollama running? Error: {str(e)}")
        return
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Test 2: Try to generate a simple response
    try:
        print("\nTest 2: Testing generation with a simple prompt...")
        
        # Get the first available model
        model_name = models[0]['name'] if models else "llama3.2:latest"
        print(f"Using model: {model_name}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model_name,
                    "prompt": "Say hello world",
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'response' in result:
                    print("✅ Success: Ollama API generated a response")
                    print(f"Response: {result['response']}")
                else:
                    print("❌ Error: 'response' field missing in API response")
                    print(f"Full response: {json.dumps(result, indent=2)}")
            else:
                print(f"❌ Error: Ollama API returned status code {response.status_code}")
                print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_ollama_connection())
