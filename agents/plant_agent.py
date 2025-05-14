import httpx
import asyncio
import time

from .base_agent import BaseAgent
from .logger import logger

class PlantAgent(BaseAgent):
    def __init__(self, model="llama3.2:latest"):
        super().__init__(
            domain_keywords=['plant', 'flower', 'tree', 'shrub', 'botany', 'herb', 
                            'flora', 'vegetation', 'bush', 'seeds', 'leaf', 'leaves',
                            'root', 'stem', 'photosynthesis', 'garden', 'grow', 
                            'fruit', 'vegetable', 'rose', 'tulip', 'daisy', 'sunflower',
                            'oak', 'pine', 'maple', 'cactus', 'succulent', 'grass',
                            'moss', 'fern', 'algae', 'pollen', 'blossom', 'bloom']
        )
        self.llm_url = "http://localhost:11434/api/generate"
        self.system_prompt = "You are a botany expert specializing in plants. Answer this question:"
        self.model = model

    def set_model(self, model_name: str):
        """Set the model to use for this agent"""
        self.model = model_name

    async def answer_question(self, query: str) -> str:
        full_prompt = f"{self.system_prompt} {query}"
        start_time = time.time()
        
        try:
            print(f"Sending request to Ollama API with model: {self.model}")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.llm_url,
                    json={
                        "model": self.model,
                        "prompt": full_prompt,
                        "stream": False
                    }
                )
                
                if response.status_code != 200:
                    error_msg = f"PlantAgent error: API returned status code {response.status_code}. Response: {response.text}"
                    # Log the error
                    processing_time = time.time() - start_time
                    logger.log_query(
                        query=query,
                        agent_type="plant",
                        model=self.model,
                        response=error_msg,
                        processing_time=processing_time
                    )
                    return error_msg
                
                try:
                    result = response.json()
                    if 'response' not in result:
                        error_msg = f"PlantAgent error: 'response' field missing in API response. Full response: {result}"
                        # Log the error
                        processing_time = time.time() - start_time
                        logger.log_query(
                            query=query,
                            agent_type="plant",
                            model=self.model,
                            response=error_msg,
                            processing_time=processing_time
                        )
                        return error_msg
                    
                    # Log the successful response
                    response_text = result['response'].strip()
                    processing_time = time.time() - start_time
                    logger.log_query(
                        query=query,
                        agent_type="plant",
                        model=self.model,
                        response=response_text,
                        processing_time=processing_time
                    )
                    return response_text
                    
                except Exception as json_error:
                    error_msg = f"PlantAgent error parsing JSON: {str(json_error)}. Response text: {response.text}"
                    # Log the error
                    processing_time = time.time() - start_time
                    logger.log_query(
                        query=query,
                        agent_type="plant",
                        model=self.model,
                        response=error_msg,
                        processing_time=processing_time
                    )
                    return error_msg
                
        except httpx.ConnectError as e:
            error_msg = f"PlantAgent error: Could not connect to Ollama API at {self.llm_url}. Is Ollama running? Error: {str(e)}"
            # Log the error
            processing_time = time.time() - start_time
            logger.log_query(
                query=query,
                agent_type="plant",
                model=self.model,
                response=error_msg,
                processing_time=processing_time
            )
            return error_msg
        except httpx.TimeoutException as e:
            error_msg = f"PlantAgent error: Request to Ollama API timed out. Error: {str(e)}"
            # Log the error
            processing_time = time.time() - start_time
            logger.log_query(
                query=query,
                agent_type="plant",
                model=self.model,
                response=error_msg,
                processing_time=processing_time
            )
            return error_msg
        except Exception as e:
            error_msg = f"PlantAgent error: {str(e)}"
            # Log the error
            processing_time = time.time() - start_time
            logger.log_query(
                query=query,
                agent_type="plant",
                model=self.model,
                response=error_msg,
                processing_time=processing_time
            )
            return error_msg
