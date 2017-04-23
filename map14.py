import csv
import networkx as nx
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import random
import math

countries, lats, lons, pops, GDPs = [], [], [], [], []
pos = {}
filename = 'Data.csv'

colors, sizes = [], []

empire_pops = [0, 0, 0, 0]
empire_GDPs = [0, 0, 0, 0]


def importData():

    with open(filename) as f:
        # Create a csv reader object.
        reader = csv.reader(f)

        # Store the latitudes and longitudes in the appropriate lists.
        for row in reader:
            countries.append(row[0])
            lats.append(float(row[1]))
            lons.append(float(row[2]))
            pops.append(float(row[3])/10000)
            GDPs.append(float(row[4])/10000)

def genGraph():

    G = nx.Graph()

    #Add nodes & calculate distances between countries and add edges
    i = 1
    for c, p, g, lon, lat in zip(countries, pops, GDPs, lons, lats):
        G.add_node(c, pop = p, GDP = g, lon = lon, lat = lat)
        
    for c1, lon1, lat1, pop1, g in zip(countries, lons, lats, pops, GDPs):
        #connected = False
        for c2, lon2, lat2, pop2  in zip(countries[i:], lons[i:], lats[i:], pops[i:]):
            dist = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)
            maxPop = max(pop1, pop2)
            score  = np.power(maxPop,(1/5))/dist
            if score > 0.09:
                #connected = True
                G.add_edge(c1, c2, weight = dist)
                #G.node[c2]["connected"] = connected
        #G.node[c1]["connected"] = connected     
        i = i + 1
        
    for u in G.nodes():
        connected = 1
        if G.degree(u) == 0:
            connected = 0
        G.node[u]["connected"] = connected

    #connect america to europe
    G.add_edge("United States", "Ireland")
    G.add_edge("Canada", "Ireland")
    G.add_edge("Portugal","United States")
    G.add_edge("United States","Morocco")
    return G

def war_init(G,pos):
    """Set countries to attack"""
    teams = ["red","yellow","blue"]
    i = 1
    for u in G.nodes():
        state = "white"
        size = 50
        emp = 0
        x = random.randint(0,1)
        if teams and G.node[u]["pop"] * x > 10 and G.node[u]["GDP"] * x > 1000:
            state = teams.pop()
            #print(len(G.neighbors(u)))
            size = 150
            emp = i
            empire_pops[i] = G.node[u]["pop"]
            empire_GDPs[i] = G.node[u]["GDP"]
            i = i + 1
            print(u,": ",state)
        G.node[u]["state"] = state
        G.node[u]["size"] = size
        G.node[u]["empire"] = emp
    #plotGraph(G)

def findP(pop1, pop2, GDP1, GDP2):
    
    return (pop1/(pop1+pop2))* (GDP1/(GDP1+GDP2))

def step(G):
    """Given a graph G, run one time-step."""
    #myList = []
    for u, d in G.nodes(data=True):
        if G.node[u]["state"] in ["red","yellow","blue"]:
            for v in G.neighbors(u):
                #if G.node[u]["state"] in myList:
                    #continue
                #else:
                    state, won = war_update(u,v)
    
                    if won == "yes":
                        G.node[v]["state"] = state
                        #myList.append(state)
                    
                    else:
                        G.node[u]["state"] = state

def war_update(u,v):

    u1, p1, g1 = G.node[u]["state"], G.node[u]["pop"], G.node[u]["GDP"]
    u2, p2, g2 = G.node[v]["state"], G.node[v]["pop"], G.node[v]["GDP"]

    emp_u = G.node[u]["empire"]
    emp_v = G.node[v]["empire"]

    pop1 = max(p1, empire_pops[emp_u])
    pop2 = max(p2, empire_pops[emp_v])
    GDP1 = max(g1, empire_GDPs[emp_u])
    GDP2 = max(g2, empire_GDPs[emp_v])

    #Is neighbour a target? - not if I'm white (neutral) or if we're on on same team
    if u1 == "white" or u1 == u2:
        return u2 , "no"
    else:
        #Is a target - assess target (will later consider GDP - risk/reward ratio)
        # if pop1 > pop2:
            #if we are bigger then attack
        p = findP(pop1, pop2, GDP1, GDP2)
        print(u," ",p)
        if random.random()*random.random() < p:
            #win battle
            empire_pops[emp_u] = pop1 + G.node[v]["pop"]
            empire_GDPs[emp_u] = GDP1 + G.node[v]["GDP"]
            empire_pops[emp_v] = pop2 - G.node[u]["pop"]
            empire_GDPs[emp_v] = GDP2 - G.node[u]["GDP"]
            #print(u,"beat",v,pop1," ",pop2, " ", GDP1, " ", GDP2)
            return u1 , "yes"
        else:
            #lose battle
            empire_pops[emp_u] = pop1 - G.node[v]["pop"]
            empire_GDPs[emp_u] = GDP1 - G.node[v]["GDP"]
            empire_pops[emp_v] = pop2 + G.node[u]["pop"]
            empire_GDPs[emp_v] = GDP2 + G.node[u]["GDP"]
            #print(u,"lose to",v,pop1," ",pop2, " ", GDP1, " ", GDP2)
            return u2, "no"
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
    nsteps = 500 # how many time-steps to run

    war_init(G,pos)

    for i in range(nsteps):
        numRed = sum(G.node[i]["state"] == "red" for i in G.nodes())
        numYellow = sum(G.node[i]["state"] == "yellow" for i in G.nodes())
        numBlue = sum(G.node[i]["state"] == "blue" for i in G.nodes())
        numWhite = sum(G.node[i]["state"] == "white" for i in G.nodes())

        #print("Before Step:", i, "-> Red:", numRed, " Yellow:", numYellow, " Blue:", numBlue, " White:", numWhite)

        step(G)
        
        if i == 400:
            for u1 in G.nodes():
                bestscore = 0
                if G.node[u1]["connected"] == 0:
                    for u2 in G.nodes():
                        if (u1 == u2) or (G.node[u2]["connected"] != 1):
                            continue
                        lon1 = G.node[u1]["lon"]
                        lat1 = G.node[u1]["lat"]
                        lon2 = G.node[u2]["lon"]
                        lat2 = G.node[u2]["lat"]
                        dist = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)
                        maxPop = empire_pops[G.node[u2]["empire"]]
                        score  = np.power(maxPop,(1/5))/dist
#                        print(u1)
#                        print(u2)
    #                    print(maxPop)
#                        print(score)
                        if score > bestscore:
                            bestscore = score
                            bestnode = u2
                            bestdist = dist
                    if bestscore > 0:
                        G.add_edge(u1, bestnode, weight = bestdist)
                        G.node[u1]["connected"] == 2
                    
    plotGraph(G)


