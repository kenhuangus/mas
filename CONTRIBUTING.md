# Contributing to MAS Framework

Thank you for your interest in contributing to the Multi-Agent System Framework! This document provides guidelines and instructions for contributing.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Making Changes](#making-changes)
4. [Testing](#testing)
5. [Submitting Changes](#submitting-changes)
6. [Code Style](#code-style)
7. [Documentation](#documentation)

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mas.git
   cd mas
   ```

3. Set up your development environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

## Development Setup

### Required Dependencies
- Python 3.8+
- numpy>=1.24.0
- jsonschema>=4.17.3
- typing-extensions>=4.8.0
- python-json-logger>=2.0.7
- pydantic>=2.0.0

### Development Tools
- pytest for testing
- black for code formatting
- mypy for type checking
- flake8 for linting

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Making Changes

### Adding New Agents

1. Create a new agent class in `mas/agents/`:
   ```python
   from ..agent import Agent
   from typing import Dict

   class NewAgent(Agent):
       def process_message(self, message: Dict) -> Dict:
           # Implement your agent logic
           return processed_message
   ```

2. Register the agent in `mas/agent_registry.py`:
   ```python
   from .agents.new_agent import NewAgent

   AGENT_REGISTRY["new_agent"] = NewAgent
   ```

### Adding Transformations

1. Add your transformation to the appropriate agent:
   ```python
   def _transform_data(self, data: Dict) -> Dict:
       method = self.config.get("method")
       if method == "your_method":
           return your_transformation(data)
   ```

2. Update configuration schema:
   ```json
   {
       "transformation": {
           "method": "your_method",
           "parameters": {}
       }
   }
   ```

### Adding Examples

1. Create a new directory in `examples/`
2. Include:
   - `config.json`: Configuration file
   - `test_example.py`: Test cases
   - `README.md`: Documentation

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest examples/your_example/test_example.py

# Run with coverage
pytest --cov=mas tests/
```

### Writing Tests

1. Create test cases:
   ```python
   def test_your_feature():
       # Arrange
       config = {...}
       workflow = WorkflowManager(config)
       
       # Act
       result = workflow.start_workflow(...)
       
       # Assert
       assert result["expected_key"] == expected_value
   ```

2. Test error cases:
   ```python
   def test_error_handling():
       with pytest.raises(ValueError):
           # Test code that should raise error
   ```

## Submitting Changes

1. Create a branch:
   ```bash
   git checkout -b feature/your-feature
   ```

2. Make your changes:
   - Write clear commit messages
   - Keep commits focused
   - Reference issues

3. Push changes:
   ```bash
   git push origin feature/your-feature
   ```

4. Create a Pull Request:
   - Describe your changes
   - Link related issues
   - Update documentation

## Code Style

### Python Style Guide
- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use docstrings (Google style)

### Example
```python
from typing import Dict, Optional

def process_data(data: Dict, options: Optional[Dict] = None) -> Dict:
    """Process the input data with given options.
    
    Args:
        data: Input data to process
        options: Optional processing parameters
    
    Returns:
        Processed data dictionary
    
    Raises:
        ValueError: If data is invalid
    """
    if not data:
        raise ValueError("Empty data")
    
    return processed_data
```

### Configuration Style
- Use descriptive keys
- Include version information
- Document schema
- Validate against schema

## Documentation

### Docstrings
```python
class YourAgent(Agent):
    """Agent that performs specific task.
    
    Attributes:
        config: Agent configuration
        agent_id: Unique identifier
    """
    
    def process_message(self, message: Dict) -> Dict:
        """Process incoming message.
        
        Args:
            message: Input message
            
        Returns:
            Processed message
        """
```

### README Files
- Include purpose
- Show examples
- List dependencies
- Provide usage instructions

### Configuration Documentation
```json
{
    "agent_type": "your_agent",
    "config": {
        // Required: Method to use
        "method": "example",
        
        // Optional: Additional parameters
        "parameters": {
            "param1": "value1"
        }
    }
}
```

## Questions?

- Open an issue at [https://github.com/kenhuangus/mas/issues](https://github.com/kenhuangus/mas/issues)
- Join our Discord
- Email support@distributedapps.ai

Thank you for contributing to MAS Framework! 🎉
