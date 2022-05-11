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
    #retsinfo = Retsinfo(level=level, batchsize=batchsize, Timeout=190, workers=16, edges=True)  # mode=dev)
    #asyncio.run(retsinfo.main())
    #df, url = asyncio.run(retsinfo.main())
    # df, url = read(level)
    #df = asyncio.run(retsinfo.main())

    #res = retsinfo.write()
    #res.edgesUrl.explode().to_pickle("data/urls_l2.pkl")

    # with closing(asyncio.get_event_loop()) as loop:
#res.edgesUrl.size()