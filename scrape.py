#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

from theatre import Theatre

amc_url = 'https://www.amctheatres.com/'

markets  = []

theatres = []
dolby    = []
laser    = []

def main():
  # start of markets
  # request and parse movie-theatres url
  movie_theatres_url = amc_url + 'movie-theatres'
  movie_theater_request = requests.get(movie_theatres_url)
  movie_theatres = BeautifulSoup(movie_theater_request.text, 'html.parser')
  # print(movie_theatres.prettify())

  # pull out all the markets
  markets = movie_theatres.find_all('a', class_="Link Link--arrow Link--reversed Link--arrow--txt--tiny txt--tiny")[1:]
  print(len(markets))

  # go through each theater in market
  for market in markets:
    
    market_string = market['href']
    print(market_string)
    
    market_url = amc_url + market_string
    market_request = requests.get(market_url)

    market = BeautifulSoup(market_request.text, 'html.parser')

    scrape_market(market)

  # end of markets

def scrape_market(market):

  market_theatres = []
  market_dolby    = []
  market_laser    = []

  # Loop through theaaters in the market, append to theater lists
  for theatre in market.find_all('li', class_="PanelList-li"):
    theatre = Theatre(theatre)
    market_theatres.append(theatre)
    if theatre.dolby:
      market_dolby.append(theatre)
    if theatre.laser:
      market_laser.append(theatre)
  print("Theaters: {0}".format(len(market_theatres)))
  print("Dolby: {0}".format(len(market_dolby)))
  for item in market_dolby:
    print(item.address())
  print("Laser: {0}".format(len(market_laser)))
  for item in market_laser:
    print(item.address())

  # append market lists to global lists
  global theatres
  global dolby
  global laser

  theatres.extend(market_theatres)
  dolby.extend(market_dolby)
  laser.extend(market_laser)
  
  print("Total Theaters: {0}".format(len(theatres)))
  print("Total Dolby: {0}".format(len(dolby)))
  print("Total Laser: {0}".format(len(laser)))


# maps_api_key = ''
# with open('maps-api-key') as f:
#   maps_api_key = '&key=' + f.read()

# # docs https://developers.google.com/maps/documentation/geocoding/overview
# maps_geocode = 'https://maps.googleapis.com/maps/api/geocode/json?'
# maps_address = 'address=' + dolby[0].address_url()
# print(maps_geocode + maps_address + maps_api_key)
# # maps_request = requests.get(maps_geocode + maps_address + maps_api_key) commented out beacuse api costs $$$

# print(maps_request.text)


if __name__ == "__main__":
  main()