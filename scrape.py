#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

from theatre import Theatre

amc_url = 'https://www.amctheatres.com/'

# # start of markets
# # request and parse movie-theatres url
# movie_theatres_url = amc_url + 'movie-theatres'
# movie_theater_request = requests.get(movie_theatres_url)
# movie_theatres = BeautifulSoup(movie_theater_request.text, 'html.parser')
# # print(movie_theatres.prettify())

# # pull out all the markets
# markets = movie_theatres.find_all('a', class_="Link Link--arrow Link--reversed Link--arrow--txt--tiny txt--tiny")[1:]
# print(len(markets))

# # go through each theater in market
# for market in markets[0:1]:
#   print(market['href'])

# # end of markets


market_string = 'movie-theatres/houston'
market_url = amc_url + market_string
market_request = requests.get(market_url)
market = BeautifulSoup(market_request.text, 'html.parser')

theatres = []
dolby    = []
laser    = []

for theatre in market.find_all('li', class_="PanelList-li"):
  theatre = Theatre(theatre)
  theatres.append(theatre)
  print(len(theatres))
  if theatre.dolby:
    dolby.append(theatre)
  if theatre.laser:
    laser.append(theatre)
print(len(dolby))
print(len(laser))
print(dolby[0].address())


maps_api_key = ''
with open('maps-api-key') as f:
  maps_api_key = '&key=' + f.read()

# docs https://developers.google.com/maps/documentation/geocoding/overview
maps_geocode = 'https://maps.googleapis.com/maps/api/geocode/json?'
maps_address = 'address=' + dolby[0].address_url()
print(maps_geocode + maps_address + maps_api_key)
# maps_request = requests.get(maps_geocode + maps_address + maps_api_key) commented out beacuse api costs $$$

print(maps_request.text)