"""Flake8 plugin entry point for bekci."""

__version__ = "0.1.3"

from .plugin import Plugin

__all__ = ["Plugin", "__version__"]
