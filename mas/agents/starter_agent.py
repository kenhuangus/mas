from ..agent import Agent, AgentType
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class StarterAgent(Agent):
    """Agent responsible for initializing workflows."""
    
    def __init__(self, agent_id: str, config: Dict, system_config: Dict, llm_config: Dict = None):
        super().__init__(agent_id, config, system_config, llm_config)
        self.initialization_type = config.get("config", {}).get("initialization_type", "standard")

    def process_message(self, message: Dict) -> Dict:
        """Initialize workflow with starting data.
        
        Args:
            message: The message containing initial data
            
        Returns:
            Dict containing initialized data and metadata
        """
        logger.info(f"Initializing workflow with type: {self.initialization_type}")
        
        payload = message.get("payload", {})
        data = payload.get("data", {})
        workflow_context = payload.get("workflow_context", {})
        
        # Add initialization metadata
        initialized_data = {
            "data": data,
            "metadata": {
                "initialization_type": self.initialization_type,
                "initialized_by": self.agent_id,
                "workflow_info": workflow_context
            }
        }
        
        return initialized_data
