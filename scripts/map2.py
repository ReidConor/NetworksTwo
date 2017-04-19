import csv
import networkx as nx
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


filename = 'Data.csv'

G = nx.Graph()
countries, lats, lons = [], [], []
pos = {}

# Make this plot larger.
plt.figure(figsize=(15,10))
 
with open(filename) as f:
    # Create a csv reader object.
    reader = csv.reader(f)
    
    # Store the latitudes and longitudes in the appropriate lists.
    i = 0
    for row in reader:
        countries.append(row[0])
        lats.append(float(row[1]))
        lons.append(float(row[2]))
        i = i + 1
    
m = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
              lat_0=0, lon_0=0)

m.drawcoastlines()
m.drawcountries()
#m.fillcontinents(color = 'gray')
m.drawmapboundary()
#m.drawmeridians(np.arange(0, 360, 30))
#m.drawparallels(np.arange(-90, 90, 30))

for country, lon, lat, in zip(countries, lons, lats):
    G.add_node(country)
    x,y = m(lon, lat)
    pos[country] = (x,y)
    #m.plot(x, y, 'yo', markersize=msize)
    
#Calculate Distances between countries and add edges
i = 1
for c1, lon1, lat1, in zip(countries, lons, lats):
    for c2, lon2, lat2, in zip(countries[i:], lons[i:], lats[i:]):
        dist = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)
        if dist < 10:
            G.add_edge(c1, c2, weight = dist)
    i = i + 1
    
nx.draw_networkx(G,pos,node_size=50,node_color='yellow',edge_color = 'red',with_labels = False)

#plt.show()