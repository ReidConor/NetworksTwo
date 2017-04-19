import csv
import networkx as nx
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


filename = 'Data3.csv'

G = nx.Graph()
countries, GDPs, lats, lons = [], [], [], []
pos = {}

# Make this plot larger.
plt.figure(figsize=(13,9))
 
with open(filename) as f:
    # Create a csv reader object.
    reader = csv.reader(f)
    
    # Store the latitudes and longitudes in the appropriate lists.
    i = 0
    for row in reader:
        countries.append(row[0])
        lats.append(float(row[2]))
        lons.append(float(row[3]))
        GDPs.append(float(row[4]))
        i = i + 1
    
m = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
              lat_0=0, lon_0=0)

m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color = 'gray')
m.drawmapboundary()
m.drawmeridians(np.arange(0, 360, 30))
m.drawparallels(np.arange(-90, 90, 30))

for country, lon, lat, GDP in zip(countries, lons, lats, GDPs):
    G.add_node(country)
    x,y = m(lon, lat)
    msize = GDP
    pos[country] = (x,y)
    #m.plot(x, y, 'yo', markersize=msize)
    
nx.draw_networkx(G,pos,node_size=100,node_color='yellow')

#plt.show()