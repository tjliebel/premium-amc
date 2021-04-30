import urllib.parse
from bs4 import BeautifulSoup

class Theatre:
  # raw      = raw beautiful soup object
  # name     = name of theatre
  # _address = address of theatre, use address() to get this
  # features = list of premium features

  def __init__(self, soup):
    # soup is a beautiful soup object of a theatre from AMC's site
    
    self.raw  = soup
    self.name = soup.find(class_="TheatreInfo").find(class_="Link-text Headline--h3").text
    self._address = ''

    self.features = []
    for line in soup.find(class_="u-listUnstyled u-separatedList Headline--eyebrow--alt txt--gray--light").find_all('li'):
      self.features.append(line.text)

    self.dolby = "Dolby Cinema" in self.features
    self.laser = "IMAX with Laser at AMC" in self.features

  # this is a function so that it isn't done on EVERY theater as it is built, but only when needed
  def address(self):
    # if address has been built already, return it, else build, set, and return
    if self._address != '':
      return self._address
    else:
      # I know that this is absolutely horendous, but this is what my 2am brain did with the 
      # weirdness of the 2 line address and the extra (unpredictable?) whitespace 
      # and there not being a comma between street and city
      address_raw = self.raw.find(class_="TheatreInfo").find(class_="Link-text txt--thin").text
      address_lines = address_raw.splitlines()
      address_lines[0] = address_lines[0].split()
      address_lines[0][-1] = address_lines[0][-1] + ','
      address_lines[1] = address_lines[1].split()
      self._address = ' '.join(address_lines[0] + address_lines[1])
      return self._address
  
  def address_url(self):
    return urllib.parse.quote_plus(self.address())
      