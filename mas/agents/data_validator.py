"""Data Validator Agent for validating input data."""

from typing import Dict
import jsonschema
from ..agent import Agent

class DataValidator(Agent):
    """Agent that validates input data against a schema."""
    
    def process_message(self, message: Dict) -> Dict:
        """Validate the input data against the configured schema."""
        # Get validation config
        validation_config = self.config.get("input_validation", {})
        required_fields = validation_config.get("required_fields", [])
        schema = validation_config.get("schema")
        
        # Check required fields
        for field in required_fields:
            if field not in message:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate against schema if provided
        if schema:
            try:
                jsonschema.validate(instance=message, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                raise ValueError(f"Schema validation failed: {str(e)}")
        
        return message
