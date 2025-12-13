"""
World Happiness Dashboard Package

This package contains modules for analyzing the World Happiness Report dataset.
"""

__version__ = "1.0.0"

from .data_loader import DataLoader
from .data_cleaner import DataCleaner
from .analyzer import Analyzer
from .index_calculator import IndexCalculator
from .visualizer import Visualizer
from .insight_engine import InsightEngine

__all__ = [
    'DataLoader',
    'DataCleaner',
    'Analyzer',
    'IndexCalculator',
    'Visualizer',
    'InsightEngine'
]

