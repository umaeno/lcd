import pygame, sys, os, time, datetime, io, json, schedule
from pygame.locals import *
from collections import OrderedDict
try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

os.environ["SDL_FBDEV"] = "/dev/fb0"
pygame.init()

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


def url_builder(city_id, apitype):
    user_api = '814fcbef78be15dcc4bd405afec6914f'
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/' + apitype
    full_api_url = '?id=' + api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url


def data_fetch(full_api_url):
    #url = urllib.request.urlopen(full_api_url)
    url = urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output, object_pairs_hook=OrderedDict)
    url.close()
    return raw_api_dict


def data_organizer(raw_api_dict):
    data = dict(
        

def data_organizer2(raw_api_dict):
    data2 = dict(
        temp_min = raw_api_dict['list'][0]['main']['temp_min'],
        temp_max = raw_api_dict['list'][0]['main']['temp_max'],
        weather = raw_api_dict['list'][0]['weather'][0]['description'],
        icon = raw_api_dict['list'][0]['weather'][0]['icon'],
        temp_min2 = raw_api_dict['list'][1]['main']['temp_min'],
        temp_max2 = raw_api_dict['list'][1]['main']['temp_max'],
        weather2 = raw_api_dict['list'][1]['weather'][0]['description'],
        icon2 = raw_api_dict['list'][1]['weather'][0]['icon']
    )
    return data


def data_update():
    global data
    print('data update')
    currenttime = datetime.datetime.time(datetime.datetime.now())
    str_time = currenttime.strftime("%I:%M:%S %p")
    f = open('log.txt', 'a')
    f.write(str_time + "\n")
    f.close()
    data = data_organizer(data_fetch(url_builder(cityid, 'weather')))
    data2 = data_organizer2(data_fetch(url_builder(cityid, 'forecast')))


# First fetch
cityid = 2172517  # Canberra AU    
data = data_organizer(data_fetch(url_builder(cityid)))


# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
CYAN  = (  0, 255, 255)

# set up the window
screen = pygame.display.set_mode((160, 128), 0, 32)
pygame.mouse.set_visible(0)

print('scheduling')
schedule.every(30).minutes.do(data_update)
#schedule.every().minute.do(data_update)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # fill screen
    screen.fill(BLACK)

    # show today
    smallfont = pygame.font.SysFont(None, 14)
    text = smallfont.render('Today', True, WHITE)
    textpos = text.get_rect(centerx=screen.get_width()/4)
    screen.blit(text, textpos)

    # show today's icon
    img_url = "http://openweathermap.org/img/w/" + data['icon'] + ".png"
    img_str = urlopen(img_url).read()
    img_file = io.BytesIO(img_str)
    img = pygame.image.load(img_file)
    imgpos = img.get_rect(centerx=screen.get_width()/4,centery=30)
    screen.blit(img, imgpos)
    
    # show today's weather
    text = smallfont.render(data['weather'], True, (100, 200, 100))
    textpos = text.get_rect(centerx=screen.get_width()/4,centery=50)
    screen.blit(text, textpos)

    # show today's temperture
    tempfont = pygame.font.SysFont(None, 28)
    text = tempfont.render('/', True, WHITE)
    textpos = text.get_rect(centerx=screen.get_width()/4,centery=70)
    screen.blit(text, textpos)
    
    text = tempfont.render('{:.1f}'.format(data['temp_max']), True, RED)
    textpos = text.get_rect(centerx=screen.get_width()/4-20,centery=70)
    screen.blit(text, textpos)

    text = tempfont.render('{:.1f}'.format(data['temp_min']), True, BLUE)
    textpos = text.get_rect(centerx=screen.get_width()/4+20,centery=70)
    screen.blit(text, textpos)

    # Draw Lines
    pygame.draw.line(screen, GREEN, [screen.get_width()/2, 5], [screen.get_width()/2, 80], 1)

    # show date
    currenttime = datetime.datetime.time(datetime.datetime.now())
    font = pygame.font.SysFont(None, 20)
    text = font.render(currenttime.strftime("%m/%d"), 1, CYAN)
    textpos = text.get_rect(centery=100)
    screen.blit(text, textpos)

    text = font.render(currenttime.strftime("%a"), 1, CYAN)
    textpos = text.get_rect(bottomleft=(10, screen.get_height()))
    screen.blit(text, textpos)
    
    # show current time
    largefont = pygame.font.SysFont(None, 54)
    currenttime = datetime.datetime.time(datetime.datetime.now())
    text = largefont.render(currenttime.strftime("%H:%M"), 1, CYAN)
    textpos = text.get_rect(bottomright=(screen.get_width()-10,screen.get_height()))
    screen.blit(text, textpos)

    print('display updating')
    pygame.display.update()

    schedule.run_pending()
    time.sleep(60)
