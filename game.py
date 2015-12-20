#!/usr/bin/env python
#
# Gierka Julka i Taty

import pygame

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)

_cached_fonts = {}
def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

_cached_text = {}
def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image == None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image

pygame.init()
mode=pygame.display.list_modes()[0]
screen = pygame.display.set_mode(mode, pygame.FULLSCREEN)
clock = pygame.time.Clock()
done = False

font_preferences = ["Comic Sans MS", "Impact", "Helvetica"]

pygame.mixer.init()

sounds={}
import glob, random

default_sound=pygame.mixer.Sound('sounds/default.wav')
julek_sound=pygame.mixer.Sound('sounds/julek.wav')
nie=pygame.mixer.Sound('sounds/nie.wav')

for i in glob.glob('sounds/?.wav'):
    print 'Loading', i
    sounds[i[7:8].upper()]=pygame.mixer.Sound(i)

font_size=mode[1]/2
text = create_text("Julek", font_preferences, font_size, (254, 216, 1))

cur_klawisz='?'
julek_sound.play()
global fill
fill=(31, 102, 224)
c=None

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            else:
                if event.key > 128:
                    continue
                klawisz=chr(event.key).upper()
                if klawisz.isalpha() and ( c == None or not c.get_busy()):
                    text = create_text(chr(event.key).upper(), font_preferences, font_size, (254, 216, 1))
                    cur_sound=sounds.get(klawisz, default_sound)
                    c=cur_sound.play()
                    cur_klawisz=klawisz
                    fill=(random.randrange(1,255), random.randrange(1,255),random.randrange(1,255))
    screen.fill(fill)
    screen.blit(text, (mode[0]/2 - text.get_width() // 2, mode[1]/2 - text.get_height() // 2))
    
    pygame.display.flip()
    clock.tick(60)