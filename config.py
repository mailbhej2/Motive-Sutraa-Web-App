from pathlib import Path
from dotenv import load_dotenv
import os

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Application
# ==========================================================

APP_NAME = "Motive Sutraa ֎🇦🇮 Studio"
APP_VERSION = "1.0"

# ==========================================================
# Window
# ==========================================================

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# ==========================================================
# AI Models
# ==========================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

TEXT_MODEL = "gemini-2.5-pro"
FAST_MODEL = "gemini-2.5-flash"

# ==========================================================
# Languages
# ==========================================================

LANGUAGES = [
    "Hindi",
    "English",
]

DEFAULT_LANGUAGE = "Hindi"

# ==========================================================
# Duration
# ==========================================================

MIN_DURATION = 1
MAX_DURATION = 60
DEFAULT_DURATION = 5

# ==========================================================
# UI
# ==========================================================

IMAGE_BATCH_SIZE = 5

# ==========================================================
# Prompt Structure Constants
# ==========================================================

IMAGE_SHOT_TYPE = "Cinematic Photo"

VIDEO_SHOT_TYPE = "Cinematic Video"

VIDEO_MAIN_VISUAL_REFERENCE = (
    "Crucial: Preserve all 3D animated character(s) from the attached "
    "image exactly as shown. Maintain identical facial features, body "
    "proportions, hairstyle, fur/skin texture, clothing, accessories, "
    "expressions, and overall animated appearance. Keep the same "
    "stylized 3D animation design throughout. Never transform the "
    "characters into realistic humans or alter their artistic style. "
    "Strict global consistency constraint: Maintain the exact same "
    "animated character models, art style, and asset identity across "
    "this and all subsequent scenes."
)

VIDEO_VOICE_PROFILE = (
    "Strictly deep, clear only male voice speaking the voiceover "
    "explicitly in Hindi language."
)

VIDEO_VOICE_CONSISTENCY = (
    "Maintain a perfectly consistent voice tone, pitch, and delivery "
    "style across all outputs."
)

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

PROMPTS_DIR = BASE_DIR / "prompts"

OUTPUT_DIR = BASE_DIR / "output"

PROJECTS_DIR = OUTPUT_DIR / "projects"
IMAGES_DIR = OUTPUT_DIR / "images"
VIDEOS_DIR = OUTPUT_DIR / "videos"
JSON_DIR = OUTPUT_DIR / "json"
EXPORTS_DIR = OUTPUT_DIR / "exports"

LAST_JSON_FILE = JSON_DIR / "last_generation.json"

ASSETS_DIR = BASE_DIR / "assets"

LOGS_DIR = BASE_DIR / "logs"

TEMP_DIR = BASE_DIR / "temp"

EXAMPLES_DIR = BASE_DIR / "examples"

# ==========================================================
# Prompt Files
# ==========================================================

STORY_PROMPT_FILE = PROMPTS_DIR / "story.txt"

SCENE_PROMPT_FILE = PROMPTS_DIR / "scene.txt"

IMAGE_PROMPT_FILE = PROMPTS_DIR / "image_prompt.txt"

FLOW_PROMPT_FILE = PROMPTS_DIR / "flow_json.txt"

# ==========================================================
# Create Required Directories
# ==========================================================

for folder in (
    PROMPTS_DIR,
    OUTPUT_DIR,
    PROJECTS_DIR,
    IMAGES_DIR,
    VIDEOS_DIR,
    JSON_DIR,
    EXPORTS_DIR,
    ASSETS_DIR,
    LOGS_DIR,
    TEMP_DIR,
    EXAMPLES_DIR,
):
    folder.mkdir(parents=True, exist_ok=True)