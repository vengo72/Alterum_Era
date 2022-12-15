import pygame
import os


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


class Heroes(pygame.sprite.Sprite):
    def __init__(self, name, damage, health, power, speed, picture, x, y, *group):
        super().__init__(*group)
        self.name = name
        self.damage = damage
        self.health = health
        self.power = power
        self.speed = speed

        self.image = load_image(picture)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


all_sprites = pygame.sprite.Group()
# создадим спрайт
sprite = pygame.sprite.Sprite()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 500
    screen = pygame.display.set_mode(size)
    arrow = pygame.sprite.Sprite(all_sprites)
    warrior = Heroes('warrior', 10, 30, 0, 3, 'warrior.png', 0, 0)
    screen.fill(pygame.Color("white"))
    all_sprites = pygame.sprite.Group()
    all_sprites.add(warrior)
    running = True
    flag = False
    f = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                f = event.pos
                flag = True
        if flag:
            if f[0] > warrior.rect.x:
                warrior.rect.x += 1
                all_sprites = pygame.sprite.Group()
                all_sprites.add(warrior)
            if f[1] > warrior.rect.y:
                warrior.rect.y += 1
                all_sprites = pygame.sprite.Group()
                all_sprites.add(warrior)
            if f[0] < warrior.rect.x:
                warrior.rect.x -= 1
                all_sprites = pygame.sprite.Group()
                all_sprites.add(warrior)
            if f[1] < warrior.rect.y:
                warrior.rect.y -= 1
                all_sprites = pygame.sprite.Group()
                all_sprites.add(warrior)
            if warrior.rect.y == f[1] and warrior.rect.x == f[0]:
                flag = False
        screen.fill(pygame.Color("white"))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
