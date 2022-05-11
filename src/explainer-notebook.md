---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.7
  kernelspec:
    display_name: Python [conda env:comsocsci2022]
    language: python
    name: conda-env-comsocsci2022-py
---

<!-- #region -->
# Project Assignment
## Group 6
> s183930 - Nikolaj S. Povlsen

> s184208 - Steffen Holm Cordes

> s217176 - Johan Fredrik Bjørnland

## Link to Git repository
https://github.com/realnikolaj/G6_Retsinformation



## Contribution statement

We worked collaboratory as a group, main responsibles on code, website and explainer notebook are:

Downloaded and preprocessed the data: Nikolaj & Steffen & Fredrik

Network analysis: Nikolaj & Fredrik

Text analysis: Steffen

<!-- #endregion -->

# Motivation

## 1. What is your dataset?

The dataset used in this project consists of laws fetched from www.retsinformation.dk. Preliminary search for primary documents were made using "extreme search" function (1) available at the source website. Attributes and text collected using request (2) and secondary documents (edges) found using javascript rendering with requests_html (3).

- 343 Primary/initial nodes based on search criteria.

- Identify Secondary nodes (nodes affected by Primary nodes).

- 2173 edges in total

## 2. Why did you choose this/these particular dataset(s)?

Influenced by the corona pandemic, Danish lawmakers made amendments to existing laws and created new laws. By evaluating common links between all new laws containing "pandemic" keywords we seek to establish the one most relevant document for the creation of future laws. Although highly accessible, the Danish law may not be easily understood by everyone. Subjecting the documents to impartial and unbiased computer algorithms we seek to establish a logical chain of links and establish significant areas of importance in the Danish body of law

## 3. What was your goal for the end user's experience?

- Define scope of documents and fetch data
- Define the network with documents as nodes and references as edges
- Identify significant nodes by:​
  - Visualizing the network
  - Analyze and condition to test "High significance" hypothesis​
- Tokenize, clean the law texts and generate Wordclouds
- Using the Wordclouds based on TF-IDF to understand the contextual association between "high significance" nodes and their neighbours​

# Basic stats. Let's understand the dataset better


Below we have the asynchronous dataloader which downloads the required information in batches from https://www.retsinformation.dk/api/document/eli/.

The end result is a ~13MB BZ2 compressed datafile with the following fields:


| **Data field**  | **rlvl**            | **id**            | **title**                   | **documentTypeId**                          | **shortName**             | **full_text**                            | **isHistorical**                       | **ressort**               | **EliUrl**                                                    | **stateLabel**         | **metadata**                                                           | **edges**                                                  | **edgesUrl**                                                                                                    |
|-----------------|---------------------|-------------------|-----------------------------|---------------------------------------------|---------------------------|------------------------------------------|----------------------------------------|---------------------------|---------------------------------------------------------------|------------------------|------------------------------------------------------------------------|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| **Description** | Recursive level 1-3 | Unique id for law | Official title              | Type of document, e.g. Lov or Ændringslov   | Shortname identifier      | Full text of law                         | Is this law historical or applicable   | Ministry responsible      | API link                                                      | If law has been passed | Metadata, including date of publication                                | References to other laws                                   | Links to references                                                                                             |
| **Example**     | 2                   | 224291            | Lov om ændring af lov om... | 20                                          | LOV nr 1439 af 29/06/2021 | Den fulde tekstLov om ændring af lov ... | False                                  | Beskæftigelsesministeriet | https://www.retsinformation.dk/api/document/eli/lta/2021/1439 | Vedtaget               | {'displayName': 'Offentliggørelsesdato', 'displayValue': '30/06/2021'} | ['LOV nr 1641 af 19/11/2020', 'LBK nr 2566 af 13/12/2021'] | ['https://www.retsinformation.dk/eli/lta/2020/1641', 'https://www.retsinformation.dk/eli/ft/202013LA0235', ...] |

<!-- #region tags=[] -->

