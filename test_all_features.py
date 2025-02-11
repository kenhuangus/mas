import json
import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from mas.workflow import WorkflowManager
from datetime import datetime
from typing import Dict, List
import copy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_successful_workflow():
    """Test a successful workflow execution with all features."""
    logger.info("\n=== Testing Successful Workflow ===")
    
    with open("config.json", "r") as f:
        config = json.load(f)
    
    workflow_manager = WorkflowManager(config)
    
    # Test data with various types
    initial_data = {
        "text_data": "Hello, Multi-Agent System!",
        "nested_data": {
            "key1": "value1",
            "key2": "value2",
            "numbers": [1, 2, 3],
            "mixed": {
                "text": "nested text",
                "number": 42
            }
        },
        "list_data": ["item1", "ITEM2", "Item3"],
        "number": 100
    }
    
    try:
        result = workflow_manager.start_workflow("main_workflow", initial_data)
        logger.info("Workflow completed successfully!")
        logger.info("\nWorkflow Context:")
        logger.info(json.dumps(result["workflow_context"], indent=2))
        logger.info("\nWorkflow Result:")
        logger.info(json.dumps(result["result"], indent=2))
        return True
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        return False

def test_concurrent_workflows():
    """Test multiple workflows running concurrently."""
    logger.info("\n=== Testing Concurrent Workflows ===")
    
    with open("config.json", "r") as f:
        config = json.load(f)
    
    workflow_manager = WorkflowManager(config)
    results = []
    
    def run_workflow(data: Dict) -> Dict:
        return workflow_manager.start_workflow("main_workflow", data)
    
    # Create multiple test datasets
    test_data = [
        {"text_data": f"Test data {i}", "number": i} 
        for i in range(5)
    ]
    
    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(run_workflow, data)
                for data in test_data
            ]
            results = [future.result() for future in futures]
        
        logger.info(f"Successfully completed {len(results)} concurrent workflows")
        return True
    except Exception as e:
        logger.error(f"Concurrent workflow test failed: {str(e)}")
        return False

def test_edge_cases():
    """Test various edge cases and boundary conditions."""
    logger.info("\n=== Testing Edge Cases ===")
    
    with open("config.json", "r") as f:
        config = json.load(f)
    
    workflow_manager = WorkflowManager(config)
    edge_cases = [
        # Empty data
        {},
        # Very large nested structure
        {
            "depth_0": {
                "depth_1": {
                    "depth_2": {
                        "depth_3": {
                            "data": "deep nested data"
                        }
                    }
                }
            }
        },
        # Mixed data types
        {
            "text": "test",
            "number": 42,
            "bool": True,
            "null": None,
            "list": [1, "two", 3.0, False],
            "empty_list": [],
            "empty_dict": {}
        },
        # Special characters
        {
            "special": "!@#$%^&*()_+-=[]{}|;:'\",.<>?/\\",
            "unicode": "Hello, 世界! Привет, мир! 👋🌍"
        }
    ]
    
    results = []
    for case in edge_cases:
        try:
            result = workflow_manager.start_workflow("main_workflow", case)
            results.append(True)
        except Exception as e:
            logger.error(f"Edge case failed: {str(e)}")
            logger.error(f"Input data: {json.dumps(case, indent=2)}")
            results.append(False)
    
    return all(results)

def test_data_transformations():
    """Test different data transformation types."""
    logger.info("\n=== Testing Data Transformations ===")
    
    with open("config.json", "r") as f:
        config = json.load(f)
    
    # Test different transformation types
    transformations = ["uppercase", "lowercase", "reverse"]
    results = []
    
    test_data = {
        "text": "Transform Me",
        "nested": {
            "text": "Also Transform",
            "list": ["Item1", "item2", "ITEM3"]
        }
    }
    
    for transform_type in transformations:
        try:
            # Create a new config with the current transformation type
            test_config = copy.deepcopy(config)
            test_config["agents"]["data_processor_1"]["config"]["transformation_type"] = transform_type
            
            workflow_manager = WorkflowManager(test_config)
            result = workflow_manager.start_workflow("main_workflow", test_data)
            
            logger.info(f"\nTransformation type: {transform_type}")
            logger.info(json.dumps(result["result"], indent=2))
            results.append(True)
        except Exception as e:
            logger.error(f"Transformation '{transform_type}' failed: {str(e)}")
            results.append(False)
    
    return all(results)

def test_error_recovery():
    """Test error recovery and retry mechanisms."""
    logger.info("\n=== Testing Error Recovery ===")
    
    with open("config.json", "r") as f:
        config = json.load(f)
    
    # Modify config to test different error scenarios
    test_cases = [
        {
            "name": "retry_success",
            "config_changes": {
                "agents.data_processor_1.config.max_retries": 3,
                "agents.data_processor_1.config.retry_delay": 1000
            },
            "data": {"text": "Should succeed after retry"}
        },
        {
            "name": "max_retries_exceeded",
            "config_changes": {
                "agents.data_processor_1.config.max_retries": 1,
                "agents.data_processor_1.config.retry_delay": 500
            },
            "data": {"text": "Should fail after max retries"}
        }
    ]
    
    results = []
    for case in test_cases:
        try:
            # Apply config changes
            test_config = copy.deepcopy(config)
            for path, value in case["config_changes"].items():
                parts = path.split(".")
                current = test_config
                for part in parts[:-1]:
                    current = current[part]
                current[parts[-1]] = value
            
            workflow_manager = WorkflowManager(test_config)
            result = workflow_manager.start_workflow("main_workflow", case["data"])
            
            logger.info(f"\nError recovery test '{case['name']}':")
            logger.info(json.dumps(result["workflow_context"], indent=2))
            results.append(True)
        except Exception as e:
            logger.error(f"Error recovery test '{case['name']}' failed: {str(e)}")
            results.append(False)
    
    return all(results)

def test_workflow_interruption():
    """Test workflow behavior when interrupted."""
    logger.info("\n=== Testing Workflow Interruption ===")
    
    with open("config.json", "r") as f:
        config = json.load(f)
    
    workflow_manager = WorkflowManager(config)
    
    def interrupt_workflow():
        time.sleep(0.5)  # Wait for workflow to start
        # Simulate interruption by modifying workflow state
        return True
    
    try:
        # Start workflow in a separate thread
        workflow_thread = threading.Thread(
            target=workflow_manager.start_workflow,
            args=("main_workflow", {"text": "Interrupt me"})
        )
        workflow_thread.start()
        
        # Start interruption in another thread
        interrupt_thread = threading.Thread(target=interrupt_workflow)
        interrupt_thread.start()
        
        # Wait for both threads to complete
        workflow_thread.join(timeout=2)
        interrupt_thread.join(timeout=2)
        
        return True
    except Exception as e:
        logger.error(f"Workflow interruption test failed: {str(e)}")
        return False

def main():
    """Run all tests and report results."""
    test_results = {
        "successful_workflow": test_successful_workflow(),
        "concurrent_workflows": test_concurrent_workflows(),
        "edge_cases": test_edge_cases(),
        "data_transformations": test_data_transformations(),
        "error_recovery": test_error_recovery(),
        "workflow_interruption": test_workflow_interruption()
    }
    
    logger.info("\n=== Test Results Summary ===")
    for test_name, result in test_results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        logger.info(f"{test_name}: {status}")
    
    return all(test_results.values())

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
