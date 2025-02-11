import json
import logging
from mas.workflow import WorkflowManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Load configuration
    with open("config.json", "r") as f:
        config = json.load(f)

    # Create workflow manager
    workflow_manager = WorkflowManager(config)

    # Test data
    initial_data = {
        "message": "Hello, Multi-Agent System!",
        "data": {
            "key1": "value1",
            "key2": "value2"
        }
    }

    try:
        # Run the workflow
        logger.info("Starting workflow execution...")
        result = workflow_manager.start_workflow("main_workflow", initial_data)
        
        logger.info("Workflow completed successfully!")
        logger.info("Workflow Context:")
        logger.info(json.dumps(result["workflow_context"], indent=2))
        logger.info("\nWorkflow Result:")
        logger.info(json.dumps(result["result"], indent=2))
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
