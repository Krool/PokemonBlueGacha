"""
Game configuration constants
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (64, 64, 64)

# File paths - work for both desktop and web
import os
import sys

# Detect if running in browser (Pygbag)
IS_WEB = sys.platform == "emscripten"

# Determine base path: check if we're in src/ directory or project root
# If data/ exists locally, we're in src (web), otherwise we're in root (desktop from project root)
def get_base_path():
    if IS_WEB or os.path.exists("data"):
        return ""  # We're in src/ or web, use relative paths
    else:
        return "../"  # We're running from project root, go up from src/

BASE_PATH = get_base_path()

# File paths
POKEMON_CSV = os.path.join(BASE_PATH, "data/pokemon_gen1.csv")
TYPES_CSV = os.path.join(BASE_PATH, "data/pokemon_types.csv")
RARITY_CSV = os.path.join(BASE_PATH, "data/rarity_drop_weights.csv")
GACHA_MACHINES_CSV = os.path.join(BASE_PATH, "data/gacha_machines.csv")
ITEMS_CSV = os.path.join(BASE_PATH, "data/items_gen1.csv")
SAVE_FILE = os.path.join(BASE_PATH, "saves/player_save.json") if not IS_WEB else "player_save.json"

# Asset paths
SPRITES_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Pokemon/")
TYPES_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Types/")
ITEMS_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Items/")
SOUNDS_PATH = os.path.join(BASE_PATH, "Assets/Sounds/")
TITLE_FONT_PATH = os.path.join(BASE_PATH, "Assets/Font/TitleFont.ttf")
BODY_FONT_PATH = os.path.join(BASE_PATH, "Assets/Font/8BitFont.ttf")

# UI Images
LOGO_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Main/logo.png")
GACHA_RED_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Main/gacha_red.png")
GACHA_BLUE_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Main/gacha_blue.png")
GACHA_YELLOW_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Main/gacha_yellow.png")
GACHA_ITEM_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Main/gacha_item.png")
POKEDOLLAR_ICON_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Main/pokedollar_icon.png")
RAYS_PATH = os.path.join(BASE_PATH, "Assets/Sprites/Main/rays.png")

# Game balance
STARTING_GOLD = 0
GOLD_CHEAT_AMOUNT = 10000
# Note: Pull costs now come from gacha_machines.csv per version

# Animation settings
MAX_ANIMATION_TIME = 2.0  # seconds
LOADING_TIME = 4.0  # seconds for loading screen

