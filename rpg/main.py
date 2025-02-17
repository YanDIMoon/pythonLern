import pygame
import numpy as np
from config import WIDTH, HEIGHT, TILE_SIZE, FPS, COLORS, MAP_SIZE, MINIMAP_COLORS,MINIMAP_SIZE, MINIMAP_MARGIN
from battle import Unit
from ai import get_enemy_move
import random 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tactical RPG")
clock = pygame.time.Clock()

# Camera offset for scrolling
camera_x = 0
camera_y = 0

# Initialize player and enemy on the larger map
player = Unit("Hero", 100, random.randint(10, 20), random.randint(3, 8), random.randint(0, MAP_SIZE-1), random.randint(0, MAP_SIZE-1))
enemy = Unit("Orc", 80, random.randint(8, 15), random.randint(3, 7), random.randint(0, MAP_SIZE-1), random.randint(0, MAP_SIZE-1))
combat_turn = "player"

def draw_units():
    # Draw units with camera offset
    screen_x = player.x * TILE_SIZE - camera_x
    screen_y = player.y * TILE_SIZE - camera_y
    enemy_screen_x = enemy.x * TILE_SIZE - camera_x
    enemy_screen_y = enemy.y * TILE_SIZE - camera_y

    # Only draw if within screen bounds
    if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
        if (player.x, player.y) == (enemy.x, enemy.y):
            pygame.draw.rect(screen, COLORS["collision"], (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
        else:
            pygame.draw.rect(screen, COLORS["player"], (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
            if 0 <= enemy_screen_x < WIDTH and 0 <= enemy_screen_y < HEIGHT:
                pygame.draw.rect(screen, COLORS["enemy"], (enemy_screen_x, enemy_screen_y, TILE_SIZE, TILE_SIZE))
            
            if player.hp > 0:
                pygame.draw.rect(screen, COLORS["hp_bar"], (screen_x, screen_y - 5, TILE_SIZE * (max(0, player.hp)/100), 3))
            if enemy.hp > 0 and 0 <= enemy_screen_x < WIDTH and 0 <= enemy_screen_y < HEIGHT:
                pygame.draw.rect(screen, COLORS["hp_bar"], (enemy_screen_x, enemy_screen_y - 5, TILE_SIZE * (max(0, enemy.hp)/80), 3))

def handle_combat():
    global combat_turn
    if combat_turn == "player":
        received_damage = enemy.take_damage(player.attack)
        print(f"⚔️ {player.name} атакует {enemy.name} и наносит {received_damage} урона!")
        combat_turn = "enemy"
    else:
        received_damage = player.take_damage(enemy.attack)
        print(f"⚔️ {enemy.name} атакует {player.name} и наносит {received_damage} урона!")
        combat_turn = "player"

def reset_game():
    pygame.event.clear()
    pygame.display.flip()
    screen.fill(COLORS["background"])
    global player, enemy, combat_turn, camera_x, camera_y

    # Store current progression
    player_stats = {
        'level': player.level,
        'exp': player.experience,
        'exp_next': player.exp_to_next_level
    }

    player = Unit("Hero", 100, player.attack, player.defense, random.randint(0, MAP_SIZE-1), random.randint(0, MAP_SIZE-1))
    player.level = player_stats['level']
    player.experience = player_stats['exp']
    player.exp_to_next_level = player_stats['exp_next']
    
    # Scale enemy based on player's level
    base_hp = 80 + (10 * player.level)
    base_attack = random.randint(8 + player.level, 15 + player.level)
    base_defense = random.randint(3 + player.level//2, 7 + player.level//2)

    enemy = Unit("Orc", base_hp, base_attack, base_defense, random.randint(0, MAP_SIZE-1), random.randint(0, MAP_SIZE-1))

    # Reset camera
    camera_x = 0
    camera_y = 0
    combat_turn = "player"

def draw_minimap():
    # Create minimap surface
    minimap = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
    minimap.fill(MINIMAP_COLORS["background"])
    
    # Calculate scale factors
    scale_x = MINIMAP_SIZE / (MAP_SIZE * TILE_SIZE)
    scale_y = MINIMAP_SIZE / (MAP_SIZE * TILE_SIZE)
    
    # Draw player and enemy positions
    player_mini_x = int(player.x * TILE_SIZE * scale_x)
    player_mini_y = int(player.y * TILE_SIZE * scale_y)
    enemy_mini_x = int(enemy.x * TILE_SIZE * scale_x)
    enemy_mini_y = int(enemy.y * TILE_SIZE * scale_y)
    
    # Draw dots
    pygame.draw.circle(minimap, MINIMAP_COLORS["player_dot"], (player_mini_x, player_mini_y), 3)
    pygame.draw.circle(minimap, MINIMAP_COLORS["enemy_dot"], (enemy_mini_x, enemy_mini_y), 3)
    
    # Draw border
    pygame.draw.rect(minimap, MINIMAP_COLORS["border"], (0, 0, MINIMAP_SIZE, MINIMAP_SIZE), 1)
    
    # Draw minimap on main screen
    screen.blit(minimap, (MINIMAP_MARGIN, MINIMAP_MARGIN))

running = True
while running:
    screen.fill(COLORS["background"])
    # Update camera to follow player
    camera_x = player.x * TILE_SIZE - WIDTH // 2
    camera_y = player.y * TILE_SIZE - HEIGHT // 2
    
    # Keep camera within map bounds
    camera_x = max(0, min(camera_x, MAP_SIZE * TILE_SIZE - WIDTH))
    camera_y = max(0, min(camera_y, MAP_SIZE * TILE_SIZE - HEIGHT))
    draw_minimap()
    draw_units()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        elif event.type == pygame.KEYDOWN:
            new_x, new_y = player.x, player.y
            if event.key == pygame.K_w:
                new_y = player.y - 1
            elif event.key == pygame.K_s:
                new_y = player.y + 1
            elif event.key == pygame.K_a:
                new_x = player.x - 1
            elif event.key == pygame.K_d:
                new_x = player.x + 1
            elif event.key == pygame.K_q:
                running = False
                break

            # Check if new position is within map bounds
            if 0 <= new_x < MAP_SIZE and 0 <= new_y < MAP_SIZE:
                player.move(new_x, new_y)

            if player.hp > 0 and enemy.hp > 0:
                new_enemy_x, new_enemy_y = get_enemy_move(enemy, player)
                if 0 <= new_enemy_x < MAP_SIZE and 0 <= new_enemy_y < MAP_SIZE:
                    enemy.x, enemy.y = new_enemy_x, new_enemy_y

            if (player.x, player.y) == (enemy.x, enemy.y) and player.hp > 0 and enemy.hp > 0:
                handle_combat()

    if player.hp <= 0 or enemy.hp <= 0:
        if player.hp <= 0:
            exp_gain = 25 * enemy.level
            enemy.gain_experience(exp_gain)
            print(f"Игрок погиб. {enemy.name} получает {exp_gain} опыта!")
            print("Нажмите Enter для новой игры.")
        else:
            exp_gain = 50 * enemy.level
            player.gain_experience(exp_gain)
            print(f"Враг повержен! {player.name} получает {exp_gain} опыта!")
            print("Нажмите Enter для новой игры.")

        waiting = True
        while waiting and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        waiting = False
                        running = False
                    elif event.key == pygame.K_RETURN:
                        reset_game()
                        waiting = False

    if (player.x, player.y) == (enemy.x, enemy.y) and player.hp > 0 and enemy.hp > 0:
        while player.hp > 0 and enemy.hp > 0 and running:
            screen.fill(COLORS["background"])
            draw_units()
            draw_minimap()  # Add this line
        
            draw_units()
            
            if combat_turn == "player":
                print(f"\nВаш ход! HP Игрока: {player.hp}, HP Врага: {enemy.hp}")
                print("Нажмите SPACE для атаки...")
                waiting_input = True
                while waiting_input and running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            waiting_input = False
                            running = False
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            handle_combat()
                            waiting_input = False
                    pygame.display.flip()
                    clock.tick(FPS)
            else:
                print(f"\nХод врага! HP Игрока: {player.hp}, HP Врага: {enemy.hp}")
                handle_combat()
            
            pygame.display.flip()
            clock.tick(FPS)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

