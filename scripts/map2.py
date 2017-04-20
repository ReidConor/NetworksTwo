import csv
import networkx as nx
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import random


def genGraph():

    filename = '../data/Data.csv'

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
    return G, pos

def plotGraph(Graph, pos):

    colors= []

    for u in G.nodes():
        if G.node[u]["state"] == 0:
            colors.append("white")
        else:
            colors.append(G.node[u]["state"])

    nx.draw_networkx(G,pos,node_size=50,node_color=colors,edge_color = 'red',with_labels = False)

    plt.show()

def infection_init(G):
    """Make a graph with some infected nodes."""
    for u in G.nodes():
        G.node[u]["state"] = 0
    init = random.sample(G.nodes(), i)
    teams = ["red","green","blue"]
    for u in init:
        G.node[u]["state"] = teams.pop() 
        # random.choice(teams)

def step(G):
    """Given a graph G, run one time-step."""
    new_state = {}
    for u, d in G.nodes(data=True):
        for u2 in G.neighbors(u):
            G.node[u]["state"] = infection_update(d["state"], G.node[u2]["state"])
        # break

def infection_update(s1, ss):
    """Update the state of node s1, given the states of its neighbours ss."""

    # print(s1, ss)
    # print("---------")

    if ss == 0: #that country hasnt been taken over
        return s1
    else:
        if random.random() > p:
            return s1
        else:
            return ss


if __name__ == "__main__":
    G, pos = genGraph()

    print("Number of nodes: ",len(G.nodes()))
    print("Number of edges: ", len(G.edges()))

    #set up params we need
    n = len(G.nodes()) # number of nodes
    # pn = 0.1 # per-edge probability of existing
    p = 0.5 # probability of acquiring infection from a single neighbour, per time-step
    i = 3 # number of nodes initially infected
    # td = 10 # td time-steps after infection, the individual dies
    nsteps = 2 # how many time-steps to run

    infection_init(G)

    for i in range(nsteps):
        step(G)

    plotGraph(G, pos)
