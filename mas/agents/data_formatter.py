"""Data Formatter Agent for formatting output."""

from typing import Dict
import json
from datetime import datetime
from ..agent import Agent

class DataFormatter(Agent):
    """Agent that formats data for output."""
    
    def process_message(self, message: Dict) -> Dict:
        """Format the data according to configuration."""
        output_format = self.config.get("output_format", "json")
        include_metadata = self.config.get("include_metadata", True)
        pretty_print = self.config.get("pretty_print", True)
        
        if output_format != "json":
            raise ValueError(f"Unsupported output format: {output_format}")
        
        # Prepare output
        output = {}
        
        # Add data
        output.update(message)
        
        # Add metadata if requested
        if include_metadata:
            output["metadata"] = {
                "timestamp": datetime.utcnow().isoformat(),
                "agent_id": self.agent_id,
                "format_version": "1.0"
            }
        
        # Format as JSON
        if pretty_print:
            return json.loads(json.dumps(output, indent=2))
        else:
            return output
