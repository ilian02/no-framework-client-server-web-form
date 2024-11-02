"""
Place to store all important outside variables
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader


templates_dir = Path(__file__).parent / "Templates"
static_dir = Path(__file__).parent / "static"
env = Environment(loader=FileSystemLoader(templates_dir))
