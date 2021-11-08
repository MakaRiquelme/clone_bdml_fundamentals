
import csv
import requests
import io
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Classes to hold the data
class EarthQuake:
  def __init__(self, row):
    # Parse earthquake data from USGS
    self.timestamp = row[0]
    self.lat = float(row[1])
    self.lon = float(row[2])
    try:
      self.magnitude = float(row[4])
    except ValueError:
      self.magnitude = 0
    
def get_earthquake_data(url):
  # Read CSV earthquake data from USGS
  response = requests.get(url)
  csvio = io.StringIO(response.text)
  reader = csv.reader(csvio)
  header = next(reader)
  quakes = [EarthQuake(row) for row in reader]
  quakes = [q for q in quakes if q.magnitude > 0]
  return quakes


# control marker color and size based on magnitude
def get_marker(magnitude):
    markersize = magnitude * 2.5;
    if magnitude < 1.0:
        return ('bo'), markersize
    if magnitude < 3.0:
        return ('go'), markersize
    elif magnitude < 5.0:
        return ('yo'), markersize
    else:
        return ('ro'), markersize


def create_png(url, outfile): 
  quakes = get_earthquake_data(url)
  print(quakes[0].__dict__)

  # Set up Basemap
  mpl.rcParams['figure.figsize'] = '16, 12'
  m = Basemap(projection='kav7', lon_0=-90, resolution = 'l', area_thresh = 1000.0)
  m.drawcoastlines()
  m.drawcountries()
  m.drawmapboundary(fill_color='0.3')
  m.drawparallels(np.arange(-90.,99.,30.))
  junk = m.drawmeridians(np.arange(-180.,180.,60.))

  # sort earthquakes by magnitude so that weaker earthquakes
  # are plotted after (i.e. on top of) stronger ones
  # the stronger quakes have bigger circles, so we'll see both
  start_day = quakes[-1].timestamp[:10]
  end_day = quakes[0].timestamp[:10]
  quakes.sort(key=lambda q: q.magnitude, reverse=True)

  # add earthquake info to the plot
  for q in quakes:
    x,y = m(q.lon, q.lat)
    mcolor, msize = get_marker(q.magnitude)
    m.plot(x, y, mcolor, markersize=msize)

  # add a title
  plt.title("Earthquakes {0} to {1}".format(start_day, end_day))
  plt.savefig(outfile)

if __name__ == '__main__':
  url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.csv'
  outfile = 'earthquakes.png'
  create_png(url, outfile)
