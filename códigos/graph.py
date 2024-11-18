import networkx as nx
import json


f = open('relacoes.json',"r")
users = json.load(f)
G = nx.Graph()

for user, colabs in users.items():
  G.add_node(user)
  for colab, times in colabs.items():
    G.add_node(colab)
    G.add_edge(user,colab)

for u in users:
  G.add_node(u)
  for c in users[u]:
    if c not in users:
      G.add_node(c)
for u in users:
  for c in users[u]:
    for x in users[u]:
      if x != c:
        G.add_edge(x, c, times=times)
    if c in G.nodes():
      G.add_edge(u, c)


nx.write_gexf(G, "grafoFinal.gexf")

