"""
Sabitler ve konfigürasyon ayarları
"""

# Ekran ayarları
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Layout oranları
PLAY_AREA_WIDTH_RATIO = 0.65  # Ekranın %65'i PlayArea
PIECE_POOL_WIDTH_RATIO = 0.30  # Ekranın %30'u PiecePool
MARGIN = 20  # Kenar boşlukları

# Renkler (Modern tema)
BACKGROUND_COLOR = (45, 52, 54)  # Koyu gri
PLAY_AREA_BG = (99, 110, 114)    # Orta gri
PIECE_POOL_BG = (178, 190, 195)  # Açık gri
GRID_LINE_COLOR = (200, 200, 200)
SHADOW_COLOR = (0, 0, 0, 100)    # Yarı saydam siyah
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (52, 152, 219)    # Mavi vurgu

# Grid boyutu seçenekleri (rows, cols)
GRID_OPTIONS = [
    (2, 3),
    (3, 3),
    (3, 4),
    (4, 4),
    (4, 5),
    (5, 5)
]

# Görsel ayarlar
GRID_LINE_WIDTH = 2
SHADOW_OFFSET = 5
HOVER_SCALE = 1.05
SNAP_THRESHOLD = 40  # Snap için mesafe eşiği (piksel)

# Animasyon
SNAP_ANIMATION_DURATION = 200  # ms

# Desteklenen resim formatları
SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.bmp']

# Stok görseller klasörü
STOCK_IMAGES_DIR = "assets/stock_images"

# Game modes
GAME_MODE_CREATIVE = "creative"  # Free mode (no time limit)
GAME_MODE_TIMED = "timed"  # Time attack mode
GAME_MODE_CHALLENGE = "challenge"  # Challenge mode (limited moves)
