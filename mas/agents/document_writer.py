"""Document Writer Agent for formatting output."""

from typing import Dict
import json
from ..agent import Agent

class DocumentWriter(Agent):
    """Agent that formats and writes documents."""
    
    def process_message(self, message: Dict) -> Dict:
        """Format the document according to configuration."""
        output_format = self.config.get("output_format", "json")
        
        if output_format == "json":
            # Already in JSON format, just pass through
            return message
        else:
            raise ValueError(f"Unknown output format: {output_format}")
