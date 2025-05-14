import httpx
import asyncio
import time
from .base_agent import BaseAgent
from .logger import logger

class RoutingAgent(BaseAgent):
    def __init__(self, model="llama3.2:latest"):
        super().__init__(domain_keywords=[])
        self.llm_url = "http://localhost:11434/api/generate"
        self.system_prompt = """You are a query classifier that determines if a question is about plants, animals, or neither.

RULES:
1. If the query mentions any animal (mammals, reptiles, birds, fish, etc.) or animal-related terms (fur, feathers, wings, etc.), classify it as 'animal'.
2. If the query mentions any plant (trees, flowers, vegetables, etc.) or plant-related terms (leaves, roots, photosynthesis, etc.), classify it as 'plant'.
3. If the query is ambiguous or about neither plants nor animals, classify it as 'unknown'.
4. IMPORTANT: Only respond with one word: 'animal', 'plant', or 'unknown'. No other text.

Classify this query:"""
        self.model = model

    async def classify_query(self, query: str) -> str:
        full_prompt = f"{self.system_prompt} {query}"
        start_time = time.time()
        
        try:
            print(f"Sending classification request to Ollama API with model: {self.model}")
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
                    error_msg = f"RoutingAgent error: API returned status code {response.status_code}"
                    # Log the error
                    processing_time = time.time() - start_time
                    logger.log_query(
                        query=query,
                        agent_type="routing",
                        model=self.model,
                        classification="error",
                        response=error_msg,
                        processing_time=processing_time
                    )
                    return error_msg
                
                try:
                    result = response.json()
                    if 'response' not in result:
                        error_msg = f"RoutingAgent error: 'response' field missing in API response"
                        # Log the error
                        processing_time = time.time() - start_time
                        logger.log_query(
                            query=query,
                            agent_type="routing",
                            model=self.model,
                            classification="error",
                            response=error_msg,
                            processing_time=processing_time
                        )
                        return error_msg
                    
                    classification = result['response'].strip().lower()
                    if classification in ['plant', 'animal', 'unknown']:
                        # Log the successful classification
                        processing_time = time.time() - start_time
                        logger.log_query(
                            query=query,
                            agent_type="routing",
                            model=self.model,
                            classification=classification,
                            response=classification,
                            processing_time=processing_time
                        )
                        return classification
                    
                    # If classification is not one of the expected values, default to unknown
                    processing_time = time.time() - start_time
                    logger.log_query(
                        query=query,
                        agent_type="routing",
                        model=self.model,
                        classification="unknown",
                        response=f"Unexpected classification: {classification}, defaulting to unknown",
                        processing_time=processing_time
                    )
                    return 'unknown'
                except Exception as json_error:
                    error_msg = f"RoutingAgent error parsing JSON: {str(json_error)}"
                    # Log the error
                    processing_time = time.time() - start_time
                    logger.log_query(
                        query=query,
                        agent_type="routing",
                        model=self.model,
                        classification="error",
                        response=error_msg,
                        processing_time=processing_time
                    )
                    return error_msg
                
        except httpx.ConnectError as e:
            error_msg = f"RoutingAgent error: Could not connect to Ollama API. Error: {str(e)}"
            # Log the error
            processing_time = time.time() - start_time
            logger.log_query(
                query=query,
                agent_type="routing",
                model=self.model,
                classification="error",
                response=error_msg,
                processing_time=processing_time
            )
            return error_msg
        except httpx.TimeoutException as e:
            error_msg = f"RoutingAgent error: Request timed out. Error: {str(e)}"
            # Log the error
            processing_time = time.time() - start_time
            logger.log_query(
                query=query,
                agent_type="routing",
                model=self.model,
                classification="error",
                response=error_msg,
                processing_time=processing_time
            )
            return error_msg
        except Exception as e:
            error_msg = f"RoutingAgent error: {str(e)}"
            # Log the error
            processing_time = time.time() - start_time
            logger.log_query(
                query=query,
                agent_type="routing",
                model=self.model,
                classification="error",
                response=error_msg,
                processing_time=processing_time
            )
            return error_msg
