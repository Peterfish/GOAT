"""
GOAT Storytelling Agent - AI-powered story generation pipeline

This package provides tools for generating stories using LLMs through Ollama.

Main components:
- StoryAgent: Main class for story generation
- StoryContext: Story context manager for continuity between chapters
- Plan: Utility class for parsing and formatting story plans
- config: Configuration settings for the AI model
- prompts: Prompt templates for each generation step
- utils: Text utility functions
"""

from goat_storytelling_agent.storytelling_agent import StoryAgent
from goat_storytelling_agent.story_context import StoryContext
from goat_storytelling_agent.plan import Plan
from goat_storytelling_agent import config
from goat_storytelling_agent import prompts
from goat_storytelling_agent import utils

__version__ = "1.1.0"
__all__ = ["StoryAgent", "StoryContext", "Plan", "config", "prompts", "utils"]
