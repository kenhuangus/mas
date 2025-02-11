from ..agent import Agent, AgentType
from typing import Dict
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class ErrorHandlerAgent(Agent):
    """Agent responsible for handling errors and implementing recovery strategies."""
    
    def __init__(self, agent_id: str, config: Dict, system_config: Dict, llm_config: Dict = None):
        super().__init__(agent_id, config, system_config, llm_config)
        self.max_retries = config.get("config", {}).get("max_retries", 3)
        self.retry_delay = config.get("config", {}).get("retry_delay", 1000)  # milliseconds

    def process_message(self, message: Dict) -> Dict:
        """Handle errors in the workflow.
        
        Args:
            message: The message containing error information
            
        Returns:
            Dict containing error handling result and metadata
        """
        payload = message.get("payload", {})
        error_info = payload.get("error", "Unknown error")
        original_message = payload.get("original_message", {})
        workflow_context = payload.get("workflow_context", {})
        
        # Log the error
        logger.error(f"Handling workflow error: {error_info}")
        
        # Get current retry count
        retry_count = workflow_context.get("retry_count", 0)
        
        if retry_count < self.max_retries:
            # Implement retry logic
            time.sleep(self.retry_delay / 1000)  # Convert to seconds
            retry_count += 1
            
            error_response = {
                "data": original_message.get("payload", {}).get("data", {}),
                "metadata": {
                    "error_handling": {
                        "error": error_info,
                        "handled_by": self.agent_id,
                        "retry_count": retry_count,
                        "recovery_action": "retry",
                        "handling_time": datetime.utcnow().isoformat()
                    }
                },
                "workflow_context": {
                    **workflow_context,
                    "retry_count": retry_count,
                    "last_error": error_info,
                    "recovery_status": "retrying"
                }
            }
        else:
            # Max retries exceeded
            error_response = {
                "data": {
                    "error": error_info,
                    "original_data": original_message.get("payload", {}).get("data", {})
                },
                "metadata": {
                    "error_handling": {
                        "error": error_info,
                        "handled_by": self.agent_id,
                        "retry_count": retry_count,
                        "recovery_action": "abort",
                        "handling_time": datetime.utcnow().isoformat()
                    }
                },
                "workflow_context": {
                    **workflow_context,
                    "retry_count": retry_count,
                    "last_error": error_info,
                    "recovery_status": "failed",
                    "status": "error"
                }
            }
        
        return error_response
