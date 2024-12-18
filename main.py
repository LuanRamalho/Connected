import random
import pygame
import json
import os

from objects import Balls, Coins, Tiles, Particle, Message, Button

# Função para carregar o HighScore do arquivo JSON
def load_highscore():
    if not os.path.exists('highscore.json'):
        save_highscore(0)  # Cria o arquivo se não existir
    try:
        with open('highscore.json', 'r') as file:
            data = json.load(file)
            return data.get("highscore", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0  # Retorna 0 em caso de erro

# Função para salvar o HighScore no arquivo JSON
def save_highscore(score):
    with open('highscore.json', 'w') as file:
        json.dump({"highscore": score}, file)

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH // 2, HEIGHT // 2

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption('Connected')

clock = pygame.time.Clock()
FPS = 90

# COLORS **********************************************************************
RED = (255, 0, 0)
GREEN = (0, 177, 64)
BLUE = (30, 144, 255)
ORANGE = (252, 76, 2)
YELLOW = (254, 221, 0)
PURPLE = (155, 38, 182)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (25, 25, 25)

color_list = [PURPLE, GREEN, BLUE, ORANGE, YELLOW, RED]
color_index = 0
color = color_list[color_index]

# SOUNDS **********************************************************************
flip_fx = pygame.mixer.Sound('Sounds/flip.mp3')
score_fx = pygame.mixer.Sound('Sounds/point.mp3')
dead_fx = pygame.mixer.Sound('Sounds/dead.mp3')
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')

pygame.mixer.music.load('Sounds/bgm.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

# FONTS ***********************************************************************
title_font = "Fonts/Aladin-Regular.ttf"
score_font = "Fonts/DroneflyRegular-K78LA.ttf"
game_over_font = "Fonts/ghostclan.ttf"
final_score_font = "Fonts/DalelandsUncialBold-82zA.ttf"
new_high_font = "Fonts/BubblegumSans-Regular.ttf"

connected = Message(WIDTH // 2, 120, 55, "ConnecteD", title_font, WHITE, win)
score_msg = Message(WIDTH // 2, 100, 60, "0", score_font, (150, 150, 150), win)
highscore_msg = Message(50, 10, 20, "Highscore: 0", score_font, WHITE, win)  # Exibe o highscore no jogo
game_msg = Message(80, 150, 40, "GAME", game_over_font, BLACK, win)
over_msg = Message(210, 150, 40, "OVER!", game_over_font, WHITE, win)
final_score = Message(WIDTH // 2, HEIGHT // 2, 90, "0", final_score_font, RED, win)
new_high_msg = Message(WIDTH // 2, HEIGHT // 2 + 60, 20, "New High", None, GREEN, win)

# Button images
home_img = pygame.image.load('Assets/homeBtn.png')
replay_img = pygame.image.load('Assets/replay.png')
sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/soundOnBtn.png")
easy_img = pygame.image.load("Assets/easy.jpg")
hard_img = pygame.image.load("Assets/hard.jpg")

# Buttons
easy_btn = Button(easy_img, (70, 24), WIDTH // 4 - 10, HEIGHT - 100)
hard_btn = Button(hard_img, (70, 24), WIDTH // 2 + 10, HEIGHT - 100)
home_btn = Button(home_img, (24, 24), WIDTH // 4 - 18, HEIGHT // 2 + 120)
replay_btn = Button(replay_img, (36, 36), WIDTH // 2 - 18, HEIGHT // 2 + 115)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT // 2 + 120)

# Groups **********************************************************************
RADIUS = 70
ball_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

ball = Balls((CENTER[0], CENTER[1] + RADIUS), RADIUS, 90, win)
ball_group.add(ball)
ball = Balls((CENTER[0], CENTER[1] - RADIUS), RADIUS, 270, win)
ball_group.add(ball)

# TIME ************************************************************************
start_time = pygame.time.get_ticks()
current_time = 0
coin_delta = 850
tile_delta = 2000

# VARIABLES *******************************************************************
clicked = False
new_coin = True
num_clicks = 0
score = 0
player_alive = True
highscore = load_highscore()  # Carrega o HighScore do arquivo JSON
sound_on = True
easy_level = True

home_page = True
game_page = False
score_page = False

# LOOP PRINCIPAL **************************************************************
running = True
while running:
    win.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > highscore:
                save_highscore(score)
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_page:
            if not clicked:
                clicked = True
                for ball in ball_group:
                    ball.dtheta *= -1
                    flip_fx.play()

                num_clicks += 1
                if num_clicks % 5 == 0:
                    color_index = (color_index + 1) % len(color_list)
                    color = color_list[color_index]

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

    if home_page:
        connected.update()
        pygame.draw.circle(win, BLACK, CENTER, 80, 20)
        ball_group.update(color)

        if easy_btn.draw(win):
            ball_group.empty()
            ball = Balls((CENTER[0], CENTER[1] + RADIUS), RADIUS, 90, win)
            ball_group.add(ball)
            home_page = False
            game_page = True
            easy_level = True

        if hard_btn.draw(win):
            ball_group.empty()
            ball = Balls((CENTER[0], CENTER[1] + RADIUS), RADIUS, 90, win)
            ball_group.add(ball)
            ball = Balls((CENTER[0], CENTER[1] - RADIUS), RADIUS, 270, win)
            ball_group.add(ball)
            home_page = False
            game_page = True
            easy_level = False

    if score_page:
        game_msg.update()
        over_msg.update()
        final_score.update(score if score else "0", color)
        if score and score >= highscore:
            new_high_msg.update(shadow=False)

        if home_btn.draw(win):
            home_page, score_page, game_page = True, False, False
            player_alive = True
            score = 0
            score_msg.update("0", (150, 150, 150))

        if replay_btn.draw(win):
            home_page, score_page, game_page = False, False, True
            player_alive = True
            score = 0
            score_msg.update("0", (150, 150, 150))

            ball_group.empty()
            ball = Balls((CENTER[0], CENTER[1] + RADIUS), RADIUS, 90, win)
            ball_group.add(ball)
            if not easy_level:
                ball = Balls((CENTER[0], CENTER[1] - RADIUS), RADIUS, 270, win)
                ball_group.add(ball)

        if sound_btn.draw(win):
            sound_on = not sound_on
            sound_btn.update_image(sound_on_img if sound_on else sound_off_img)
            if sound_on:
                pygame.mixer.music.play(loops=-1)
            else:
                pygame.mixer.music.stop()

    if game_page:
        pygame.draw.circle(win, BLACK, CENTER, 80, 20)
        ball_group.update(color)
        coin_group.update(color)
        tile_group.update()
        score_msg.update(score)
        highscore_msg.update(f"Highscore: {highscore}")
        particle_group.update()

        if player_alive:
            for ball in ball_group:
                if pygame.sprite.spritecollide(ball, coin_group, True):
                    score_fx.play()
                    score += 1
                    if score > highscore:
                        highscore = score

                    x, y = ball.rect.center
                    for _ in range(10):
                        particle = Particle(x, y, color, win)
                        particle_group.add(particle)

                if pygame.sprite.spritecollide(ball, tile_group, True):
                    x, y = ball.rect.center
                    for _ in range(30):
                        particle = Particle(x, y, color, win)
                        particle_group.add(particle)
                    player_alive = False
                    dead_fx.play()

            current_time = pygame.time.get_ticks()
            if coin_delta < current_time - start_time < coin_delta + 100 and new_coin:
                y = random.randint(CENTER[1] - RADIUS, CENTER[1] + RADIUS)
                coin = Coins(y, win)
                coin_group.add(coin)
                new_coin = False

            if current_time - start_time >= tile_delta:
                y = random.choice([CENTER[1] - 80, CENTER[1], CENTER[1] + 80])
                tile_type = random.randint(1, 3)
                tile = Tiles(y, tile_type, win)
                tile_group.add(tile)
                start_time = current_time
                new_coin = True

        if not player_alive and len(particle_group) == 0:
            if score > highscore:
                highscore = score
                save_highscore(highscore)

            score_page, game_page = True, False
            score_page_fx.play()
            ball_group.empty()
            tile_group.empty()
            coin_group.empty()

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
