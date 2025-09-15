from fastapi.templating import Jinja2Templates
from pathlib import Path

ROOT_PATH = Path(__file__).parent
templates_folder = ROOT_PATH / "web" / "templates"

templates = Jinja2Templates(templates_folder)