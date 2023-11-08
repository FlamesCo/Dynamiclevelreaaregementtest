import pygame
import random

# Initialization
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game Variables
enemy_rows = 5
enemy_cols = 11
enemy_width = 40
enemy_height = 40
player_width = 60
player_height = 20
player_velocity = 5
bullet_width = 5
bullet_height = 10
bullet_velocity = 7
enemy_velocity_x = 1
enemy_velocity_y = 40
move_down = False

score = 0
lives = 3

# Function to reset the game
def reset_game():
    global player, enemies, player_bullets, enemy_bullets, score, lives, enemy_velocity_x, move_down
    player = pygame.Rect(screen_width//2, screen_height - 60, player_width, player_height)
    enemies = [pygame.Rect(col * (enemy_width + 10) + 50, row * (enemy_height + 10) + 50, enemy_width, enemy_height)
               for row in range(enemy_rows) for col in range(enemy_cols)]
    player_bullets = []
    enemy_bullets = []
    score = 0
    lives = 3
    enemy_velocity_x = 1
    move_down = False

reset_game()

# Main game loop
running = True
game_over = False
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement handling
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.right < screen_width:
            player.x += player_velocity
        if keys[pygame.K_SPACE]:
            if not player_bullets:
                player_bullets.append(pygame.Rect(player.x + player.width//2, player.y, bullet_width, bullet_height))

    # Update game state
    for bullet in player_bullets:
        bullet.y -= bullet_velocity
        if bullet.y < 0:
            player_bullets.remove(bullet)

    # Move enemies
    for enemy in enemies:
        enemy.x += enemy_velocity_x
        if move_down:
            enemy.y += enemy_velocity_y
    move_down = False

    # Check if enemies need to drop down and change direction
    for enemy in enemies:
        if enemy.right >= screen_width or enemy.left <= 0:
            enemy_velocity_x *= -1
            move_down = True
            break

    # Collision detection
    for enemy in enemies[:]:
        for bullet in player_bullets[:]:
            if bullet.colliderect(enemy):
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Check for game over/win conditions
    if not enemies:
        game_over = True
        win = True
    elif any(enemy.y + enemy.height > player.y for enemy in enemies):
        game_over = True
        win = False

    # Game Display
    screen.fill(BLACK)

    # Draw player
    pygame.draw.rect(screen, WHITE, player)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Draw bullets
    for bullet in player_bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Display score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Game over conditions
    if game_over:
        if win:
            end_text = font.render('You Win! Press SPACE to play again.', True, GREEN)
        else:
            end_text = font.render('You Lose. Press SPACE to retry.', True, RED)
        screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - end_text.get_height() // 2))
        if keys[pygame.K_SPACE]:
            game_over = False
            win = False
            reset_game()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
