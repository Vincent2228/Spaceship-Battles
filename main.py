import pygame
import os
pygame.font.init()
pygame.mixer.init()

# open and set the dimensions of the window along with the caption at the top of the window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACESHIP BATTLES")


# global variables stored for later use
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (30, 141, 68)
GOLD = (255, 215, 0)
DULL_YELLOW = (128, 128, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('Assets', 'oddlook.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'ImpactEffect.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'LaserEffect.mp3'))

HEALTH_FONT = pygame.font.SysFont('consolas', 40)
HEALTH_FONT_BG = pygame.font.SysFont('consolas', 41, True)
WINNER_FONT = pygame.font.SysFont('consolas', 100)

FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# control the speed of the spaceships/bullets and the amount of bullets a spaceship can shoot at a time
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


# import assets and store them inside the global variables
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space2.jpg')), (WIDTH, HEIGHT))

 
# draw_window function that will draw all the assets and their position on the screen. Updates the display at the end of the function
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text_bg = HEALTH_FONT_BG.render(
        "Health", 1, RED)
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text_bg = HEALTH_FONT_BG.render(
        "Health", 1, DULL_YELLOW)   
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text_bg, (WIDTH - red_health_text.get_width() - 12, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text_bg, (8, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets: 
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


# updates the movement of the yellow ship
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and (yellow.x - VELOCITY > 0):  # LEFT
        yellow.x -= VELOCITY
    # RIGHT
    if keys_pressed[pygame.K_d] and (yellow.x + VELOCITY + yellow.width < BORDER.x):
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and (yellow.y - VELOCITY > 0):  # UP
        yellow.y -= VELOCITY
    # DOWN
    if keys_pressed[pygame.K_s] and (yellow.y + VELOCITY + yellow.height < HEIGHT - 15):
        yellow.y += VELOCITY


# updates the movement of the red ship
def red_handle_movement(keys_pressed, red):
    # LEFT
    if keys_pressed[pygame.K_LEFT] and (red.x - VELOCITY > BORDER.x + BORDER.width):
        red.x -= VELOCITY
    # RIGHT
    if keys_pressed[pygame.K_RIGHT] and (red.x + VELOCITY + red.width < WIDTH):
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and (red.y - VELOCITY > 0):  # UP
        red.y -= VELOCITY
    # DOWN
    if keys_pressed[pygame.K_DOWN] and (red.y + VELOCITY + red.height < HEIGHT - 15):
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, GOLD)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


# main function that will start the game and keep it running until user exits
def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    run = True
    clock = pygame.time.Clock()
    
    BACKGROUND_MUSIC.play()
    
    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit( )

            if event.type == pygame.KEYDOWN and len(yellow_bullets) < MAX_BULLETS:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if red_health <= 0:
            winner_text = "YELLOW WINS"

        if yellow_health <= 0:
            winner_text = "RED WINS"

        if winner_text != "":
            draw_winner(winner_text)
            BACKGROUND_MUSIC.stop()
            break

        print(red_bullets, yellow_bullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
