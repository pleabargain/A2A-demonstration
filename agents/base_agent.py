class BaseAgent:
    def __init__(self, domain_keywords):
        self.domain_keywords = domain_keywords

    def matches_query(self, query: str) -> bool:
        """
        Check if the query matches any of the agent's domain keywords.
        This method is more flexible and will match partial words as well.
        """
        query_lower = query.lower()
        
        # Direct keyword matching
        for keyword in self.domain_keywords:
            if keyword.lower() in query_lower:
                return True
        
        # Check for related terms that might not be in the keywords list
        # For example, "leaf" is related to "plant" but might not be in the keywords
        if self.__class__.__name__ == "PlantAgent":
            plant_related_terms = ["leaf", "leaves", "root", "stem", "photosynthesis", 
                                  "garden", "grow", "seed", "fruit", "vegetable"]
            for term in plant_related_terms:
                if term.lower() in query_lower:
                    return True
                    
        elif self.__class__.__name__ == "AnimalAgent":
            animal_related_terms = ["fur", "feather", "wing", "paw", "tail", 
                                   "predator", "prey", "hunt", "carnivore", "herbivore"]
            for term in animal_related_terms:
                if term.lower() in query_lower:
                    return True
        
        return False

    async def answer_question(self, query: str) -> str:
        raise NotImplementedError("Subclasses must implement this method.")
