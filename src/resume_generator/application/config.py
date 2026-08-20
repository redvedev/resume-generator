"""Configuration settings for the resume builder."""

import logging
from pathlib import Path

# File paths
DATA_DIR = Path("data")
PERSONAL_INFO_DIR = DATA_DIR / "personal_data"
TEMPLATE_DIR = DATA_DIR / "template"

OUTPUT_DIR = Path("data/output")
OFFER_DIR = Path("data/offers")

# Compilation settings
KEEP_TEX = True  # Keep .tex file after compilation
RUN_PDFLATEX = True  # Automatically compile with pdflatex

LOGGING_LEVEL = logging.INFO