```python
'''
This is the dataloader class script that scrapes source using the requsts-html to collect data and render Java 
on non-API pages to collect a list of the refferences at the document.
Python built-in asynio is used to enable asynchronous scraping of multiple nodes in parallel.
'''
from gevent import monkey
# monkey.patch_all()
import sys
import bz2
import pickle
import random
import _pickle as cPickle
import nest_asyncio
import asyncio
from requests_html import AsyncHTMLSession, HTMLSession
import re
import pandas as pd
import json
from itertools import chain
from more_itertools import ichunked


class Retsinfo:
    def __init__(self, level, batchsize=25, Timeout=10, workers=None, edges=True):
        self._lvl = level
        self._timeout = Timeout
        self._batchsize = batchsize
        self.loop = asyncio.new_event_loop()
        self._workers = workers
        #self._df = self.read()
        self._edges = edges
        self._listdata = []
        self.done = 0
        self._elipattern = '/eli/.*'
        self._outcolumns = ['rlvl', 'id', 'title', 'documentTypeId', 'shortName', 'full_text', 'isHistorical', 'ressort', "EliUrl", "stateLabel", "metadata", "edges", "edgesUrl"]
        self._previous_df = None
        self._and_uniques = None
        self._result = None

    async def main(self):
        self.read()
        #return self._df
        iter = self._df.iteritems()  # self._df.itertuples(index=False)
        batches = ichunked(iter, self._batchsize)
        # Initialize the class object event loop
        loop = asyncio.get_running_loop()
        with AsyncHTMLSession(loop=loop, workers=self._workers) as session:

            #for _batch in [next(batches) for i in range(2)]:  # batch[:4]:
            for _batch in batches:  #  [next(batches) for i in batches]: #  range(self._df.size / self._batchsize)]:  # range(4)]:  # batch[:4]:
                await self.run(session, _batch)


                # for response in await self.run(session,_batch):
                #     await self.append(response)
        # df, url = self.write()

        self.write()
        return self._df, self._and_uniques

    async def run(self, session, batch):  # , df, loop=None, stepsize=10, edges=True, workers=None):
        """
        :param df: List of URL's
        :param Batch: Dumb fix for errors caused by potentially hundreds of async render requests (request_html.AsyncHTMLSession)
        :return: List of row, data
        """
        # Use list comprehension to create a list of
        # tasks to complete. The executor will run the `fetch`
        # function for each url in the urlslist
        tasks = [await session.loop.run_in_executor(
            session.thread_pool,
            self.fetch,
            *(session, _idx, url)
        )
                 for _idx, url in batch  # For multiple arguments to fetch function
                 ]

        await asyncio.gather(*tasks)

    def running(self):
        return self.done < self._df.size

    async def get_edges(self, session, id, url):
        #url = url.split('api')[0] + url.split('document/')[1]
        resp = await session.get(url, timeout=self._timeout)
        await resp.html.arender(retries=60, wait=random.randint(10, 30), timeout=self._timeout, sleep=8, keep_page=False)
        #edges = [{url.split('/eli')[0] + edge: '{placeholder}'} for edge in resp.html.links if
        #         (re.match(self._elipattern, edge) and len(edge) < 30)]
        fulltext = resp.html.text
        _changes = fulltext.find("overblik")
        changes_ = fulltext[_changes:].find("Fold ind")
        edgesUrl = [url.split('/eli')[0] + edge for edge in resp.html.links if (re.match(self._elipattern, edge) and len(edge) < 30)]
        edges = fulltext[_changes:_changes+changes_].splitlines()[1:] # Finds the list of edges, limits output
        return edges, edgesUrl

    async def get_meta(self, session, id, url):
        temp_url = url.split('eli')[0] + 'api/document/' + url.split('dk/')[1]
        resp = await session.get(temp_url, timeout=self._timeout)
        document = json.loads(resp.text)  # Source API response
        '''
        Add varaibles below to get more info
        OBS!!! Don't forget to add them to the return of get_meta() (this function), otherwise the append() call won't append them to the final data output
        '''

        unique_identity = document[0]["id"]
        title = document[0]["title"]
        ressort = document[0]["ressort"]
        documentTypeId = document[0]["documentTypeId"]
        shortName = document[0]["shortName"]
        url = resp.html.url
        isHistorical = document[0]["isHistorical"]
        full_text = str(resp.html.full_text)  # document[0]["documentHtml"]
        try:
            # caseHistoryReferenceGroup = document[0]["caseHistoryReferenceGroup"][0]['references']
            stateLabel = document[0]["caseHistoryReferenceGroup"][0]['stateLabel']
        except:
            # caseHistoryReferenceGroup = None
            stateLabel = None
        metadata = document[0]["metadata"]
        return [
            unique_identity,
            title,
            documentTypeId,
            shortName,
            full_text,
            isHistorical,
            ressort,
            url,
            stateLabel,
            metadata]
            # caseHistoryReferenceGroup,

    async def fetch(self, session, id, url):  # , id, name, url):  #, session, id, url, edges=True):
        print(f'Currently getting {url}')
        metadata = await self.get_meta(session, id, url)
        edges, edgesUrl = await self.get_edges(session, id, url)
        # L = await asyncio.gather(
        #     self.get_meta(session, id, url),
        #     self.get_edges(session, id, url),
        #     )
        # print(L)
        # print(len(L))

        # await self.append([self._lvl - 1, *L[0], L[1], L[2]])
        # return [*metadata, edges]
        await self.append([self._lvl-1, *metadata, edges, edgesUrl])

    async def display_status(self):
        while self.running():
            await asyncio.sleep(2)
            print('\rdone:', self.done)

    async def append(self, node):
        self._listdata.append(node)
        self.done += 1
        await asyncio.sleep(0.01)
        # Print the result
        print('\rdone:', self.done)

    def write(self):
        self._result = pd.DataFrame(data=self._listdata, columns=self._outcolumns)

        with bz2.BZ2File(f'data/picl_data_l{self._lvl}' + '.pbz2', 'w') as f:
            cPickle.dump(self._result, f)

        # if self._lvl == 1:
        # self._result.edgesUrl.explode().to_pickle(f'data/urls_l{self._lvl}.pkl')
        # else:
        #self._result = pd.DataFrame([self._previous_df, self._result])
        self._and_uniques = pd.DataFrame(data=self._result.edgesUrl.explode())
        self._and_uniques = pd.Series(self._result.edgesUrl.explode().drop_duplicates().reset_index(drop=True))
        self._and_uniques.to_pickle(f'data/urls_l{self._lvl}.pkl')  # Used for lvl+1 iteration - likely not needed

        print('Success')
        print(self._result.size)
        print(self._result.head())
        print(f'Writes data to data/picl_data_l{self._lvl}.pbz2')
        print(f'Writes unique urls to data/urls_l{self._lvl}.pkl')

    def read(self):
        # if self._lvl == 1:

        _clean = pd.read_pickle(f'data/urls_l{self._lvl - 1}.pkl')
        self._df = _clean
        self._df = self._df.where(~_clean.str.contains("#"))
        self._df = self._df.where(~_clean.str.contains("pdf", case=False))
        self._df = self._df.dropna()
        print(f'Reading url list of length{len(self._df)}')
        # self._df = cPickle.load(self._df)

        # else:
        #     #self._previous_df = bz2.BZ2File(f'data/picl_data_l{self._lvl - 1}' + '.pbz2', 'rb')  # Or data/urls_l1.pkl
        #     #self._previous_df = cPickle.load(self._previous_df)
        #     self._df = pd.read_pickle(f'data/urls_l{self._lvl - 1}.pkl')
        #     self._df = pd.concat([self._previous_df.EliUrl, self._df]).drop_duplicates().reset_index(drop=True)

                #pd.Series([self._previous_df, self._df]).drop_duplicates()


def read(lvl):
    df = bz2.BZ2File(f'data/picl_data_l{lvl}.pbz2', 'rb') # Or data/urls_l1.pkl
    df = cPickle.load(df)
    url = pd.read_pickle(f'data/urls_l{lvl}.pkl')
    # print('')
    # df = pd.read_csv('data/metadata.csv', sep=";", encoding="latin1", header=0, usecols=[0, 2, 8, 27])

    return df, url

if __name__ == '__main__':

    nest_asyncio.apply()
    level = 1
    batchsize = 16
    retsinfo = Retsinfo(level=level, batchsize=batchsize, Timeout=190, workers=16, edges=True)  # mode=dev)
    df, url = asyncio.run(retsinfo.main())
    #df, url = read(level)
    #res = retsinfo.write()
    #res.edgesUrl.explode().to_pickle("data/urls_l2.pkl")  # Unnests the links to use for next iteration "level"

```

