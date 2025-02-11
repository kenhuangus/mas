"""Workflow management for the Multi-Agent System."""

from typing import Dict, Any, Optional
import uuid
from datetime import datetime
from .agent import Agent
from .agent_registry import AGENT_REGISTRY

class WorkflowManager:
    """Manages workflows in the Multi-Agent System."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the workflow manager with configuration."""
        self.config = config
        self.agents = {}
        self.workflow_definitions = config.get("workflow_definitions", {})
        
        # Initialize agents from config
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize agents based on configuration."""
        agent_configs = self.config.get("agents", {})
        
        for agent_id, agent_config in agent_configs.items():
            agent_type = agent_config.get("type")
            if agent_type not in AGENT_REGISTRY:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            # Create agent instance
            agent_class = AGENT_REGISTRY[agent_type]
            agent = agent_class(
                agent_id=agent_config.get("id", str(uuid.uuid4())),
                config=agent_config.get("config", {})
            )
            
            self.agents[agent_id] = agent
    
    def start_workflow(self, workflow_name: str, initial_payload: Optional[Dict] = None) -> Dict:
        """Start a workflow with the given name and initial payload."""
        if workflow_name not in self.workflow_definitions:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        workflow = self.workflow_definitions[workflow_name]
        stages = workflow.get("stages", [])
        
        if not stages:
            raise ValueError(f"Workflow {workflow_name} has no stages")
        
        # Initialize workflow context
        context = {
            "workflow_id": str(uuid.uuid4()),
            "workflow_name": workflow_name,
            "start_time": datetime.utcnow().isoformat(),
            "current_stage": stages[0]["name"]
        }
        
        # Process each stage
        current_payload = initial_payload or {}
        
        for stage in stages:
            agent_id = stage["agent"]
            if agent_id not in self.agents:
                raise ValueError(f"Unknown agent: {agent_id}")
            
            agent = self.agents[agent_id]
            try:
                # Update context
                context["current_stage"] = stage["name"]
                context["current_agent"] = agent_id
                
                # Process message
                current_payload = agent.process_message(current_payload)
                
            except Exception as e:
                # Handle error stage if defined
                error_stage = stage.get("error_stage")
                if error_stage and error_stage in self.agents:
                    error_agent = self.agents[error_stage]
                    context["error"] = str(e)
                    current_payload = error_agent.process_message(current_payload)
                else:
                    raise
        
        # Update completion status
        context["end_time"] = datetime.utcnow().isoformat()
        context["status"] = "completed"
        
        # Return the processed payload directly
        return current_payload
