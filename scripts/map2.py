import csv
import networkx as nx
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import random


filename = 'Data.csv'

G = nx.Graph()
countries, lats, lons, pops, color_map = [], [], [], [], []
pos = {}

attack_colors = ['red','blue','green']

# Make plot larger.
plt.figure(figsize=(15,9))
 
with open(filename) as f:
    # Create a csv reader object.
    reader = csv.reader(f)
    
    # Store the latitudes and longitudes in the appropriate lists.
    for row in reader:
        countries.append(row[0])
        lats.append(float(row[1]))
        lons.append(float(row[2]))
        pops.append(float(row[3]))
    
m = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
              lat_0=0, lon_0=0)

m.drawcoastlines()
m.drawcountries()
#m.fillcontinents(color = 'gray')
m.drawmapboundary()
#m.drawmeridians(np.arange(0, 360, 30))
#m.drawparallels(np.arange(-90, 90, 30))

i = 0
for country, lon, lat, pop in zip(countries, lons, lats, pops):
    G.add_node(country)
    x,y = m(lon, lat)
    pos[country] = (x,y)

    print(country)
    state = 0
    color = 'yellow'
    if i < 3:
        if pop * random.randint(0,1) > 10000:
            state = 1
            color = attack_colors[i]
            i = i + 1
    G.node[country]["state"] = state
    color_map.append(color)
    
#Calculate Distances between countries and add edges
i = 1
for c1, lon1, lat1, pop1 in zip(countries, lons, lats, pops):
    for c2, lon2, lat2, pop2  in zip(countries[i:], lons[i:], lats[i:], pops[i:]):
        dist = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)
        maxPop = max(pop1, pop2)
        score  = np.power(maxPop,(1/4))/dist
        if score > 1:
            G.add_edge(c1, c2, weight = dist)
    i = i + 1
    
nx.draw_networkx(G,pos,node_size=50,node_color = color_map, edge_color = 'purple', with_labels = False)



