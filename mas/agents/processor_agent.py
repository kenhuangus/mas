from ..agent import Agent, AgentType
from typing import Dict, Any, Union
import logging

logger = logging.getLogger(__name__)

class ProcessorAgent(Agent):
    """Agent responsible for processing data according to configured transformations."""
    
    def __init__(self, agent_id: str, config: Dict, system_config: Dict, llm_config: Dict = None):
        super().__init__(agent_id, config, system_config, llm_config)
        self.transformation_type = config.get("config", {}).get("transformation_type", "default")
        self.max_retries = config.get("config", {}).get("max_retries", 3)
        self.retry_delay = config.get("config", {}).get("retry_delay", 1000)
        
        # Validate transformation type
        self.valid_transformations = ["uppercase", "lowercase", "reverse", "default"]
        if self.transformation_type not in self.valid_transformations:
            raise ValueError(f"Invalid transformation type: {self.transformation_type}. Must be one of {self.valid_transformations}")

    def process_message(self, message: Dict) -> Dict:
        """Process data according to agent configuration.
        
        Args:
            message: The message containing data to process
            
        Returns:
            Dict containing the processed data and metadata
        """
        logger.info(f"Processing data with transformation: {self.transformation_type}")
        
        payload = message.get("payload", {})
        data = payload.get("data", {})
        workflow_context = payload.get("workflow_context", {})
        
        try:
            # Apply transformation based on configuration
            processed_data = self._transform_data(data)
            
            return {
                "data": {
                    "data": processed_data,
                    "metadata": {
                        "processing_info": {
                            "transformation_type": self.transformation_type,
                            "processed_by": self.agent_id
                        }
                    }
                },
                "workflow_context": workflow_context
            }
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise
    
    def _transform_data(self, data: Any) -> Any:
        """Transform data according to the configured transformation type.
        
        Args:
            data: Data to transform
            
        Returns:
            Transformed data
        """
        if isinstance(data, dict):
            return {
                key: self._transform_data(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self._transform_data(item) for item in data]
        elif isinstance(data, str):
            return self._apply_transformation(data)
        else:
            return data
    
    def _apply_transformation(self, text: str) -> str:
        """Apply the specified transformation to a string.
        
        Args:
            text: String to transform
            
        Returns:
            Transformed string
        """
        if self.transformation_type == "uppercase":
            return text.upper()
        elif self.transformation_type == "lowercase":
            return text.lower()
        elif self.transformation_type == "reverse":
            return text[::-1]
        else:  # default
            return text
