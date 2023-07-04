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
GREY = (24, 22, 29)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (30, 141, 68)
GOLD = (255, 215, 0)
DULL_YELLOW = (128, 128, 0)
ORANGE = (247, 147, 39)
PLAYER_YELLOW = (255, 229, 105)
PLAYER_RED = (183, 4, 4)
CONTINUE_COLOR = (37, 186, 67)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join("Assets", "oddlook.mp3"))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "ImpactEffect.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "LaserEffect.mp3"))

HEALTH_FONT = pygame.font.SysFont("consolas", 40)
HEALTH_FONT_BG = pygame.font.SysFont("consolas", 41, True)
TITLE_FONT = pygame.font.SysFont("consolas", 55)
INSTRUCTION_TEXT = pygame.font.SysFont("consolas", 25)
WINNER_FONT = pygame.font.SysFont("consolas", 100)
CONTROLS_FONT = pygame.font.SysFont("consolas", 25)

FPS = 60
YELLOW_SPACESHIP_WIDTH, YELLOW_SPACESHIP_HEIGHT = 75, 60
RED_SPACESHIP_WIDTH, RED_SPACESHIP_HEIGHT = 65, 50

# control the speed of the spaceships/bullets and the amount of bullets spaceships can shoot at a time
VELOCITY = 5
BULLET_VELOCITY = 12
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


# import assets and store them inside the global variables
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        YELLOW_SPACESHIP_IMAGE, (YELLOW_SPACESHIP_WIDTH, YELLOW_SPACESHIP_HEIGHT)
    ),
    270,
)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        RED_SPACESHIP_IMAGE, (RED_SPACESHIP_WIDTH, RED_SPACESHIP_HEIGHT)
    ),
    90,
)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space2.jpg")), (WIDTH, HEIGHT)
)
SPACE2 = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space3.png")), (WIDTH, HEIGHT)
)


# draw_window function that will draw all the assets and their position on the screen. Updates the display at the end of the function
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, GREY, BORDER)

    red_health_text_bg = HEALTH_FONT_BG.render("Health", 1, RED)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text_bg = HEALTH_FONT_BG.render("Health", 1, DULL_YELLOW)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

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


