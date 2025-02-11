"""Data Transformer Agent for normalizing data."""

from typing import Dict, List
import numpy as np
from ..agent import Agent

class DataTransformer(Agent):
    """Agent that performs data transformations."""
    
    def process_message(self, message: Dict) -> Dict:
        """Transform the data according to configuration."""
        transformation_type = self.config.get("transformation_type")
        
        if transformation_type == "normalize":
            return self._normalize_data(message)
        else:
            raise ValueError(f"Unknown transformation type: {transformation_type}")
    
    def _normalize_data(self, message: Dict) -> Dict:
        """Normalize numeric data using the specified method."""
        normalization_config = self.config.get("normalization", {})
        method = normalization_config.get("method", "min_max")
        target_range = normalization_config.get("target_range", [0, 1])
        
        data = message.get("data", [])
        if not data:
            return message
        
        # Extract values
        values = [item["value"] for item in data]
        
        if method == "min_max":
            min_val = min(values)
            max_val = max(values)
            range_val = max_val - min_val
            
            if range_val == 0:
                normalized = [target_range[0]] * len(values)
            else:
                normalized = [
                    target_range[0] + (target_range[1] - target_range[0]) * 
                    (v - min_val) / range_val
                    for v in values
                ]
        
        elif method == "z_score":
            mean = np.mean(values)
            std = np.std(values)
            if std == 0:
                normalized = [0] * len(values)
            else:
                normalized = [(v - mean) / std for v in values]
        
        else:
            raise ValueError(f"Unknown normalization method: {method}")
        
        # Update data with normalized values
        for item, norm_value in zip(data, normalized):
            item["normalized_value"] = norm_value
        
        message["data"] = data
        return message
