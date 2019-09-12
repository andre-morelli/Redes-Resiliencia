# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 12:48:09 2019

@author: ANDRE BORGATO MORELLI
"""

import igraph as ig
import networkx as nx
import numpy as np
import operator

def get_igraph(G, weight=None):
    G = G.copy() 
    G = nx.relabel.convert_node_labels_to_integers(G)
    Gig = ig.Graph(directed=True)
    Gig.add_vertices(list(G.nodes()))
    Gig.add_edges(list(G.edges()))
    Gig.vs['osmid'] = list(nx.get_node_attributes(G, 'osmid').values())
    if weight != None:
        Gig.es[weight] = list(nx.get_edge_attributes(G, weight).values())
    return Gig

def get_efficiency(G, weight = None):
    Gig = get_igraph(G,weight=weight)
    efficiency = {}
    for node in Gig.vs:
        shrt = Gig.shortest_paths_dijkstra(node,weights=weight)
        total_proximity=0
        for l in shrt[0]:
            if l == 0:
                continue
            total_proximity += 1/l
        total_proximity = total_proximity/len(Gig.vs)
        efficiency[int(node['osmid'])] = total_proximity
    return efficiency

def get_connectivity(G):
    Gig = get_igraph(G,weight=None)
    valid_paths = {}
    for node in Gig.vs:
        shrt = Gig.shortest_paths(node)
        valid = 0
        for l in shrt[0]:
            if l == 0:
                continue
            if l!=np.inf:
                valid+=1
        valid_paths[int(node['osmid'])] = valid
    return valid_paths

def get_targeted_efficiency_and_connectivity(G, target, target_true_label=0, weight = None):
    Gig = get_igraph(G,weight=weight)
    efficiency = {}
    valid_paths = {}
    nodes = Gig.vs
    target_list = [node for node in nodes if node[target]==target_true_label]
    for node in nodes:
        shrt = Gig.shortest_paths_dijkstra(node,target=target_list,weights=weight)
        l = min(shrt)
        efficiency[int(node['osmid'])] = 1/l
        if 1/l==0:
            valid_paths[int(node['osmid'])] = 0
        else:
            valid_paths[int(node['osmid'])] = 1
    return efficiency, valid_paths

def get_efficiency_and_connectivity(G, weight = None):
    Gig = get_igraph(G,weight=weight)
    efficiency = {}
    valid_paths = {}
    for node in Gig.vs:
        shrt = Gig.shortest_paths_dijkstra(node,weights=weight)
        total_proximity = 0
        valid = 0
        for l in shrt[0]:
            if l == 0:
                continue
            if l!=np.inf:
                valid+=1
            total_proximity += 1/l
        total_proximity = total_proximity/(len(Gig.vs)-1)
        efficiency[int(node['osmid'])] = total_proximity
        valid_paths[int(node['osmid'])] = valid
    return efficiency, valid_paths

def get_overall_connectivity(valid_paths, original_valid_paths=None):
    if original_valid_paths != None:
        paths = sum(valid_paths.values())/sum(original_valid_paths.values())
    else:
        paths = sum(valid_paths.values())/len(valid_paths)
    return paths

def get_overall_efficiency(efficiency, original_efficiency):
    return np.nanmean(list(efficiency.values()))/np.nanmean(list(original_efficiency.values()))

def remove_nodes_by_attr(G, attr, remove_proportion, ascending=False):
    G_new = G.copy()
    lst = [(G.nodes[n][attr], n) for n in G.nodes]
    if ascending:
        lst= sorted(lst)
    else:
        lst= sorted(lst, reverse=True)
    remove = [n for m,n in lst[:int(remove_proportion*len(lst))]]
    for node in remove:
        G_new.remove_node(node)
    return G_new

def remove_edges_by_attr(G, attr, remove_proportion, ascending=False):
    G_new = G.copy()
    lst = [(G.edges[e][attr], e) for e in G.edges]
    if ascending:
        lst= sorted(lst)
    else:
        lst= sorted(lst, reverse=True)
    remove = [n for m,n in lst[:int(remove_proportion*len(lst))]]
    for edge in remove:
        G_new.remove_edge(*edge)
    return G_new

def remove_nodes_random(G, remove_proportion, random_seed=None):
    random.seed(random_seed)
    G_new = G.copy()
    remove = random.sample(list(G.nodes), int(remove_proportion*len(G.nodes)))
    for node in remove:
        G_new.remove_node(node)
    return G_new

def remove_edges_random(G, remove_proportion, random_seed=None):
    random.seed(random_seed)
    G_new = G.copy()
    remove = random.sample(list(G.edges), int(remove_proportion*len(G.edges)))
    for edge in remove:
        G_new.remove_edge(*edge)
    return G_new
