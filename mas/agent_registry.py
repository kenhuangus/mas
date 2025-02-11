"""Registry of available agent types."""

from typing import Dict, Type
from .agent import Agent
from .agents.document_reader import DocumentReader
from .agents.document_processor import DocumentProcessor
from .agents.document_writer import DocumentWriter
from .agents.data_validator import DataValidator
from .agents.data_transformer import DataTransformer
from .agents.data_aggregator import DataAggregator
from .agents.data_formatter import DataFormatter

# Registry of agent types to their implementing classes
AGENT_REGISTRY: Dict[str, Type[Agent]] = {
    # Document Processing Agents
    "document_reader": DocumentReader,
    "document_processor": DocumentProcessor,
    "document_writer": DocumentWriter,
    
    # Data Pipeline Agents
    "data_validator": DataValidator,
    "data_transformer": DataTransformer,
    "data_aggregator": DataAggregator,
    "data_formatter": DataFormatter
}
