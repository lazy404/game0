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

font_preferences = ["Impact", "Helvetica"]

pygame.mixer.init()
sounds={}
default_sound=pygame.mixer.Sound('sounds/a.wav')

font_size=mode[1]/3
text = create_text("Julek", font_preferences, font_size, (180, 128, 0))

cur_klawisz='?'

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            else:
                klawisz=chr(event.key).upper()
                if klawisz.isalpha():
                    text = create_text(chr(event.key).upper(), font_preferences, font_size, (180, 128, 0))
                    cur_sound=sounds.get(klawisz, default_sound)
                    c=cur_sound.play()
                    cur_klawisz=klawisz
    
    screen.fill((255, 255, 255))
    screen.blit(text, (mode[0]/2 - text.get_width() // 2, mode[1]/2 - text.get_height() // 2))
    
    pygame.display.flip()
    clock.tick(60)