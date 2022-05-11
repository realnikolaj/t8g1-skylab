import pandas as pd
import networkx as nx
import networkx as nx
import netwulf as nw
import itertools
import numpy as np
import bz2
import pickle
import _pickle as cPickle


def significant(idToIndexMapper):
    for key in idToIndexMapper:
        if idToIndexMapper[key]["indexInGraph"] == 91:
            print("Highest degree", idToIndexMapper[key])

def build(dff):
    G = nx.empty_graph(0, None)
    for node in dff[["id", "edgesUrl", "isHistorical", "stateLabel"]].itertuples():
        G.add_nodes_from(dff.id)
        if not node.isHistorical and node.stateLabel != None:
            G.add_node(node.id)
            for edge in node.edgesUrl:
                if not dff.id[dff.EliUrl.str.endswith(edge.split('dk/')[1])].empty:
                    nbrIsHis = dff.isHistorical[dff.EliUrl.str.endswith(edge.split('dk/')[1])].values.item()
                    nbrRatified = dff.stateLabel[dff.EliUrl.str.endswith(edge.split('dk/')[1])].values.item()
                    if not nbrIsHis and not nbrRatified:
                        nbr = dff.id[dff.EliUrl.str.endswith(edge.split('dk/')[1])]
                        G.add_edge(node.id, nbr.to_numpy().item())
                    # G.add_edges_from(((node, nbr) for _, node, nbrlist in [node for node in df[["EliUrl", "edgesUrl"]].itertuples()]))  # for nbr in nbrlist[1]))
    return G

def buildwithHist(df):
    G = nx.empty_graph(0, None)
    for node in df[["id", "edgesUrl", "isHistorical", "stateLabel"]].itertuples():
        G.add_nodes_from(df.id)
        if node.stateLabel != None:
            G.add_node(node.id)
            for edge in node.edgesUrl:
                if not df.id[df.EliUrl.str.endswith(edge.split('dk/')[1])].empty:
                #     nbrIsHis = df.isHistorical[df.EliUrl.str.endswith(edge.split('dk/')[1])].values.item()
                #     nbrRatified = df.stateLabel[df.EliUrl.str.endswith(edge.split('dk/')[1])].values.item()
                #     if not nbrIsHis and not nbrRatified:
                    nbr = df.id[df.EliUrl.str.endswith(edge.split('dk/')[1])]
                    G.add_edge(node.id, nbr.to_numpy().item())
                    # G.add_edges_from(((node, nbr) for _, node, nbrlist in [node for node in df[["EliUrl", "edgesUrl"]].itertuples()]))  # for nbr in nbrlist[1]))
    return G



def interEdges(df1, df2):
    reverseEdge = 0
    for node in df2[["id", "edgesUrl"]].itertuples():
        for edge in node.edgesUrl:
            if not df1.id[df1.EliUrl.str.endswith(edge.split('dk/')[1])].empty:
                refIsHist = df1.isHistorical[df1.EliUrl.str.endswith(edge.split('dk/')[1])].values.item()
                refIsRat = df1.stateLabel[df1.EliUrl.str.endswith(edge.split('dk/')[1])].values.item()
                if not refIsHist and not refIsRat:
                    reverseEdge += 1
    return reverseEdge

def nodeAttr(G, df):
    for node in df.itertuples():
        sizeoftext =  np.log2(node.full_text.__sizeof__())
        # attrs = {node.id: {"lvl": node.rlvl, "group": node.ressort, "size": sizeoftext}}
        attrs = {node.id: {"group": node.rlvl, "ressort": node.ressort, "size": sizeoftext}}
        # attrs = {node.id: {"lvl": node.rlvl, "ressort": node.ressort, "size": sizeoftext, "group": node.documentTypeId}}
        nx.set_node_attributes(G, attrs)

def exclusive(df1, df2):
    exclusives = []
    for node in df2.itertuples(index=False):
        if df1.id[df1.id == node.id].empty:
            exclusives.append(node)
    return pd.DataFrame(exclusives, columns=df2.columns)

def read(lvl):
    df = bz2.BZ2File(f'data/picl_data_l{lvl}.pbz2', 'rb') # Or data/urls_l1.pkl
    df = cPickle.load(df)
    url = pd.read_pickle(f'data/urls_l{lvl}.pkl')
    return df, url

def write(df):
    with bz2.BZ2File(f'data/picl_data_final__.pbz2', 'w') as f:
        cPickle.dump(df, f)

# nx.degree_centrality(G)
if __name__ == '__main__':
    df = bz2.BZ2File(f'data/picl_data_final__.pbz2', 'rb') # Or data/urls_l1.pkl
    df = cPickle.load(df)
    # #ressortslist = df3.ressort.unique()
    # df1, url1 = read(1)
    # df2, url2 = read(2)
    # df3, url3 = read(3)
    # dfe2 = exclusive(df1, df2)
    # dfe3 = exclusive(dfe2, df3)
    # df1['rlvl'] = 1
    # dfe2['rlvl'] = 2
    # dfe3['rlvl'] = 3
    # df = pd.concat([df1,dfe2,dfe3])
    # df = df.drop_duplicates(subset=["id"])
    # write(df)
    # dfSelfEdges = interEdges(df.loc[df['rlvl'] == 2], df.loc[df['rlvl'] == 2]) # For inter referrences and self-loops
    # G = nx.DiGraph()
    # G = build(df)
    # nodeAttr(G, df)
    # list(G.nodes(data=True))[:3]
    # stylized, conf = nw.visualize(G, config=histconf)
    # histstylized, histconf = nw.visualize(HistG)
