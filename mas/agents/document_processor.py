"""Document Processor Agent for text transformations."""

from typing import Dict
from ..agent import Agent

class DocumentProcessor(Agent):
    """Agent that performs text transformations."""
    
    def process_message(self, message: Dict) -> Dict:
        """Transform the document text based on configuration."""
        transformation_type = self.config.get("transformation_type", "uppercase")
        
        if "text" not in message:
            raise ValueError("Message must contain 'text' field")
        
        text = message["text"]
        
        if transformation_type == "uppercase":
            message["text"] = text.upper()
        elif transformation_type == "lowercase":
            message["text"] = text.lower()
        elif transformation_type == "reverse":
            message["text"] = text[::-1]
        else:
            raise ValueError(f"Unknown transformation type: {transformation_type}")
        
        return message
