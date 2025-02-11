# Document Processing Example

This example demonstrates how to create a multi-agent system using just configuration, as shown in the main README.

## Structure

- `config.json`: Configuration file defining the multi-agent system
- `test_document_processing.py`: Test script that runs the example

## Agents

1. **Document Reader** (Starter Agent)
   - Validates input has required fields (text and metadata)
   - Passes validated document to processor

2. **Text Processor** (Processor Agent)
   - Transforms text to uppercase
   - Includes retry mechanism for reliability

3. **Document Writer** (End Agent)
   - Formats output as JSON
   - Completes the workflow

## Running the Example

1. Make sure you're in the project root directory
2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

3. Run the test:
   ```bash
   python examples/document_processing/test_document_processing.py
   ```

## Expected Output

```
Testing Document Processing Example
==================================

Running test case: Basic document
✅ Basic document: Passed
Input: Hello, Multi-Agent System!
Output: HELLO, MULTI-AGENT SYSTEM!

Running test case: Empty document
✅ Empty document: Passed
Input: 
Output: 

Running test case: Special characters
✅ Special characters: Passed
Input: Hello! @#$%^&*()_+
Output: HELLO! @#$%^&*()_+

🎉 All tests passed!
```

## Modifying the Example

Try these modifications to explore the system:

1. Change the transformation type in `config.json`:
   ```json
   {
       "transformation_type": "lowercase"
   }
   ```

2. Add new test cases in `test_document_processing.py`

3. Add new stages to the workflow in `config.json`
