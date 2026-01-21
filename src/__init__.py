"""
Resume Agent - AI-powered candidate screening system

This package contains the core components for processing resumes,
extracting skills, analyzing GitHub profiles, and ranking candidates.
"""

__version__ = "0.1.0"
__author__ = "Dana Martinez"

from .resume_parser import ResumeParser
from .skill_extractor import SkillExtractor

__all__ = ["ResumeParser", "SkillExtractor"]