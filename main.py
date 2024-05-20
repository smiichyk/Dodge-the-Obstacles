import pygame
import random
import sys

pygame.init()
clock = pygame.time.Clock()

# Set up the game window
screen_width = 850
screen_height = 550
screen = pygame.display.set_mode((screen_width, screen_height))

# Load and set up background image
background_img = pygame.image.load('data/background.jpg')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Load and play background music
pygame.mixer.music.load('data/background_music.ogg')
pygame.mixer.music.play(-1)

# Set window properties
pygame.display.set_caption('Dodge the Obstacles')
icon = pygame.image.load('data/player.png')
pygame.display.set_icon(icon)

# Load player image and set player properties
player_img = pygame.image.load('data/player.png')
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 20
player_speed = 5

# Load weapon image and set weapon properties
weapon_img = pygame.image.load('data/weapon.png')
weapon_width = 35
weapon_height = 35
weapon_speed = 50
weapons = []

# Load obstacle image and set obstacle properties
obstacle_img = pygame.image.load('data/obstacle.png')
obstacle_width = 40
obstacle_height = 40
obstacle_speed = 3
obstacle_frequency = 45
obstacles = []

# Initialize game variables
score = 0
font = pygame.font.Font(None, 36)

# Load sounds
collision_sound = pygame.mixer.Sound('data/collision_sound.wav')
shoot_sound = pygame.mixer.Sound('data/shoot_sound.wav')


def display_score(x, y):
    """
    Display the current score on the game screen.

    Parameters:
    - x (int): X-coordinate of the score display.
    - y (int): Y-coordinate of the score display.
    """
    score_display = font.render("Score: " + str(score), True, (0, 100, 0))
    screen.blit(score_display, (x, y))


def game_over():
    """
    Display the game over screen with the final score.
    """
    game_over_font = pygame.font.Font(None, 64)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - 140, screen_height // 2 - 32))
    display_score(screen_width // 2 - 65, screen_height // 2 + 20)
    pygame.display.flip()


# Main game loop
game_active = True
while game_active:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False

        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            weapon_x = player_x + player_width // 2 - weapon_width // 2
            weapon_y = player_y
            weapons.append([weapon_x, weapon_y])
            shoot_sound.play()

        # Generate obstacles randomly
        if random.randint(1, obstacle_frequency) == 1:
            obstacle_x = random.randint(0, screen_width - obstacle_width)
            obstacle_y = 0
            obstacles.append([obstacle_x, obstacle_y])

        # Move weapons and obstacles
        for weapon in weapons:
            weapon[1] -= weapon_speed

        obstacles = [[obstacle[0], obstacle[1] + obstacle_speed] for obstacle in obstacles]

        # Check for collisions between weapons and obstacles
        for weapon in weapons:
            for obstacle in obstacles:
                if (
                    obstacle[0] < weapon[0] < obstacle[0] + obstacle_width and
                    obstacle[1] < weapon[1] < obstacle[1] + obstacle_height
                ):
                    weapons.remove(weapon)
                    obstacles.remove(obstacle)
                    score += 10

        # Check for collisions between player and obstacles
        for obstacle in obstacles:
            if (
                player_x < obstacle[0] < player_x + player_width or
                player_x < obstacle[0] + obstacle_width < player_x + player_width
            ) and (
                player_y < obstacle[1] < player_y + player_height or
                player_y < obstacle[1] + obstacle_height < player_y + player_height
            ):
                collision_sound.play()
                running = False

        # Remove off-screen obstacles
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] < screen_height]

        # Draw elements on the screen
        screen.fill((0, 0, 0))
        screen.blit(background_img, (0, 0))

        for obstacle in obstacles:
            screen.blit(obstacle_img, (obstacle[0], obstacle[1]))

        for weapon in weapons:
            screen.blit(weapon_img, (weapon[0], weapon[1]))

        screen.blit(player_img, (player_x, player_y))

        display_score(10, 10)

        pygame.display.flip()

        clock.tick(30)

    # Display the game over screen and exit the game
    game_over()

    # Display the play again screen
    play_again_text = font.render("Press 'A' to Play Again", True, (0, 0, 0))
    screen.blit(play_again_text, (screen_width // 2 - 150, screen_height // 2 + 50))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                waiting_for_input = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    # Reset variables and start a new game cycle
                    score = 0
                    player_x = screen_width // 2 - player_width // 2
                    player_y = screen_height - player_height - 20
                    weapons = []
                    obstacles = []
                    game_active = True
                    waiting_for_input = False

    pygame.display.flip()

pygame.quit()
sys.exit()
