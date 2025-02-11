from mas.workflow import WorkflowManager
from mas.agent import Agent

# Test basic workflow creation
config = {
    "system_config": {
        "name": "Test System",
        "version": "1.0.0"
    },
    "agents": {
        "test_agent": {
            "id": "test_001",
            "type": "document_reader",
            "config": {
                "input_validation": {
                    "required_fields": ["text"]
                }
            }
        }
    },
    "workflow_definitions": {
        "test_workflow": {
            "stages": [
                {
                    "name": "test",
                    "agent": "test_agent"
                }
            ]
        }
    }
}

# Create workflow manager
workflow = WorkflowManager(config)
print("Package imported and workflow created successfully!")
