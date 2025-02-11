from ..agent import Agent, AgentType
from typing import Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EndAgent(Agent):
    """Agent responsible for finalizing workflow execution and preparing final output."""
    
    def __init__(self, agent_id: str, config: Dict, system_config: Dict, llm_config: Dict = None):
        super().__init__(agent_id, config, system_config, llm_config)

    def process_message(self, message: Dict) -> Dict:
        """Finalize workflow and prepare final output.
        
        Args:
            message: The message containing processed data
            
        Returns:
            Dict containing the final workflow output and metadata
        """
        logger.info(f"Finalizing workflow execution")
        
        payload = message.get("payload", {})
        data = payload.get("data", {})
        workflow_context = payload.get("workflow_context", {})
        
        # Prepare final output with complete execution metadata
        final_output = {
            "data": data.get("data", {}),
            "metadata": {
                **data.get("metadata", {}),
                "completion_info": {
                    "completed_by": self.agent_id,
                    "completion_time": datetime.utcnow().isoformat()
                }
            },
            "workflow_context": {
                **workflow_context,
                "status": "completed",
                "end_time": datetime.utcnow().isoformat()
            }
        }
        
        return final_output