<!-- #endregion -->

The end result of data gathering is the following:


|                       | Level 1 | Level 2 | Level 3 |
|-----------------------|---------|---------|---------|
| Laws                  | 343     | 509     | 749     |
| References post-clean | 2003    | 4191    | 11440   |


The post-clean process simply ignores historical nodes at levels above 1., which otherwise could be a historical or obsolete document with recent and more current changes available in another unique document i.e. a symbolic duplicated/deprecated node and excluded edges to nodes which were not present in either of the 3 levels of documents affectively creating a network isolated at the 3. level.


# Tools, theory and analysis

#### Describe which network science tools and data analysis strategies you've used, how those network science measures work, and why the tools you've chosen are right for the problem you're solving.

    For this project we have used networkx, netwulf and pandas. Networkx and netwulf are great tools to analyze and visulize network data. Calcualting centrality measures is easy with the built in functionality of networkx. To detect communities we have used the Girvan Newman algorithm from the Network book. Pandas has been used to explore and analyze the data. panda makes it easy to get a overview of the data, and process it into the correct format.

#### How did you use the tools to understand your dataset?

    The dataset was conditionally collected using advanced search available at the source website. These initial documents provides the first level of data and consists of documents added at the source in the interval including the year 2019-2022 aswell as being non-historical, ratified and containing a set of pandemic themed key-words which includes: virus, covid, pandemic and corona.

    Building the next levels was done by scraping each document, which is avaible through a webbrowser or a REST API, and collecting the texts and metadata contain within. Metadata for documents conforms to the Eli-standard a standard for national law texts in EU TODO:ref eli. Importantly was the referrences to other documents that would represent a literal refference to another law, a specific section or paragraph in another law or laws which are directly impacted or changed by the new or ammendet law.

    By building up 3 aditional layers, layers produced by looking at the referrences mentioned above and recursevly scraping them, the resulting network of documents, post-cleaning, presents some ~1600 unique documents or ’nodes’ with a total of 2K directed edges.

    Throughout this process we used pandas to index, filter and process the dataset into the format that we wanted. We then visulized it with networkx and netwulf to recognize any trends or patterns and obvious outliers.
