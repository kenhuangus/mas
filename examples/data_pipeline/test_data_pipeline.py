#!/usr/bin/env python
"""
Test the data pipeline example.
This example demonstrates a multi-stage data processing workflow with validation,
transformation, aggregation, and formatting.
"""

import json
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import mas
sys.path.append(str(Path(__file__).parent.parent.parent))

from mas.workflow import WorkflowManager

def test_data_pipeline():
    """Test the data pipeline workflow."""
    # Load configuration
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    # Create workflow manager
    workflow_manager = WorkflowManager(config)

    # Test data
    test_cases = [
        {
            "name": "Basic data processing",
            "input": {
                "data": [
                    {"name": "temperature", "value": 25.5},
                    {"name": "temperature", "value": 26.8},
                    {"name": "humidity", "value": 60.0},
                    {"name": "humidity", "value": 65.0}
                ],
                "schema_version": "1.0"
            },
            "expected_aggregates": {
                "temperature": 26.15,
                "humidity": 62.5
            }
        },
        {
            "name": "Single value per group",
            "input": {
                "data": [
                    {"name": "pressure", "value": 1013.25},
                    {"name": "temperature", "value": 22.0}
                ],
                "schema_version": "1.0"
            },
            "expected_aggregates": {
                "pressure": 1013.25,
                "temperature": 22.0
            }
        },
        {
            "name": "Mixed values",
            "input": {
                "data": [
                    {"name": "score", "value": 0.0},
                    {"name": "score", "value": 100.0},
                    {"name": "score", "value": 50.0}
                ],
                "schema_version": "1.0"
            },
            "expected_aggregates": {
                "score": 50.0
            }
        }
    ]

    # Run tests
    for test_case in test_cases:
        print(f"\nRunning test case: {test_case['name']}")
        
        try:
            # Start workflow
            result = workflow_manager.start_workflow(
                "data_pipeline",
                test_case["input"]
            )
            
            # Verify aggregates
            for name, expected_value in test_case["expected_aggregates"].items():
                actual_value = result["aggregates"][name]
                assert abs(actual_value - expected_value) < 0.01, \
                    f"For {name}, expected {expected_value}, but got {actual_value}"
            
            print(f"✅ {test_case['name']}: Passed")
            print(f"Input data points: {len(test_case['input']['data'])}")
            print(f"Aggregated results: {result['aggregates']}")
            
        except Exception as e:
            print(f"❌ {test_case['name']}: Failed")
            print(f"Error: {str(e)}")
            raise

def main():
    """Main entry point."""
    print("Testing Data Pipeline Example")
    print("============================")
    
    try:
        test_data_pipeline()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print("\n❌ Tests failed!")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
