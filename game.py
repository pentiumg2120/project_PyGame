import json
import os
import random
import sys
from pathlib import Path

import pygame

import generator_json


class image(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1024, 1024))
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


pygame.mixer.init()
pygame.init()
screen_size = (1920, 1000)
screen = pygame.display.set_mode(screen_size)
FPS = 50

eating_items = []
not_eating_items = []


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


running = True
clock = pygame.time.Clock()
picture_sprites = pygame.sprite.Group()

good_answer = None
score = 0


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image(Path('zastavka/zastavka.png')), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def rule_screen():
    fon = pygame.transform.scale(load_image(Path("rule/rule.png")), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    global score
    pygame.mixer.music.load(Path("data/end_game/barinov.mp3"))
    pygame.mixer.music.play()
    intro_text = ["Лол, кек", f"Кстати ваш счет:{score}",
                  "Всем удачи",
                  "Всем пока!"]

    fon = pygame.transform.scale(load_image(Path("./end_game/barinov.jpg")), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 85)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(3, 234, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_json():
    global eating_items
    global not_eating_items

    eating_items = json.loads(Path("data/eat_json.txt").read_text(encoding="UTF-8"))
    for i in eating_items:
        i["path"] = Path(i["path"])

    not_eating_items = json.loads(Path("data/not_eat_json.txt").read_text(encoding="UTF-8"))
    for i in not_eating_items:
        i["path"] = Path(i["path"])


def generate_level():
    global good_answer
    global first_picture, second_picture
    good_picture_path = Path(random.choice(eating_items)["path"])
    good_picture = load_image(good_picture_path)

    bad_picture_path = Path(random.choice(not_eating_items)["path"])
    bad_picture = load_image(bad_picture_path)

    first_picture = random.choice((bad_picture, good_picture))
    if first_picture == good_picture:
        good_answer = 1
        second_picture = bad_picture
    else:
        good_answer = 2
        second_picture = good_picture
    return [first_picture, second_picture]


def level():
    global picture_sprites
    first_picture, second_picture = generate_level()
    picture_sprites = pygame.sprite.Group()
    first_picture_sprite = image(first_picture, (500, 500))
    second_picture_sprite = image(second_picture, (1500, 500))
    picture_sprites.add(first_picture_sprite)
    picture_sprites.add(second_picture_sprite)


def check_answer(answer):
    global good_answer
    global score
    if answer == good_answer:
        score += 10
    else:
        score -= 10
    level()


generator_json.__main__()
load_json()
start_screen()
rule_screen()
level()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                check_answer(1)
            elif event.key == pygame.K_2:
                check_answer(2)
            elif event.key == pygame.K_9:
                level()
            elif event.key == pygame.K_4:
                end_screen()
                terminate()

    picture_sprites.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