## Text analysis

```python
import nltk, re
import pandas as pd
from spacy.lang.da.stop_words import STOP_WORDS
import lemmy
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import bz2
import _pickle as cPickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from IPython.display import Image
```

```python
# Load data
data = bz2.BZ2File('../data/picl_data_l3.pbz2', 'rb')
data = cPickle.load(data)
```
<!-- #region -->
The starting point for the processing of the text data is loading the downloaded data into a pandas dataframe for further processing, and working on the data in the data field 'full_text'.

First of all 'full_text' includes formatting like new line and line breaks, but also the same introductory sentences "Oversigt (indholdsfortegnelse)" and "Den fulde tekst". These will have to be removed as they do not add to a menaingful representaion of the text, and regex was chosen for simplicity and flexibility.

Next we utilize the nltk tokenizer(1) to create the list of words for each law. To reduce the number of words with the same meaning but in different grammatical form, we wanted to utilize a lemmatizer. A lemmatizer has to trained on the particular language and can be used both with part-of-speech tags. Part-of-speech(POS) tags help by defining the word grammatically in the context of the sentence(2) and can improve the performance of correct lemmatization.

We chose to leammatize instead of stemming, because we wanted to make sure the words ere easily readable in the Wordcloud representaion.

After consulting Finn Arup Nielsen excellent refrence on Danish NLP Ressources(3), we chose the Lemmy(4) lemmatizer. This package has the advantage of high accuracy on the danish language(4) and being able to use either POS tags or a standalone mode, where the latter was chosen for simplicity.

