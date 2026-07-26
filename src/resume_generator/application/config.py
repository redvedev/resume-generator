"""Configuration settings for the resume builder."""
from pathlib import Path
import logging

# Model settings
MAX_TOKENS = 8192
TEMPERATURE = 0.7

# File paths
DATA_DIR = Path("data/personal_data")
TEMPLATE_DIR = Path("data/template")
OUTPUT_DIR = Path("data/output")
OFFER_DIR = Path("data/offers")

# Compilation settings
KEEP_TEX = True      # Keep .tex file after compilation
RUN_PDFLATEX = True  # Automatically compile with pdflatex

LOGGING_LEVEL = logging.INFO