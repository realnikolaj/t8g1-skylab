---
title: Network analysis
prev: data-description
next: text-analysis
---

Brief basis of the network:

- Each node is unique and represents either:
  - A) A law or amendment to another law and is currently effective or
  - B) A passed proposal going into effect some time in the future
- Edges are directional and originates from law documents by:
  - A) Being based on referrences to other documents e.g. to a specific law document
    or a
    paragraph within a law that would provide the necessary legal foundation for where the edge originated and/or
    providing eseential background definitions regarding the scope of the law
  - B) Being based on the fact that a law is to some extent ammending or adding new definitions to other laws.

As mentioned in the data description each level of network is based on the refferences collected from the previous
level's
nodes. A document
might referrence one or more documents and might not referrence any at all. A list of all collected referrences is
kept after each data collection process and used to collect node information and edges for the next level.
By implementing this level or tier inspired process presents an opprtunity to compare or at least evaluate the
distance between nodes in the resulting network. The levels also provides analysis and comparison opportinities
regarding each node's, in each level's, relationship to the topic pandemic keywords.

Different inherent characterics regarding the levels are important to note. Level two and three does not pertain to
the conditions of the first level other than they must not be historical meaning that there must not exist a more
current version of the same law definition, with the same and they must be in
effect, meaning it is a regulation actively being posed upon residents or other legal entities of Danish juristriction
Other than that nodes of level two and three does not necesarryly contain the keywords used to aquire the nodes of
level one and they could also be dated anywhere before the year 2019.

Given the above introduction it's present to discuss some factors weighted for the inclusion of the third level. As
it appears there's is no condition regarding the topic of this research posed on any nodes appart from nodes at the
first level. Building the second level is a reasonably obvious decision, without this level, there might not be any
fundamental and node-enabling ancesting nodes e.g. such as a paragraph in the constitituion giving extended authority
in a time of crisis. Provided by the second level there's also information about, from which authority or gorvening
body, level-one nodes are related to e.g. which part of the industry or category such as health, socia-economics
etc. a node represents or is affecting the most. For the inclusion of the third-tier nodes are the rational as with
the second; by including the third level we minimize the buffer-zone of hidden incomming links to tier one's nodes,
and tier two, which improves the definition and also the quality of the network.

Before cleanup level one contains 343 unique nodes with 853 outgoing edges, level two provided the nodes referrenced
by the 853 edges in level one and 1729 outgoing edges forming the nodes of level three that in turn gave 6184
referrences which of many were not included since they inherently did not all of them go to nodes within the prior
two levels. An undetermined amount of refferences from second and third levels did not provide additional nodes
since they would be refferences to existing nodes, these were only used for creating additional incomming edges to
other levels.
In total after the described post-cleanup process the final graph consists of 1458 unique nodes and 1601 edges.

A significant number of referrences found for each node at each level was dropped due to conditions mentioned above.
initially the total number of edges in the first level was 2003, meaning that 1150 referrences were either going to
Historical documents, like mentions to the document itself in an older version or to documents that at the time of
our data collection was not yet ratified i.e. an effective law or statement, see an example of how these historical
self-referrences or self-loops manifests in a network partition in the network graph below.

![Historic edges example|35%](/images/histEdges.png)

During review of a
document, current versions will referrence earlier ones and finally - potentially if ratified - appear
again as yet another separate node with new links. We believe the self-contained mini-clusters is caused by either
various independent and self-contained documents with a certain context, origin like the type of a document here 
shown with historic edges turned off:

![DocType colored|35%](/images/withouthistgraph.png)

For 2. level the total outgoing or self-loop edges was 6201 which of where 4600 referrences was dropped due to the
clean-up conditions and the third and final level initially returned a staggering 17634 referrences which of only
786 met the conditions. Importantly, we assigned level labels or attributes in a "first-found-in" princip, meaning nodes
discovered in
level 2 will from then on always be considered a level-2 node, even if referrences from other nodes in the same
level goes to this "neighboring" node and not counted as a higher tier node. This is a post process performed after
the initial collection and reads out only new and thus exclusive nodes in the requested tier.

Intuitively, no reverse edge, i.e. edges going from a higher to a lower tier were found at level 2, this is expected
but **not quaranteed** since that, for outgoing edges in level 2 to go to level 1, would require that this node in
level 2 was created relatively recent which could be true but no hits here based on the post-clean conditions. In 
contrast level 3 makes 539 reverse edges to level 2. 
By having no reverse edges from the two higher levels to level 1 hints at a certain pattern for the level 1 ones, 
namely that they would all be edges with no further chains than those going to higher levels and form the end-nodes 
of structures they might be part of, this is also backed by running the same tests for reverse edges on each individual 
levels against it self. Self-level-loops is found in level 2 and 3 with 150 and 304 referrences respecitvely, but none 
were found in level 1, again this would also be more likely but not quaranteed.
A structure of the network with the nodes colored based on their levels is seen here below:

![DocType colored|35%](/images/lvlsgroupgraph.png)

# Degree of centrality

By calculating the degree of centrality, we can see if there is some laws thar are more central than the other laws. By looking at the distribution of the degrees of centrality across the different laws, we can see that there is a fairly wide spread of centality, but with some laws having a signifcantly higher degree of centrality.

![Origin type colored|35%](/images/centrality_distribution.png)

By looking at the top 10 nodes in terms of degree of centrality, we can see that the nr 1 node has a degree of 0.049, wich is 0.012 higher than 0.2, and twice as much as nr 8. This indicates that the nr one node has a huge impact on the other laws.

![Origin type colored|35%](/images/top10degreecentrality.png)

# Communities

By using the Girvan Newman Algorithm we can divide the nodes into communites, and display them in the network.
![Origin type colored|35%](/images/girvan_newman_communities.png)