It is prudent to remove stopwords in NLP as these do not add meaning, but are just common words. Many stopword collectoins are available, but those that support Danish language differ in quality and and quantity. The nltk package only has 94 stopwords while the spacy(5) package included 219. After reviewing the contents we decided to use the spacy(5) stopword package. 
In addition to stopwords we wanted to remove Danish law specific words such as: stk, nr, pkt, jf. and these were added to the stopword list, also words with only 1 character were removed. Also to make sure the text format was uniform. we lowercased all tokens.



(1) https://www.nltk.org/

(2) https://en.wikipedia.org/wiki/Part-of-speech_tagging

(3) https://www2.imm.dtu.dk/pubdb/edoc/imm6956.pdf

(4) https://github.com/sorenlind/lemmy

(5) https://spacy.io/
<!-- #endregion -->

#### Data processing workflow

```python
# Remove formatting and law intro sentences: "Oversigt (indholdsfortegnelse)" and "Den fulde tekst"
data['tokens'] = [re.sub(r'\xa0|\\r\\n|\\r|\\n|Oversigt \(indholdsfortegnelse\)|Den fulde tekst',' ',w.lower()) for w in data['full_text']]

# Tokenize and remove punctuation and numbers
data['tokens'] = [nltk.word_tokenize(re.sub(r'[^\w\s]|\d',' ',w.lower())) for w in data['tokens']]

# Danish lemmatizer without word tags
lemmatizer = lemmy.load("da")
data['tokens'] = [[min(lemmatizer.lemmatize("", w)) for w in ws] for ws in data['tokens']]

# Remove stopwords and stk, nr, pkt, jf
STOP_WORDS.update(['stk', 'nr', 'pkt', 'jf'])
data['tokens'] = [[w for w in ws if w not in STOP_WORDS] for ws in data['tokens']]

# Remove words with less than 2 characters
data['tokens'] = [[w for w in ws if len(w) > 1] for ws in data['tokens']]

# Lower case
data['tokens'] = [[w.lower() for w in ws] for ws in data['tokens']]
```

#### Calculate TF-IDF for each token


Our goal is to represent the law text in easily understandable manner with Wordclouds, and this demands that we only use the representative words to create the Wordclouds.
In order to only capture words which are most representative of each law in the corpus, a TF-IDF(1) value for each word was calculated. The TF part calculates each token frequency within the law tokens and IDF, the inverse document frequency, which means that if the token is not used by many other laws in the corpus, it is weighted up and vice versa. This ensures that not only frequent words are represented, but words that are particular for that law are chosen.

We had initially done a "manual" implementation of Calculating the TF-IDF matrix, but this proved to be a compute heavy operation. Instead we chose the package scikit-learn(2) which has the functionality builtin and online ressources for implementation(3), which proved much faster. The scikit-learn implementation uses the following formula to calculate IDF(2):

$ \mathit{IDF} \! \left(t \right) = \mathrm{log}\! \left(\frac{n}{\mathit{DF} \! \left(t \right)}\right)+1 $

Where DF(t) is the number of documents in the corpus that contains the token and the + 1 serves as not to ignoring tokens which appear in all documents in the corpus.

Lastly we make a dictionary with {token:TF-IDF value} for each token in each law, to make generating Wordclouds easy.

(1) https://en.wikipedia.org/wiki/Tf%E2%80%93idf

(2) https://scikit-learn.org/

(3) https://medium.com/analytics-vidhya/demonstrating-calculation-of-tf-idf-from-sklearn-4f9526e7e78b

