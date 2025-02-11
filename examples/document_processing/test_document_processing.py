#!/usr/bin/env python
"""
Test the document processing example from the README.
This example demonstrates how to create a multi-agent system using just configuration.
"""

import json
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import mas
sys.path.append(str(Path(__file__).parent.parent.parent))

from mas.workflow import WorkflowManager

def test_document_processing():
    """Test the document processing workflow."""
    # Load configuration
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    # Create workflow manager
    workflow_manager = WorkflowManager(config)

    # Test data
    test_cases = [
        {
            "name": "Basic document",
            "input": {
                "text": "Hello, Multi-Agent System!",
                "metadata": {"type": "greeting"}
            },
            "expected_text": "HELLO, MULTI-AGENT SYSTEM!"
        },
        {
            "name": "Empty document",
            "input": {
                "text": "",
                "metadata": {"type": "empty"}
            },
            "expected_text": ""
        },
        {
            "name": "Special characters",
            "input": {
                "text": "Hello! @#$%^&*()_+",
                "metadata": {"type": "special"}
            },
            "expected_text": "HELLO! @#$%^&*()_+"
        }
    ]

    # Run tests
    for test_case in test_cases:
        print(f"\nRunning test case: {test_case['name']}")
        
        try:
            # Start workflow
            result = workflow_manager.start_workflow(
                "document_processing",
                test_case["input"]
            )
            
            # Get the processed text from the result
            processed_text = result["text"]
            
            # Verify result
            assert processed_text == test_case["expected_text"], \
                f"Expected '{test_case['expected_text']}', but got '{processed_text}'"
            
            print(f" {test_case['name']}: Passed")
            print(f"Input: {test_case['input']['text']}")
            print(f"Output: {processed_text}")
            
        except Exception as e:
            print(f" {test_case['name']}: Failed")
            print(f"Error: {str(e)}")
            raise

def main():
    """Main entry point."""
    print("Testing Document Processing Example")
    print("==================================")
    
    try:
        test_document_processing()
        print("\n All tests passed!")
    except Exception as e:
        print("\n Tests failed!")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
