"""
Constants and configuration settings
"""

# Screen settings
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Layout ratios
PLAY_AREA_WIDTH_RATIO = 0.65  
PIECE_POOL_WIDTH_RATIO = 0.30  
MARGIN = 20  

# Colors (Modern theme)
BACKGROUND_COLOR = (45, 52, 54)  
PLAY_AREA_BG = (99, 110, 114)    
PIECE_POOL_BG = (178, 190, 195)  
GRID_LINE_COLOR = (200, 200, 200)
SHADOW_COLOR = (0, 0, 0, 100)    
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (52, 152, 219)    

# Grid size options (rows, cols)
GRID_OPTIONS = [
    (2, 3),
    (3, 3),
    (3, 4),
    (4, 4),
    (4, 5),
    (5, 5)
]

# Visual settings
GRID_LINE_WIDTH = 2
SHADOW_OFFSET = 5
HOVER_SCALE = 1.05
SNAP_THRESHOLD = 40  

# Animation
SNAP_ANIMATION_DURATION = 200  

# Supported image formats
SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.bmp']

# Stock images folder
STOCK_IMAGES_DIR = "assets/stock_images"

# Game modes
GAME_MODE_CREATIVE = "creative"  
GAME_MODE_TIMED = "timed"  
GAME_MODE_CHALLENGE = "challenge"  