```python
# First create string out of tokens
data['string'] = [[] for _ in range(len(data))]
for i in range(len(data)):
    data['string'].values[i] = ' '.join(data['tokens'].values[i])
    
# Code from : https://medium.com/analytics-vidhya/demonstrating-calculation-of-tf-idf-from-sklearn-4f9526e7e78b
# Using sklearn is much faster than manually creating the matrices 
cv = CountVectorizer()
word_count_vector = cv.fit_transform(data['string'])
tf = pd.DataFrame(word_count_vector.toarray(), columns=cv.get_feature_names())

tfidf_transformer = TfidfTransformer()
X = tfidf_transformer.fit_transform(word_count_vector)
idf = pd.DataFrame({'feature_name':cv.get_feature_names(), 'idf_weights':tfidf_transformer.idf_})

tf_idf = pd.DataFrame(X.toarray() ,columns=cv.get_feature_names())
```

```python
# Now make dictionary with token:TF-IDF values for each law
tfidf = [{} for x in range(len(data))]
for i in range(len(data)):
    for t in set(data['tokens'].values[i]):
        tfidf[i][t] = tf_idf.loc[i][t]

# Save TF-IDF data as compressed bz2 pickle file
# with bz2.BZ2File('data/tfidf' + '.pbz2', 'w') as f:
#     cPickle.dump(tfidf, f)
```
#### Text analysis


After processing the text we could evaluate the corpus of processed text which consists a total of 6,286,773 words and 55,675 unique words. 
The number of words in the laws varies greatly with the minimum and maximum being 8 and 157,473 and the median 758. The shortest laws are just proposing to ratify an earlier proposition, and these will of course not add much information. There are only 1.6% of the laws have under 50 words after processing, so this does not seem to be a problem. When inspecting the histogram of number of words per law, we see big difference in length, but only focusing on laws under 1000 words confirms that most low word count laws are above 100.

```python
# Creating processed corpus text and some basic stats
clean_corpus = []
for i in range(len(data)):
    clean_corpus += (data['tokens'].values[i])

print(f"Number of words in corpus: {len(clean_corpus)}")
print(f"Number of unique words in corpus: {len(set(clean_corpus))}")
```

```python
# Text statistics
word_count_per_law= pd.DataFrame([len(w) for w in data['tokens']], columns =['Wordcount per law'])
print(f"Law with the maximum wordcount in corpus: {data['title'].loc[word_count_per_law['Wordcount per law'].idxmax()]}, with {max(word_count_per_law['Wordcount per law']):d} words.")
print(f"Law with the maximum wordcount in corpus: {data['title'].loc[word_count_per_law['Wordcount per law'].idxmin()]}, with {min(word_count_per_law['Wordcount per law']):d} words.")
print(f"Median word count in laws: {word_count_per_law['Wordcount per law'].median():.0f} words.")
print(f"Percentage of laws with less than 50 words: {len([w for w in word_count_per_law['Wordcount per law'] if w < 50])/len(word_count_per_law):.1%}")
```

```python
# Histogram wordcount across documents in corpus
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
word_count_per_law.plot.hist(ax=ax[0], column='Wordcount per law', bins=25, grid=True, figsize=(10,8), color='maroon', log=True)
ax[0].set_title('Log scale histogram of wordcount per law', fontsize=12)
ax[0].set_xlabel('Wordcount')
ax[0].set_ylabel('Laws')
ax[0].get_legend().remove()

word_count_per_law[word_count_per_law['Wordcount per law'] < 1000].plot.hist(ax=ax[1], column='Wordcount per law', bins=25, grid=True, figsize=(10,8), color='maroon', log=True)
ax[1].set_title('Log scale histogram of wordcount up to 1000 per law', fontsize=12)
ax[1].set_xlabel('Wordcount')
ax[1].set_ylabel('Laws')

ax[1].get_legend().remove()

plt.suptitle('Wordcount per law', fontsize=16)
# fig.savefig('static/images/word_count_per_law.png')
plt.show()
```