# draws the instruction screen containing the controls
def draw_instructions():
    WIN.blit(SPACE2, (0, 0))
    darkener = pygame.Surface((WIDTH, HEIGHT))
    darkener.set_alpha(128)
    darkener.fill(BLACK)

    title_text = TITLE_FONT.render("Spaceship Battles", 1, ORANGE)

    welcome_text1 = INSTRUCTION_TEXT.render(
        "Welcome to outer space! Get ready to battle with a friend. Each", 1, WHITE
    )
    welcome_text2 = INSTRUCTION_TEXT.render(
        "player will control a spaceship and shoot their bullets at the", 1, WHITE
    )
    welcome_text3 = INSTRUCTION_TEXT.render(
        "other player. The person whose health first reaches 0 loses!", 1, WHITE
    )
    player1 = HEALTH_FONT.render("Player 1:", 1, PLAYER_YELLOW)
    player2 = HEALTH_FONT.render("Player 2:", 1, PLAYER_RED)
    player1_movement = CONTROLS_FONT.render("W, A, S, D  - Move Spaceship", 1, WHITE)
    player1_shooting = CONTROLS_FONT.render("Left CTRL   - Shoot Bullet", 1, WHITE)
    player2_movement = CONTROLS_FONT.render("ARROW keys  - Move Spaceship", 1, WHITE)
    player2_shooting = CONTROLS_FONT.render("Right CTRL  - Shoot Bullet", 1, WHITE)
    continue_text = INSTRUCTION_TEXT.render(
        "Press ENTER to continue...", 1, CONTINUE_COLOR
    )

    WIN.blit(darkener, (0, 0))
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))
    WIN.blit(welcome_text1, (10, title_text.get_height() + 50))
    WIN.blit(
        welcome_text2, (10, title_text.get_height() + welcome_text1.get_height() + 60)
    )
    WIN.blit(
        welcome_text3,
        (
            10,
            title_text.get_height()
            + welcome_text1.get_height()
            + welcome_text2.get_height()
            + 70,
        ),
    )
    WIN.blit(player1, (10, 250))
    WIN.blit(player2, (WIDTH // 2 + 10, 250))
    WIN.blit(player1_movement, (10, 280 + player1.get_height()))
    WIN.blit(
        player1_shooting,
        (10, 340 + player1.get_height() + player1_movement.get_height()),
    )
    WIN.blit(player2_movement, (WIDTH // 2 + 10, 280 + player2.get_height()))
    WIN.blit(
        player2_shooting,
        (WIDTH // 2 + 10, 340 + player2.get_height() + player2_movement.get_height()),
    )
    WIN.blit(
        continue_text,
        (
            WIDTH // 2 - continue_text.get_width() // 2,
            HEIGHT - continue_text.get_height() - 10,
        ),
    )

    pygame.display.update()


# draws the end screen containing the player's scores
def draw_end_screen(red_health, yellow_health, red, yellow):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, GREY, BORDER)

    darkener = pygame.Surface((WIDTH, HEIGHT))
    darkener.set_alpha(128)
    darkener.fill(BLACK)

    final_score_text = TITLE_FONT.render("Final Score", 1, WHITE)
    score_text = TITLE_FONT.render(
        str(yellow_health) + " - " + str(red_health), 1, WHITE
    )
    score_text_yellow = TITLE_FONT.render(str(yellow_health), 1, PLAYER_YELLOW)
    score_text_red = TITLE_FONT.render(str(red_health), 1, PLAYER_RED)
    score_text_space = TITLE_FONT.render(str(yellow_health) + " - ", 1, WHITE)

    restart_text = TITLE_FONT.render("RESTART", 1, GREEN)
    quit_text = TITLE_FONT.render("QUIT", 1, RED)

    WIN.blit(darkener, (0, 0))
    WIN.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, 10))
    WIN.blit(
        score_text,
        (WIDTH // 2 - score_text.get_width() // 2, final_score_text.get_height() + 60),
    )
    WIN.blit(
        score_text_yellow,
        (WIDTH // 2 - score_text.get_width() // 2, final_score_text.get_height() + 60),
    )
    WIN.blit(
        score_text_red,
        (
            WIDTH // 2 - score_text.get_width() // 2 + score_text_space.get_width(),
            final_score_text.get_height() + 60,
        ),
    )

    pygame.draw.rect(WIN, GREEN, (75, 250, 300, 125), 5)
    pygame.draw.rect(WIN, RED, (WIDTH - 375, 250, 300, 125), 5)
    WIN.blit(
        restart_text,
        (225 - restart_text.get_width() // 2, 313 - restart_text.get_height() // 2),
    )
    WIN.blit(
        quit_text,
        (
            WIDTH - 225 - quit_text.get_width() // 2,
            313 - restart_text.get_height() // 2,
        ),
    )

    red.x = 700
    red.y = 300
    yellow.x = 100
    yellow.y = 300

    pygame.display.update()


# updates the movement of the yellow ship
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and (yellow.x - VELOCITY > 0):  # LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and (
        yellow.x + VELOCITY + yellow.width - 20 < BORDER.x
    ):  # RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and (yellow.y - VELOCITY > 0):  # UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and (
        yellow.y + VELOCITY + yellow.height < HEIGHT - 15
    ):  # DOWN
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


# handles the movements and collision of the bullets
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


# main function that will start the game and keep it running until user exits
def main():
    red = pygame.Rect(700, 300, RED_SPACESHIP_WIDTH, RED_SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, YELLOW_SPACESHIP_WIDTH, YELLOW_SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    instruct = True
    run = False
    end = False
    my_quit = False

    clock = pygame.time.Clock()
    winner_text = ""

    # adjust volume for the sound effects and music
    BACKGROUND_MUSIC.set_volume(0.7)
    BULLET_FIRE_SOUND.set_volume(0.7)
    BULLET_HIT_SOUND.set_volume(0.7)
    BACKGROUND_MUSIC.play()

    while not my_quit:
        try:
            while instruct:
                clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            instruct = False
                            run = True

                draw_instructions()

            while end:
                clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = False
                        pygame.quit()

                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()

                        if (
                            pos[0] >= 75
                            and pos[0] <= 375
                            and pos[1] >= 250
                            and pos[1] <= 375
                        ):
                            yellow_bullets.clear()
                            red_bullets.clear()
                            end = False
                            run = True
                            red_health = yellow_health = 10

                        if (
                            pos[0] >= (WIDTH - 375)
                            and pos[0] <= (WIDTH - 75)
                            and pos[1] >= 250
                            and pos[1] <= 375
                        ):
                            end = False
                            my_quit = True

                draw_end_screen(red_health, yellow_health, red, yellow)

            while run:
                clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:
                        if (
                            event.key == pygame.K_LCTRL
                            and len(yellow_bullets) < MAX_BULLETS
                        ):
                            bullet = pygame.Rect(
                                yellow.x + yellow.width,
                                yellow.y + yellow.height // 2 - 2,
                                10,
                                5,
                            )
                            yellow_bullets.append(bullet)
                            BULLET_FIRE_SOUND.play()

                        if (
                            event.key == pygame.K_RCTRL
                            and len(red_bullets) < MAX_BULLETS
                        ):
                            bullet = pygame.Rect(
                                red.x, red.y + red.height // 2 - 2, 10, 5
                            )
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
                    run = False
                    end = True

                keys_pressed = pygame.key.get_pressed()
                yellow_handle_movement(keys_pressed, yellow)
                red_handle_movement(keys_pressed, red)

                handle_bullets(yellow_bullets, red_bullets, yellow, red)

                draw_window(
                    red, yellow, red_bullets, yellow_bullets, red_health, yellow_health
                )
        except pygame.error:
            my_quit = True


if __name__ == "__main__":
    main()
