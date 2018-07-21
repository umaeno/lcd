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


def url_builder(city_id):
    base_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + str(city_id)
    user_api = 'CQ6HIyCflFefGhCCw5CzKjNXdGzTlhL6'
    unit = 'metric=true'
    full_api_url = base_url + '?apikey=' + user_api + '&' + unit
    return full_api_url


def data_fetch(full_api_url):
    url = urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output, object_pairs_hook=OrderedDict)
    url.close()
    return raw_api_dict


def data_organizer(raw_api_dict):
    data = dict(
        temp_min = raw_api_dict['DailyForecasts'][0]['Temperature']['Minimum']['Value'],
        temp_max = raw_api_dict['DailyForecasts'][0]['Temperature']['Maximum']['Value'],
        dayweather = raw_api_dict['DailyForecasts'][0]['Day']['IconPhrase'],
        nightweather = raw_api_dict['DailyForecasts'][0]['Night']['IconPhrase'],
        dayicon = raw_api_dict['DailyForecasts'][0]['Day']['Icon'],
        nighticon = raw_api_dict['DailyForecasts'][0]['Night']['Icon'],
        temp_min2 = raw_api_dict['DailyForecasts'][1]['Temperature']['Minimum']['Value'],
        temp_max2 = raw_api_dict['DailyForecasts'][1]['Temperature']['Maximum']['Value'],
        dayweather2 = raw_api_dict['DailyForecasts'][1]['Day']['IconPhrase'],
        nightweather2 = raw_api_dict['DailyForecasts'][1]['Night']['IconPhrase'],
        dayicon2 = raw_api_dict['DailyForecasts'][1]['Day']['Icon'],
        nighticon2 = raw_api_dict['DailyForecasts'][1]['Night']['Icon']
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
cityid = 21921  # Canberra AU    
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
schedule.every().day.at("7:00").do(data_update)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # fill screen
    screen.fill(BLACK)

    ## show today
    smallfont = pygame.font.SysFont(None, 14)
    text = smallfont.render('Today', True, WHITE)
    textpos = text.get_rect(centerx=screen.get_width()/4)
    screen.blit(text, textpos)

    # show today's icon
    img_url = "http://apidev.accuweather.com/developers/Media/Default/WeatherIcons/" + "{:02d}".format(data['dayicon']) + "-s.png"
    img_str = urlopen(img_url).read()
    img_file = io.BytesIO(img_str)
    img = pygame.image.load(img_file)
    img = pygame.transform.smoothscale(img, (60, 36))
    imgpos = img.get_rect(centerx=screen.get_width()/8,centery=30)
    screen.blit(img, imgpos)

    pygame.draw.line(screen, WHITE, [screen.get_width()/4 + 5, text.get_height() + 5], [screen.get_width()/4 - 5, text.get_height() + img.get_height() - 5], 1)
    
    img_url = "http://apidev.accuweather.com/developers/Media/Default/WeatherIcons/" + "{:02d}".format(data['nighticon']) + "-s.png"
    img_str = urlopen(img_url).read()
    img_file = io.BytesIO(img_str)
    img = pygame.image.load(img_file)
    img = pygame.transform.smoothscale(img, (60, 36))
    imgpos = img.get_rect(centerx=screen.get_width()*3/8,centery=30)
    screen.blit(img, imgpos)
    
    # show today's weather
    text = smallfont.render(data['dayweather'], True, (100, 200, 100))
    textpos = text.get_rect(centerx=screen.get_width()/4,centery=50)
    screen.blit(text, textpos)

    # show today's temperture
    tempfont = pygame.font.SysFont(None, 26)
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

    ## show tomorrow
    text = smallfont.render('Tomorrow', True, WHITE)
    textpos = text.get_rect(centerx=screen.get_width()*3/4)
    screen.blit(text, textpos)

    # show tomorrow's icon
    img_url = "http://apidev.accuweather.com/developers/Media/Default/WeatherIcons/" + "{:02d}".format(data['dayicon2']) + "-s.png"
    img_str = urlopen(img_url).read()
    img_file = io.BytesIO(img_str)
    img = pygame.image.load(img_file)
    img = pygame.transform.smoothscale(img, (60, 36))
    imgpos = img.get_rect(centerx=screen.get_width()*5/8,centery=30)
    screen.blit(img, imgpos)

    pygame.draw.line(screen, WHITE, [screen.get_width()*3/4 + 5, text.get_height() + 5], [screen.get_width()*3/4 - 5, text.get_height() + img.get_height() - 5], 1)
    
    img_url = "http://apidev.accuweather.com/developers/Media/Default/WeatherIcons/" + "{:02d}".format(data['nighticon2']) + "-s.png"
    img_str = urlopen(img_url).read()
    img_file = io.BytesIO(img_str)
    img = pygame.image.load(img_file)
    img = pygame.transform.smoothscale(img, (60, 36))
    imgpos = img.get_rect(centerx=screen.get_width()*7/8,centery=30)
    screen.blit(img, imgpos)
    
    # show tomorrow's weather
    text = smallfont.render(data['dayweather2'], True, (100, 200, 100))
    textpos = text.get_rect(centerx=screen.get_width()*3/4,centery=50)
    screen.blit(text, textpos)

    # show tomorrow's temperture
    text = tempfont.render('/', True, WHITE)
    textpos = text.get_rect(centerx=screen.get_width()*3/4,centery=70)
    screen.blit(text, textpos)
    
    text = tempfont.render('{:.1f}'.format(data['temp_max2']), True, RED)
    textpos = text.get_rect(centerx=screen.get_width()*3/4-20,centery=70)
    screen.blit(text, textpos)

    text = tempfont.render('{:.1f}'.format(data['temp_min2']), True, BLUE)
    textpos = text.get_rect(centerx=screen.get_width()*3/4+20,centery=70)
    screen.blit(text, textpos)

    
    # show date
    currentday = datetime.datetime.now()
    font = pygame.font.SysFont(None, 20)
    text = font.render(currentday.strftime("%m/%d"), 1, CYAN)
    textpos = text.get_rect(left=10,centery=100)
    screen.blit(text, textpos)

    text = font.render(currentday.strftime("%a"), 1, CYAN)
    textpos = text.get_rect(bottomleft=(20, screen.get_height()-5))
    screen.blit(text, textpos)
    
    # show current time
    largefont = pygame.font.SysFont(None, 54)
    currenttime = datetime.datetime.time(datetime.datetime.now())
    text = largefont.render(currenttime.strftime("%H:%M"), 1, CYAN)
    textpos = text.get_rect(bottomright=(screen.get_width()-20,screen.get_height()))
    screen.blit(text, textpos)

    print('display updating')
    pygame.display.update()

    schedule.run_pending()
    time.sleep(60)
