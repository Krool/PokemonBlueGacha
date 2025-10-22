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

# File paths (relative to project root)
POKEMON_CSV = "data/pokemon_gen1.csv"
TYPES_CSV = "data/pokemon_types.csv"
RARITY_CSV = "data/rarity_drop_weights.csv"
GACHA_MACHINES_CSV = "data/gacha_machines.csv"
ITEMS_CSV = "data/items_gen1.csv"
SAVE_FILE = "saves/player_save.json"

# Asset paths (relative to project root)
SPRITES_PATH = "Assets/Sprites/Pokemon/"
TYPES_PATH = "Assets/Sprites/Types/"
SOUNDS_PATH = "Assets/Sounds/"
TITLE_FONT_PATH = "Assets/Font/TitleFont.ttf"
BODY_FONT_PATH = "Assets/Font/8BitFont.ttf"

# UI Images
LOGO_PATH = "Assets/Sprites/Main/logo.png"
GACHA_RED_PATH = "Assets/Sprites/Main/gacha_red.png"
GACHA_BLUE_PATH = "Assets/Sprites/Main/gacha_blue.png"
GACHA_YELLOW_PATH = "Assets/Sprites/Main/gacha_yellow.png"
GACHA_ITEM_PATH = "Assets/Sprites/Main/gacha_item.png"
POKEDOLLAR_ICON_PATH = "Assets/Sprites/Main/pokedollar_icon.png"
RAYS_PATH = "Assets/Sprites/Main/rays.png"

# Game balance
STARTING_GOLD = 0
GOLD_CHEAT_AMOUNT = 10000
# Note: Pull costs now come from gacha_machines.csv per version

# Animation settings
MAX_ANIMATION_TIME = 2.0  # seconds
LOADING_TIME = 4.0  # seconds for loading screen

