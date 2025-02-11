# Configuration-Driven Multi-Agent System (MAS) Framework

[![CI/CD](https://github.com/kenhuangus/mas/actions/workflows/ci.yml/badge.svg)](https://github.com/kenhuangus/mas/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/distributedapps-mas.svg)](https://badge.fury.io/py/distributedapps-mas)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## What is This?

Traditional Multi-Agent Systems often require extensive coding to define agent behaviors, workflows, and interactions. This project takes a different approach: **What if you could build an entire multi-agent system just by writing a configuration JSON file?**

Instead of hard-coding agent logic, workflows, and system behaviors, this framework allows you to:
- Define agents and their capabilities through JSON configuration
- Specify workflow stages and transitions declaratively
- Configure error handling and recovery strategies
- Set up agent communication patterns
- Integrate with external services and APIs

All without writing a single line of agent implementation code.

## Quick Start

1. Install the package:
```bash
pip install distributedapps-mas
```

2. Run the example test case:
```bash
# Clone the repository
git clone https://github.com/kenhuangus/mas.git
cd mas

# Install in development mode
pip install -e .

# Run the document processing example
python examples/document_processing/test_document_processing.py
```

You should see output like this:
```
Testing Document Processing Example
==================================

Running test case: Basic document
 Basic document: Passed
Input: Hello, Multi-Agent System!
Output: HELLO, MULTI-AGENT SYSTEM!

Running test case: Empty document
 Empty document: Passed
Input: 
Output: 

Running test case: Special characters
 Special characters: Passed
Input: Hello! @#$%^&*()_+
Output: HELLO! @#$%^&*()_+

 All tests passed!
```

## Why Configuration-Driven MAS?

1. **Rapid Development**
   - Create new agents by adding JSON configuration
   - Modify workflows without changing code
   - Test different agent configurations quickly

2. **Reduced Complexity**
   - No need to implement agent communication logic
   - Declarative workflow definitions
   - Built-in error handling and retries

3. **Flexibility**
   - Change agent behaviors through configuration
   - Swap processing strategies without code changes
   - Update workflow paths dynamically

## Core Concepts

### 1. Agents
Agents are autonomous components that perform specific tasks:
- **Starter Agents**: Handle input and validation
- **Processor Agents**: Transform and process data
- **End Agents**: Format and output results
- **Error Handlers**: Manage failures and recovery

### 2. Workflows
Workflows define how agents interact:
- **Stages**: Sequential processing steps
- **Transitions**: Rules for moving between stages
- **Error Paths**: Alternative routes for handling failures

### 3. Configuration
Everything is defined in JSON:
- **Agent Definitions**: Capabilities and settings
- **Workflow Rules**: Processing stages and paths
- **System Settings**: Global configurations

## Show Me How

Here's a complete multi-agent system defined purely in configuration:

```json
{
    "system_config": {
        "name": "Document Processing MAS",
        "version": "1.0.0"
    },
    "agents": {
        "document_reader": {
            "id": "reader_001",
            "type": "document_reader",
            "config": {
                "input_validation": {
                    "required_fields": ["text", "metadata"]
                }
            }
        },
        "text_processor": {
            "id": "processor_001",
            "type": "document_processor",
            "config": {
                "transformation_type": "uppercase",
                "max_retries": 3
            }
        },
        "document_writer": {
            "id": "writer_001",
            "type": "document_writer",
            "config": {
                "output_format": "json"
            }
        }
    },
    "workflow_definitions": {
        "document_processing": {
            "stages": [
                {
                    "name": "read",
                    "agent": "document_reader",
                    "next_stage": "process",
                    "error_stage": "error_handling"
                },
                {
                    "name": "process",
                    "agent": "text_processor",
                    "next_stage": "write",
                    "error_stage": "error_handling"
                },
                {
                    "name": "write",
                    "agent": "document_writer"
                }
            ]
        }
    }
}
```

Run your multi-agent system with just a few lines of code:

```python
from mas.workflow import WorkflowManager
import json

# Load your configuration
with open("config.json", "r") as f:
    config = json.load(f)

# Create and run your multi-agent system
workflow_manager = WorkflowManager(config)
result = workflow_manager.start_workflow(
    "document_processing",
    {"text": "Process this document", "metadata": {"type": "article"}}
)
```

## Examples

The repository includes several examples to help you get started:

### 1. Document Processing Example
Located in `examples/document_processing/`, this example demonstrates:
- Input validation
- Text transformation
- Error handling
- Multi-stage workflow

To run the example:
```bash
python examples/document_processing/test_document_processing.py
```

The example includes:
- `config.json`: Complete system configuration
- `test_document_processing.py`: Test cases and runner
- `README.md`: Detailed documentation

### 2. Data Pipeline Example
Located in `examples/data_pipeline/`, this example shows how to build a data processing pipeline with:
- Schema validation
- Data normalization
- Statistical aggregation
- Formatted output

To run the example:
```bash
python examples/data_pipeline/test_data_pipeline.py
```

Example features:
- Multi-stage data processing
- Numeric data transformation
- Group-based aggregation
- Error handling with retries
- Pretty-printed JSON output

Configuration example:
```json
{
    "agents": {
        "data_validator": {
            "type": "data_validator",
            "config": {
                "input_validation": {
                    "required_fields": ["data", "schema_version"],
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "value": {"type": "number"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "data_transformer": {
            "type": "data_transformer",
            "config": {
                "transformation_type": "normalize",
                "normalization": {
                    "method": "min_max",
                    "target_range": [0, 1]
                }
            }
        }
    }
}
```

## Features

- **Configuration-First Design**
  - Define entire system behavior through JSON
  - No agent implementation code needed
  - Easy to modify and experiment

- **Pre-built Agent Types**
  - Document Processing Agents
  - Data Pipeline Agents
  - Error Handler Agents
  - Custom Agent Support

- **Declarative Workflows**
  - Define complex workflows in JSON
  - Automatic stage transitions
  - Built-in error handling paths

- **Built-in Transformations**
  - Text processing
  - Data validation
  - Numerical operations
  - Statistical aggregations
  - Custom transformations

## Best Practices

### 1. Configuration Design
- Use descriptive agent IDs
- Include version information
- Document configuration schema
- Validate configurations

### 2. Error Handling
- Define error stages
- Set retry policies
- Log failures
- Implement recovery strategies

### 3. Testing
- Create comprehensive test cases
- Test edge cases
- Validate configurations
- Monitor performance

### 4. Extensibility
- Create custom agents
- Add transformation types
- Implement new validators
- Extend base classes

## Installation

```bash
pip install distributedapps-mas
```

## Dependencies
- Python 3.8+
- numpy>=1.24.0
- jsonschema>=4.17.3
- typing-extensions>=4.8.0
- python-json-logger>=2.0.7

## Advanced Usage

### Adding Custom Transformations

```python
from mas.agent import Agent
from typing import Dict

class CustomProcessor(Agent):
    def process_message(self, message: Dict) -> Dict:
        # Your custom logic here
        return processed_data
```

Add it to your configuration:

```json
{
    "agents": {
        "custom_processor": {
            "type": "custom",
            "class": "path.to.CustomProcessor",
            "config": {
                "your_settings": "here"
            }
        }
    }
}
```

### Monitoring and Callbacks

```python
def on_stage_complete(stage_info):
    print(f"Stage {stage_info['name']} completed")

workflow_manager.start_workflow(
    "your_workflow",
    data,
    callbacks={
        "on_stage_complete": on_stage_complete,
        "on_error": handle_error
    }
)
```

### Dynamic Configuration

```python
# Update configuration at runtime
config["agents"]["processor"]["config"].update({
    "transformation_type": "new_type"
})

# Reload workflow
workflow_manager = WorkflowManager(config)
```

## Contributing

We welcome contributions! Whether it's:
- Adding new agent types
- Creating transformation plugins
- Improving documentation
- Reporting bugs

See our [Contributing Guidelines](CONTRIBUTING.md) for details.

## Documentation

Full documentation is available at [https://github.com/kenhuangus/mas/wiki](https://github.com/kenhuangus/mas/wiki)

## Support

- [Documentation](https://github.com/kenhuangus/mas/wiki)
- [Discord Community](https://discord.gg/distributedapps)
- [Issue Tracker](https://github.com/kenhuangus/mas/issues)
- [Email Support](mailto:support@distributedapps.ai)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Ken Huang**  
CEO, Distributedapps.ai  
[ken@distributedapps.ai](mailto:ken@distributedapps.ai)

---

Made with  by [Distributedapps.ai](https://distributedapps.ai)