When inspecting the top 25 word frequency across corpus on the processed text, we see that “fare” is number 1 and “person” is number 6, which resonates with the Corona pandemic of danger to individuals.

```python
# Cumulative word frequency distributions for corpus
word_count_clean = nltk.FreqDist(clean_corpus)
fig = plt.figure(figsize=(20, 10))
word_count_clean.plot(25,cumulative=True, title='Top 25 Cumulative word frequency distributions for corpus')
plt.show()
# fig.savefig('static/images/cumulative_word_frequency_corpus.png')
```

#### Generate Wordclouds

```python
# Generate wordclouds based on TF-IDF values
wordcloud_data = []
for i in range(len(data)):
    wordcloud = WordCloud(background_color='white', width=600, height=400).generate_from_frequencies(tfidf[i])
    plt.figure(figsize=[15, 10])
    plt.imshow(wordcloud)
    plt.axis("off")
    filename = 'plots/wordclouds/'+str(data['id'].values[i])+'.png'
    wordcloud_data.append([data['id'].values[i], filename])
    print("Saving file nr.",i,filename)
    plt.savefig(filename, bbox_inches='tight',pad_inches = 0)
    plt.close()
```

#### Evalution of text processing and Worcloud generation


Below we see an example of a Wordcloud and it shows that the lemmatization was not succesful in all accounts. The words "registrere", "registrering" and "offentligøre", "offentligørelse" should not have been seperate words, but otherwise the Wordcloud iseems representative for the law: "Bekendtgørelse af lov om visse erhvervsdrivende virksomheder".

```python
Image(filename='../plots/wordclouds/219731.png') 
```

## Network analysis

```python
import pandas as pd
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman
import matplotlib.pyplot as plt
import netwulf as nw
import bz2
import pickle
import _pickle as cPickle
data = bz2.BZ2File('../data/picl_data.pbz2', 'rb')
data = cPickle.load(data)
```

## Create graph

```python
# Simple helper function for loading and writing processed data
def read(lvl):
    df = bz2.BZ2File(f'data/picl_data_l{lvl}.pbz2', 'rb') # Or data/urls_l1.pkl
    df = cPickle.load(df)
    url = pd.read_pickle(f'data/urls_l{lvl}.pkl')
    return df, url

def write(df):
    with bz2.BZ2File(f'data/picl_data_final__.pbz2', 'w') as f:
        cPickle.dump(df, f)
```

##### Graph builder
Pandas library is convenient for making effecient lookups and condition to find edges to existing nodes

```python
'''
This functions builds the graphs, one for graphs with historic nodes and referrences and one without
'''
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
```

```python
'''
interEdges() is build to be able to read out the number of edges between the three levels
It is used in this way: 
dfSelfEdges{LVL} = interEdges(df.loc[df['rlvl'] == {LVL}], df.loc[df['rlvl'] == {LVL}])
nodeAttr() handles adding attribute data from our dataset
exclusive() was created to handle i mishab when initially concattenating the three levels without preserving the 
level attribute.
Fixing the mishab is done with these following self-explanatory lines of code:
    df1, _ = read(1)
    df2, _ = read(2)
    df3, _ = read(3)
    dfe2 = exclusive(df1, df2)
    dfe3 = exclusive(dfe2, df3)
    df1['rlvl'] = 1
    dfe2['rlvl'] = 2
    dfe3['rlvl'] = 3
    df = pd.concat([df1,dfe2,dfe3])
    df = df.drop_duplicates(subset=["id"])
    write(df)
'''
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

```

```python
G = nx.DiGraph()

idToIndexMapper = {}

uniqueIndex = 0

for index, row in data.iterrows():
    parent_id = getIdFromUrl(row.url)
    if parent_id not in idToIndexMapper:
        idToIndexMapper[parent_id] = {"indexInGraph": uniqueIndex, "url": row.url}
        uniqueIndex += 1
    edges = row["metadata"]
    for edge in edges:
        for key in edge:
            edge_id = getIdFromUrl(key)
            if edge_id not in idToIndexMapper:
                idToIndexMapper[edge_id] = {"indexInGraph": uniqueIndex, "url": edge}
                uniqueIndex += 1
            G.add_edge(idToIndexMapper[parent_id]["indexInGraph"], idToIndexMapper[edge_id]["indexInGraph"])

nx.draw(G)
```

