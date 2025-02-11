from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional
import uuid
from datetime import datetime
import json
import logging
import jsonschema

logger = logging.getLogger(__name__)

class AgentType(Enum):
    STARTER = "starter"
    PROCESSOR = "processor"
    END = "end"
    ERROR_HANDLER = "error_handler"

class MessageStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"

class Agent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        """Initialize the agent.
        
        Args:
            agent_id: Unique identifier for this agent
            config: Agent-specific configuration
        """
        self.agent_id = agent_id
        self.config = config
    
    def create_message(self, payload: Dict, message_type: str = "agent_request") -> Dict:
        """Create a standardized message format.
        
        Args:
            payload: The message payload
            message_type: Type of message (agent_request or agent_response)
            
        Returns:
            Dict containing the formatted message
        """
        message = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "source_agent": self.agent_id,
            "message_type": message_type,
            "status": MessageStatus.PENDING.value,
            "payload": payload
        }
        
        # Validate message against schema if available
        try:
            if message_schemas := self.config.get("message_schemas", {}).get("standard_formats", {}):
                if schema := message_schemas.get(message_type):
                    jsonschema.validate(instance=message, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Message validation failed: {str(e)}")
            raise
            
        return message

    def receive_message(self, message: Dict) -> Dict:
        """Handle incoming messages and process them.
        
        Args:
            message: The incoming message to process
            
        Returns:
            Dict containing the response message
        """
        try:
            # Validate incoming message
            if message_schemas := self.config.get("message_schemas", {}).get("standard_formats", {}):
                if schema := message_schemas.get("agent_request"):
                    jsonschema.validate(instance=message, schema=schema)
            
            # Log message receipt
            logger.debug(f"Agent {self.agent_id} received message: {message.get('request_id')}")
            
            # Process the message
            response = self.process_message(message)
            
            # Create response message
            response_message = self.create_message(
                payload=response,
                message_type="agent_response"
            )
            response_message["status"] = MessageStatus.SUCCESS.value
            response_message["request_id"] = message.get("request_id")  # Maintain request chain
            
            return response_message
            
        except Exception as e:
            logger.error(f"Error processing message in agent {self.agent_id}: {str(e)}")
            error_response = self.create_message(
                payload={"error": str(e), "original_message": message},
                message_type="agent_response"
            )
            error_response["status"] = MessageStatus.ERROR.value
            error_response["request_id"] = message.get("request_id")
            return error_response

    @abstractmethod
    def process_message(self, message: Dict) -> Dict:
        """Process an incoming message.
        
        This method should be overridden by concrete agent implementations.
        
        Args:
            message: The message to process
            
        Returns:
            Dict containing the processed message
        """
        raise NotImplementedError("Concrete agents must implement process_message")
