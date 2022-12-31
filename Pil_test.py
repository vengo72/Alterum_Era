import os
import pygame
from PIL import Image, ImageDraw


def unit_icon(icon_name, color):
    image = Image.open('data/' + icon_name).convert('RGBA')
    new_image = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(new_image)
    draw.ellipse((8, 8, 240, 240), fill=color)
    new_image.paste(image, (0, 0), image)
    new_image.save(f'data/{icon_name.split(".")[0]}_{color}.png')


if __name__ == '__main__':
    print('start')
    unit_icon('warrior.png', 'blue')
