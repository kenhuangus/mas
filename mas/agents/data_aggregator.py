"""Data Aggregator Agent for computing statistics."""

from typing import Dict, List
import numpy as np
from collections import defaultdict
from ..agent import Agent

class DataAggregator(Agent):
    """Agent that performs data aggregation."""
    
    def process_message(self, message: Dict) -> Dict:
        """Aggregate data according to configuration."""
        aggregation_config = self.config.get("aggregation", {})
        method = aggregation_config.get("method", "mean")
        group_by = aggregation_config.get("group_by", "name")
        
        data = message.get("data", [])
        if not data:
            return {"aggregates": {}}
        
        # Group data
        groups = defaultdict(list)
        for item in data:
            group_key = item.get(group_by)
            if group_key is None:
                raise ValueError(f"Missing group key '{group_by}' in item")
            groups[group_key].append(item.get("value", 0))
        
        # Compute aggregates
        aggregates = {}
        for group_key, values in groups.items():
            if method == "mean":
                aggregates[group_key] = np.mean(values)
            elif method == "median":
                aggregates[group_key] = np.median(values)
            elif method == "sum":
                aggregates[group_key] = np.sum(values)
            else:
                raise ValueError(f"Unknown aggregation method: {method}")
        
        return {"aggregates": aggregates}
