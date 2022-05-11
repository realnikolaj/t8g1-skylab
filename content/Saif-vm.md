---
title: VM@Saif
prev: Group-vm
next: Nikolaj-vm
---

Data presented on this site consists of a collection of documents produced by the various Danish governments and
ministeries and hosted on the public website www.retsinformation.dk. Each node in the following networks represents a
unique document regarding procedures and contents of ammending, changing or adding laws in Denmark. There 
are various instances or government bodies capable of producing these documents thus each document contains 
information such as the body initializing the proposal of said new document, date of creation, ID's etc.

This site presents documents that are current i.e. not historical or obsolete, documents that have been ratified 
meaning the contents of the document is currently, or soon will be, afficting danish law. In addition to these 
conditions this analysis is initialized on a minor subset of the full data provided at the source and iteratevely 
build up in expanding levels. 

The preliminary subset was conditionally collected using advanced search available at the source website. These 
initial documents provides the first level of data and consists of documents added at the source in the interval 
including the year 2019-2022 aswell as being non-historical, ratified and containing a set of pandemic themed 
key-words which includes: virus, covid, pandemic and corona.

Building the next levels was done by scraping each document, which is avaible through a webbrowser or a REST API, 
and collecting the texts and metadata contain within. Metadata for documents conforms to the Eli-standard a standard 
for national law texts in EU TODO:ref eli. Importantly was the referrences to other documents that would represent a 
literal refference to another law, a specific section or paragraph in another law or laws which are directly 
impacted or changed by the new or ammendet law. 

By building up 3 aditional layers, layers produced by looking at the referrences mentioned above and recursevly 
scraping them, the resulting network of documents, post-cleaning, presents some ~1600 unique documents or 'nodes' 
with a total of 2K directed edges.

The post-clean process simply ignores historical nodes at levels above 1., which otherwise could be a 
historical or obsolete document with recent and more current changes available in another unique document i.e. a 
symbolic duplicated/deprecated node and excluded edges to nodes which were not present in either of 
the 3 levels of documents affectively creating a network isolated at the 3. level.
There's

![](/images/tempFinalNetwork.png)



In the following sections laws and documents are used interchangebly to describe a node and aswell for edge mentions 
which could be stated as a referrence or a link.
    
We believe that our source code used for collecting and analyzing the network and the body of text contained within 
each node could be utilized for other similar datastructures of HTML/Java hence why sometimes within the analysis 
you might find a certain quoted referrence not directly related to the analysis of the documents of www.
retsinformation.dk 
but 
might represent some other realization about a specific PyPi library that possed a challenge regarding the various 
data formats and structures present during this work.

|       | Level 1 | Level 2 | Level 3 |
|-------|---------|---------|---------|
| Nodes | 343     | 511     | 1090    |
| Edges | 343     | 511     | 1090    |


[The data can be downloaded in BZ2 compression format here](/data/picl_data_l3.pbz2)


