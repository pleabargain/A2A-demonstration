import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class Logger:
    def __init__(self, logs_dir: str = "logs"):
        """Initialize the logger with the directory to store logs."""
        self.logs_dir = logs_dir
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Define log file paths
        self.main_log_file = os.path.join(logs_dir, "main_log.json")
        self.routing_log_file = os.path.join(logs_dir, "routing_agent_log.json")
        self.animal_log_file = os.path.join(logs_dir, "animal_agent_log.json")
        self.plant_log_file = os.path.join(logs_dir, "plant_agent_log.json")
        
        # Initialize log files if they don't exist
        for log_file in [self.main_log_file, self.routing_log_file, self.animal_log_file, self.plant_log_file]:
            if not os.path.exists(log_file):
                with open(log_file, 'w') as f:
                    json.dump([], f)
    
    def _read_log(self, log_file: str) -> list:
        """Read the current log file."""
        try:
            with open(log_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_log(self, log_file: str, log_data: list) -> None:
        """Write to the log file."""
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def log_query(self, query: str, agent_type: str, model: str, 
                 classification: Optional[str] = None, response: Optional[str] = None,
                 processing_time: Optional[float] = None) -> None:
        """
        Log a query to both the main log and the agent-specific log.
        
        Args:
            query: The user's query
            agent_type: The type of agent (routing, animal, plant)
            model: The model used for processing
            classification: The classification result (for routing agent)
            response: The response provided to the user
            processing_time: The time taken to process the query in seconds
        """
        timestamp = datetime.now().isoformat()
        
        # Create the log entry
        log_entry = {
            "timestamp": timestamp,
            "query": query,
            "agent_type": agent_type,
            "model": model
        }
        
        # Add optional fields if provided
        if classification is not None:
            log_entry["classification"] = classification
        if response is not None:
            log_entry["response"] = response
        if processing_time is not None:
            log_entry["processing_time"] = processing_time
        
        # Log to main log file
        main_log = self._read_log(self.main_log_file)
        main_log.append(log_entry)
        self._write_log(self.main_log_file, main_log)
        
        # Log to agent-specific log file
        if agent_type == "routing":
            agent_log = self._read_log(self.routing_log_file)
            agent_log.append(log_entry)
            self._write_log(self.routing_log_file, agent_log)
        elif agent_type == "animal":
            agent_log = self._read_log(self.animal_log_file)
            agent_log.append(log_entry)
            self._write_log(self.animal_log_file, agent_log)
        elif agent_type == "plant":
            agent_log = self._read_log(self.plant_log_file)
            agent_log.append(log_entry)
            self._write_log(self.plant_log_file, agent_log)

# Create a singleton instance
logger = Logger()
