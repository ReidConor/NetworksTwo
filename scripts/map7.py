import csv
import networkx as nx
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import random
import math

countries, lats, lons, pops, GDPs = [], [], [], [], []
pos = {}
filename = '../data/Data.csv'

colors, sizes = [], []

empire_pops = [0, 0, 0, 0]


def importData():

    with open(filename) as f:
        # Create a csv reader object.
        reader = csv.reader(f)

        # Store the latitudes and longitudes in the appropriate lists.
        for row in reader:
            countries.append(row[0])
            lats.append(float(row[1]))
            lons.append(float(row[2]))
            pops.append(float(row[3]))
            GDPs.append(float(row[4]))

def genGraph():

    G = nx.Graph()

    #Add nodes & calculate distances between countries and add edges
    i = 1
    for c1, lon1, lat1, pop1, g in zip(countries, lons, lats, pops, GDPs):
        G.add_node(c1, pop = pop1, GDP = g)
        for c2, lon2, lat2, pop2  in zip(countries[i:], lons[i:], lats[i:], pops[i:]):
            dist = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)
            maxPop = max(pop1, pop2)
            score  = np.power(maxPop,(1/4))/dist
            if score > 1:
                G.add_edge(c1, c2, weight = dist)
        i = i + 1

    G.add_edge("United States", "Ireland")
    G.add_edge("Canada", "Ireland")
    G.add_edge("Portugal","United States")
    G.add_edge("United States","Morocco")
    return G

def war_init(G,pos):
    """Set countries to attack"""
    teams = ["red","yellow","blue"]
    # teams = ["red"]
    i = 1
    for u in G.nodes():
        state = "white"
        size = 50
        emp = 0
        if teams and G.node[u]["pop"] * random.randint(0,1) > 100000:
            state = teams.pop()
            print(len(G.neighbors(u)))
            size = 150
            emp = i
            i = i + 1
            print(u)
        G.node[u]["state"] = state
        G.node[u]["size"] = size
        G.node[u]["empire"] = emp
    #plotGraph(G)

def findP(pop1, pop2):

    # if ss == "white":
    #     return 1

    # redPop = 0
    # bluePop = 0
    # yellowPop = 0
    # for i in G.nodes():
    #     if G.node[i]["state"] == "red":
    #         redPop += G.node[i]["pop"]
    #     if G.node[i]["state"] == "yellow":
    #         bluePop += G.node[i]["pop"]
    #     if G.node[i]["state"] == "blue":
    #         yellowPop += G.node[i]["pop"]
    #
    # popDict = {"red":redPop, "blue":bluePop, "yellow":yellowPop}
    # popDiff = popDict[s1] - popDict[ss]
    # # print (popDiff)
    # # print(s1, ss)

    if pop1 > pop2:
        return 0.1
    else:
        return 0.5

def step(G):
    """Given a graph G, run one time-step."""
    # winCount = 0
    myList = []
    for u, d in G.nodes(data=True):
        for v in G.neighbors(u):
            # print(v)
            if G.node[u]["state"] in myList:
                continue
            else:
                state, won = war_update(u,v)
                G.node[v]["state"] = state

                if won == "yes":
                    myList.append(state)
                    # print(won)
                # if won == 2:
                #     print(won)


            # if winCount == 3:
            #     print(winCount)
            #     return 0
                # print("Found a win...continuing")
                # break

            # break
            # if myString == "win":
            #     print(myString)
            # if myString == "win":
            #     print("breaking")
            #     break



        # break

def war_update(u,v):

    s1, pop1 = G.node[u]["state"], G.node[u]["pop"]
    ss, pop2 = G.node[v]["state"], G.node[v]["pop"]

    #pop1 = max(p1, empire_pops[G.node[u]["empire"]])
    #pop2 = max(p2, empire_pops[G.node[v]["empire"]])

    #Is neighbour a target? - not if I'm white (neutral) or if we're on on same team
    if s1 == "white" or s1 == ss:
        return ss , "no"
    else:
        #Is a target - assess target (will later consider GDP - risk/reward ratio)
        # if pop1 > pop2:
            #if we are bigger then attack
        if random.random() < findP(pop1, pop2):
            #win battle
            #empire_pops[G.node[u]["empire"]] = empire_pops[G.node[u]["empire"]] + pop2
            return s1 , "yes"
        else:
            #lose battle
            #empire_pops[G.node[v]["empire"]] = empire_pops[G.node[v]["empire"]] + pop1
            return ss, "no"
        # else:
            #don't attack
            # return ss , 3

def plotGraph(G):
    # Make this plot larger.
    plt.figure(figsize=(15,10))

    m = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
                  lat_0=0, lon_0=0)

    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary()

    for country, lon, lat in zip(countries, lons, lats):
        x,y = m(lon, lat)
        pos[country] = (x,y)

    for u in G.nodes():
        colors.append(G.node[u]["state"])
        sizes.append(G.node[u]["size"])
    nx.draw_networkx(G,pos,node_size=sizes,node_color=colors,edge_color = 'green',with_labels = False)
    plt.show()

#RUN
if __name__ == "__main__":
    importData()
    G = genGraph()

    # p = 0.1 # probability of acquiring infection from a single neighbour, per time-step
    # td = 10 # td time-steps after infection, the individual dies
    nsteps = 100 # how many time-steps to run

    war_init(G,pos)

    for i in range(nsteps):
        numRed = sum(G.node[i]["state"] == "red" for i in G.nodes())
        numYellow = sum(G.node[i]["state"] == "yellow" for i in G.nodes())
        numBlue = sum(G.node[i]["state"] == "blue" for i in G.nodes())
        numWhite = sum(G.node[i]["state"] == "white" for i in G.nodes())

        print("Before Step:", i, "-> Red:", numRed, " Yellow:", numYellow, " Blue:", numBlue, " White:", numWhite)

        step(G)


    plotGraph(G)