```python
sorted(G.degree, key=lambda x: x[1], reverse=True)

for key in idToIndexMapper:
    if idToIndexMapper[key]["indexInGraph"] == 91:
        print("Highest degree", idToIndexMapper[key])

```

## Find communites

```python
communities = girvan_newman(G, most_valuable_edge=None)
node_groups = []
for com in next(communities):
    node_groups.append(list(com))

colors = ['blue', 'green', 'yellow', 'red', "cyan", "magenta", "#B23AEE", "#B4EEB4", "#FF1493", "#FFF68F"]
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
        print("sdfsd")
        color_map[node](colors[color_index])

nx.set_node_attributes(G, color_map, "group")

```

```python
nw.visualize(G)
```

<!-- #region -->
# Discussion

1. What went well?,
   * We believe, despite the huge potential for improvement, that the initial pitch for building the pandemic themes 
     Retsinfo network has been realized and the guestimated structure of the network was very close to the graphs 
     presented.
   * Our dataloader, altough a significant resource hog for us as developers, proved its worth by being very 
     resillient to changes and new ideas to include in the returned dataframe. - Creating an asyncronous web 
     scraping class from the ground was from the perspective of on of the authors a very rewarding learning experience
   * The libraries and their contributors used in this project definately needs a mentioning. Especially core python 
     developers for including very detailed but still simplistic examples for the asyncio library, but also Pandas and 
     networkx 
     needs a 
     mention. 
     Without pandas, performing simple conditial lookups between 
     referrences of edge 
     url's to match the unique Eli Url and in turn then the document id which was used to name the nodes, would have 
     required lots of development and custom function would never have been able to process at the speeds that 
     Pandas dataframes achieves. Networkx is also a very user friendly library with many included helper function 
     even in variation different implementations provided many, often extremely simple options for adding nodes and 
     attributes aswell as edges from dict-of-dicts which was relatively simple to provide using Padndas.
   * Eli which is short for "European Law Institue" provides the layout that is used at the source which, 
     considering the wast amount of documents being processed, didn't seem to contain a single error making our work 
     that less cumbersome.
2. What is still missing? What could be improved?, Why?
   * Many things:
     * Better graph labelling description and possible tweaking the conditions to which document type is displayed 
        in graph - there 24 document types after level 3.
       * We've slightly implemented the use of network probertis i.e. configs for the netwulf library which should 
         produce more or less similar graphs, but the results is not entirely satisfying and more could be done as 
         well as returning figures to matplotlib to control and add more usefull plot legends. - 
     * More in-depth graph analysis.
       * Too much time was allocated to creating a resiliant model that, in all fariness, produces some really 
         sanitized results. A clean-up process which again was easy to verify using pandas wonderful library
       * Several other key graph algorithms could be implemented very easyli along with producing a set of random 
         networks based on average degree of the Retsinfo network, the cause of the lack of these is simply poor 
         resource management, one of which was spent going down a rabit hole trying to implement a library to create 
         a database made by a fellow Danish analysts but none the less a library that did not work - possibly 
         because of recent changes to the source.


   * There's a lot of things to work on, and with the libraries mentioned and our experience creating a data 
     scraping tool 
     from scratch there's much potential for extending the project to other topic key-words, internatial 
     implementations for comparing documents between other and multiple countries.  
       * A "paragraph-in-document"-as-nodes-network effectively increasing resolution of the referrences law specifics.
       * Utilizing the shortNames referrences in the "[DK]: Ændrer i/ophæver" portion of the rendered site enabling us to distinguish between simple referrences and actual ammendments made by the document.
<!-- #endregion -->

```python

```
