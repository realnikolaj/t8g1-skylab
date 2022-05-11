---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import pandas as pd
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman
import matplotlib.pyplot as plt
import netwulf as nw
import bz2
import pickle
import _pickle as cPickle
import numpy as np
```

```python
data = bz2.BZ2File('../data/picl_data_l3.pbz2', 'rb')
data = cPickle.load(data)
```

## Create graph

```python
df = data
def build():
    G = nx.empty_graph(0, None)
    G.add_nodes_from(df.id)
    for node in df[["id","edgesUrl"]].itertuples():
        for edge in node[2]:
            if not df.id[df.EliUrl.str.endswith(edge.split('dk/')[1])].empty:
                nbr = df.id[df.EliUrl.str.endswith(edge.split('dk/')[1])]
                G.add_edge(node.id, nbr.to_numpy().item())
                # G.add_edges_from(((node, nbr) for _, node, nbrlist in [node for node in df[["EliUrl", "edgesUrl"]].itertuples()]))  # for nbr in nbrlist[1]))
    return G
G = build() 
```

## Degree of centality

```python
centrality = nx.degree_centrality(G)
sortedList = sorted(centrality.items(), key=lambda item: item[1], reverse=True)
print("top 10 nodes in temrs of degree of cenrality")
for i in range(len(sortedList[:10])):
    print("Nr {}: Node nr {} - Degree centrality: {}".format(i + 1, sortedList[i][0], sortedList[i][1]))
```

### Plot distribution of degree of centrality

```python
l = list(centrality.items())

# plot
fig, ax = plt.subplots()
y= []

for i in l:
    y.append(i[1])
x = [i for i in range(len(y))]
ax.bar(x, y, width=1, edgecolor="white", linewidth=0.2)
plt.savefig('centrality_distribution.png')
plt.show()
```

## Find communites

```python
communities = girvan_newman(G, most_valuable_edge=None)
node_groups = []
for com in next(communities):
    node_groups.append(list(com))
cmap = plt.get_cmap('viridis')

colors = cmap(np.linspace(0, 1, 100))

color_index = 0
color_map = {}
for node in G:
    color_index = 0
    node_added = False
    for node_group in node_groups:
        if node in node_group:
            color_map[node] = colors[color_index]
        color_index += 1
        node_added = True
    if node_added is False:
        color_map[node](colors[color_index])
```

```python
nw.visualize(G)
```
