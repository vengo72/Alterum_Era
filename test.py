import os
import random

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


size = width, height = 500, 500
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


class Creature(pygame.sprite.Sprite):
    image = load_image("warrior.png")

    def __init__(self, x, y, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Creature.image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


creature = Creature(10, 10)
all_sprites.add(creature)

running = True
flag = False
f = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            f = event.pos
            flag = True
    if flag:
        if f[0] > creature.rect.x:
            creature.rect.x += 1
            all_sprites = pygame.sprite.Group()
            all_sprites.add(creature)
        if f[1] > creature.rect.y:
            creature.rect.y += 1
            all_sprites = pygame.sprite.Group()
            all_sprites.add(creature)
        if f[0] < creature.rect.x:
            creature.rect.x -= 1
            all_sprites = pygame.sprite.Group()
            all_sprites.add(creature)
        if f[1] < creature.rect.y:
            creature.rect.y -= 1
            all_sprites = pygame.sprite.Group()
            all_sprites.add(creature)
        if creature.rect.y == f[1] and creature.rect.x == f[0]:
            flag = False
    screen.fill(pygame.Color("white"))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()



