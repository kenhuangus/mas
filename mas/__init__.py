"""
Multi-Agent System (MAS) Framework
================================

A powerful framework for building distributed multi-agent systems.

Author: Ken Huang (CEO, Distributedapps.ai)
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Ken Huang"
__author_email__ = "ken@distributedapps.ai"
__license__ = "MIT"
__copyright__ = "Copyright 2025 Ken Huang, Distributedapps.ai"

from .agent import Agent, AgentType, MessageStatus
from .workflow import WorkflowManager

__all__ = [
    "Agent",
    "AgentType",
    "MessageStatus",
    "WorkflowManager"
]
