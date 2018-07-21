import pygame, sys, os, time, datetime, io, json, schedule
from pygame.locals import *
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


def url_builder(city_id):
    user_api = '814fcbef78be15dcc4bd405afec6914f'
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/weather?id='     # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
    full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url


def data_fetch(full_api_url):
    #url = urllib.request.urlopen(full_api_url)
    url = urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict


def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        sky_desc=raw_api_dict['weather'][0]['description'],
        icon=raw_api_dict['weather'][0]['icon'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=raw_api_dict.get('deg'),
        dt=time_converter(raw_api_dict.get('dt')),
        cloudiness=raw_api_dict.get('clouds').get('all')
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
    data = data_organizer(data_fetch(url_builder(cityid)))


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
            
    # show weather description
    basicfont = pygame.font.SysFont(None, 18)
    text = basicfont.render(data['sky_desc'], True, (100, 200, 100))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery
    screen.blit(text, textrect)

    # show icon
    img_url = "http://openweathermap.org/img/w/" + data['icon'] + ".png"
    img_str = urlopen(img_url).read()
    img_file = io.BytesIO(img_str)
    img = pygame.image.load(img_file)
    screen.blit(img, (20, 20))

    # show current time
    currenttime = datetime.datetime.time(datetime.datetime.now())
    text = basicfont.render(currenttime.strftime("%I:%M %p"), 1, CYAN)
    textpos = text.get_rect(center=(screen.get_width()/2,80))
    screen.blit(text, textpos)

    print('display updating')
    pygame.display.update()

    schedule.run_pending()
    time.sleep(60)
