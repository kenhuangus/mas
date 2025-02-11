"""Document Reader Agent for validating input documents."""

from typing import Dict
from ..agent import Agent

class DocumentReader(Agent):
    """Agent that validates input documents."""
    
    def process_message(self, message: Dict) -> Dict:
        """Validate and process the input document."""
        # Get required fields from config
        required_fields = self.config.get("input_validation", {}).get("required_fields", [])
        
        # Validate required fields
        for field in required_fields:
            if field not in message:
                raise ValueError(f"Missing required field: {field}")
        
        # Return validated document
        return message
