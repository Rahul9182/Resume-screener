"""
Information extraction modules for resume parsing
"""
from .langchain_extractor import extract_with_langchain
from .vision_extractor import extract_with_openai_vision

__all__ = [
    'extract_with_langchain',
    'extract_with_openai_vision'
]