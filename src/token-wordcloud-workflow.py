import nltk, re
import pandas as pd
# spacy has 219 danish stopwords as nltk only has 94
from spacy.lang.da.stop_words import STOP_WORDS
import lemmy
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import bz2
import pickle
import _pickle as cPickle
from wordcloud import WordCloud
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np

# Load data
data = bz2.BZ2File('data/picl_data_l3.pbz2', 'rb')
data = cPickle.load(data)

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

# Create string out of tokens
data['string'] = [[] for _ in range(len(data))]
for i in range(len(data)):
    data['string'].values[i] = ' '.join(data['tokens'].values[i])

# Calculate TF-IDF for each token
# Code from : https://medium.com/analytics-vidhya/demonstrating-calculation-of-tf-idf-from-sklearn-4f9526e7e78b
cv = CountVectorizer()
word_count_vector = cv.fit_transform(data['string'])
tf = pd.DataFrame(word_count_vector.toarray(), columns=cv.get_feature_names())

tfidf_transformer = TfidfTransformer()
X = tfidf_transformer.fit_transform(word_count_vector)
idf = pd.DataFrame({'feature_name':cv.get_feature_names(), 'idf_weights':tfidf_transformer.idf_})

tf_idf = pd.DataFrame(X.toarray() ,columns=cv.get_feature_names())

# Now make dictionary with token:TF-IDF value
tfidf = [{} for x in range(len(data))]
for i in range(len(data)):
    for t in set(data['tokens'].values[i]):
        tfidf[i][t] = tf_idf.loc[i][t]

# Save TF-IDF data as compressed bz2 pickle file
with bz2.BZ2File('data/tfidf' + '.pbz2', 'w') as f:
    cPickle.dump(tfidf, f)

# Creating processed corpus text and some basic stats
clean_corpus = []
for i in range(len(data)):
    clean_corpus += (data['tokens'].values[i])

print(f"Number of words in corpus: {len(clean_corpus)}")
print(f"Number of unique words in corpus: {len(set(clean_corpus))}")


# Cumulative word frequency distributions for corpus
word_count_clean = nltk.FreqDist(clean_corpus)
fig = plt.figure(figsize=(20, 10))
word_count_clean.plot(25,cumulative=True, title='Top 25 Cumulative word frequency distributions for corpus')
plt.show()
fig.savefig('static/images/cumulative_word_frequency_corpus.png')

# Text statistics
word_count_per_law= pd.DataFrame([len(w) for w in data['tokens']], columns =['Wordcount per law'])
print(f"Law with the maximum wordcount in corpus: {data['title'].loc[word_count_per_law['Wordcount per law'].idxmax()]}, with {max(word_count_per_law['Wordcount per law']):d} words.")
print(f"Law with the maximum wordcount in corpus: {data['title'].loc[word_count_per_law['Wordcount per law'].idxmin()]}, with {min(word_count_per_law['Wordcount per law']):d} words.")
print(f"Median word count in laws: {word_count_per_law['Wordcount per law'].median():.0f} words.")
print(f"Percentage of laws with less than 50 words: {len([w for w in word_count_per_law['Wordcount per law'] if w < 50])/len(word_count_per_law):.1%}")

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
fig.savefig('static/images/word_count_per_law.png')
plt.show()

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







