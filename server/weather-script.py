#!/usr/bin/python2

# Kindle Weather Display
# Matthew Petroff (http://www.mpetroff.net/)
# September 2012

import urllib2
from xml.dom import minidom
import datetime
import codecs


city = 'Stockholm'

#
# Download and parse weather data
#

# Fetch data (change lat and lon to desired location)
weather_xml = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city +'&mode=xml&units=metric&cnt=7').read()
dom = minidom.parseString(weather_xml)


# Parse data
forecast = dom.getElementsByTagName('time')
highs = [None]*4
lows = [None]*4
icons = [None]*4
for i in range(4):
    temperature = forecast[i].getElementsByTagName('temperature')
    highs[i] = int(round(float(temperature[0].getAttribute('max'))))
    lows[i] = int(round(float(temperature[0].getAttribute('min'))))
    symbol = forecast[i].getElementsByTagName('symbol')
    if symbol[0].getAttribute('var') == '01d':
        #Sun
        icons[i] = 'skc'
    elif symbol[0].getAttribute('var') == '02d':
        icons[i] = 'few' #sun with clouds
        # few clouds
        icons[i] = 'sct'
    elif symbol[0].getAttribute('var') == '03d':
        #scattered clouds
        icons[i] = 'bkn'
    elif symbol[0].getAttribute('var') == '04d':
        #broken clouds
        icons[i] = 'ovc'
    elif symbol[0].getAttribute('var') == '09d':
        #shower rain
        icons[i] = 'ra'
    elif symbol[0].getAttribute('var') == '10d':
        #rain
        if symbol[0].getAttribute('number') == '500':
            icons[i] = 'hi_shwrs'
        else:
            icons[i] = 'shra'
    elif symbol[0].getAttribute('var') == '11d':
        if symbol[0].getAttribute('number') == '210':
            #light thunderstorm
            icons[i] = 'scttsra'
        else:
            #thunderstorm
            icons[i] = 'tsra'
    elif symbol[0].getAttribute('var') == '13d':
        if symbol[0].getAttribute('number') == '511':
            #rain and snow and cold
            icons[i] = 'mix'
        else:
            #snow
            icons[i] = 'sn'
    elif symbol[0].getAttribute('var') == '50d':
        #mist
        icons[i] = 'fg'
    else:
        #blizzard
        icons[i] = 'blizzard'
        #blizzard
        icons[i] = 'cold'
        #drought
        icons[i] = 'du'
        #
        icons[i] = 'sctfg'
        #
        icons[i] = 'fg'
        #burning
        icons[i] = 'fu'
        #rain and cold
        icons[i] = 'fzra'
        #hot
        icons[i] = 'hot'
        #hail
        icons[i] = 'ip'
        #rain and snow
        icons[i] = 'rasn'
        #rain and hail
        icons[i] = 'raip'
        #wind
        icons[i] = 'wind'

# Parse dates
xml_day_one = dom.getElementsByTagName('time')[0].getAttribute('day')
day_one = datetime.datetime.strptime(xml_day_one, '%Y-%m-%d')


#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()

# Insert icons and temperatures
output = output.replace('ICON_ONE',icons[0]).replace('ICON_TWO',icons[1]).replace('ICON_THREE',icons[2]).replace('ICON_FOUR',icons[3])
output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
output = output.replace('DAY_THREE',days_of_week[(day_one + 2*one_day).weekday()]).replace('DAY_FOUR',days_of_week[(day_one + 3*one_day).weekday()])

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)
