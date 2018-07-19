import pygame, sys, os, time, datetime, io
from pygame.locals import *
try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

os.environ["SDL_FBDEV"] = "/dev/fb0"
pygame.init()

def inverted(img):
   inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
   inv.fill((255,255,255,255))
   inv.blit(img, (0,0), None, BLEND_RGB_SUB)
   return inv

# set up the window
screen = pygame.display.set_mode((160, 128), 0, 32)
pygame.mouse.set_visible(0)
#screen.fill((255, 255, 255))
screen.fill((0, 0, 0))

basicfont = pygame.font.SysFont(None, 18)
text = basicfont.render('Hello World!', True, (100, 200, 100))
textrect = text.get_rect()
textrect.centerx = screen.get_rect().centerx
textrect.centery = screen.get_rect().centery
screen.blit(text, textrect)

img_url = "http://openweathermap.org/img/w/04n.png"
img_str = urlopen(img_url).read()
img_file = io.BytesIO(img_str)
img = pygame.image.load(img_file)
screen.blit(img, (20, 20))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    currenttime = datetime.datetime.time(datetime.datetime.now())

    text = basicfont.render(currenttime.strftime("%I:%M %p"), 1, (0, 0, 0))
    textpos = text.get_rect(center=(screen.get_width()/2,80))
    screen.blit(text, textpos)

    pygame.display.update()

    time.sleep(60)

