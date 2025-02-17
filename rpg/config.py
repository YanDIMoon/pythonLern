# Map settings
MAP_SIZE = 200  # Size of the full game map (50x50 tiles)
TILE_SIZE = 20
WIDTH = 1280  # Fixed window width
HEIGHT = 720  # Fixed window height
FPS = 60

# Viewport settings
VIEWPORT_WIDTH = WIDTH // TILE_SIZE  
VIEWPORT_HEIGHT = HEIGHT // TILE_SIZE

# Camera settings
CAMERA_SPEED = 5
CAMERA_MARGIN = 2
COLORS = {
    "grid": (200, 200, 200),
    "background": (0, 10, 50),
    "player": (0, 255, 0),  # 🟢 Зеленый игрок
    "enemy": (255, 0, 0),     # 🔴 Красный враг
    "collision": (150, 0, 150),
    "damage": (255, 255, 0),  # 🟡 Желтый урон
    "hp_bar": (100, 255, 100),  # Здоровье игрока
}


# Minimap settings
MINIMAP_SIZE = 150  # Size in pixels
MINIMAP_MARGIN = 10  # Distance from window edges
MINIMAP_COLORS = {
    "background": (20, 20, 40),
    "player_dot": (0, 255, 0),
    "enemy_dot": (255, 0, 0),
    "border": (100, 100, 100)
}
