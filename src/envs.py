from pathlib import Path
from jinja2 import Environment, FileSystemLoader

templates_dir = Path(__file__).parent / "Templates"
env = Environment(loader=FileSystemLoader(templates_dir))
static_dir = Path(__file__).parent / "static"
sessions = {}