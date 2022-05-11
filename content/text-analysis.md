---
title: Text analysis
prev: network-analysis
next: future-perspectives
---
In order to understand the data, one needs to understand the content. To present the law text it in a concise mannerWordclouds will be used to quickly grasp what the content of the law is about. 

## Text processing
To represent the large body of text in the laws with only the most meaningful words in a wordcloud, the text was processed in the following workflow:
- Remove formatting, punctuation and numbers.
- Lemmatization of the words to express each word in its dictionary form, in order to reduce the amount of words with the same meaning.
- Remove stopwords and words with only 1 character, which does not add meaning to the wordcloud representation, including Danish law specific words such as: stk, nr, pkt, jf.
- In order to only capture words which are most representative of each law in the corpus, a TF-IDF value for each word was calculated.

[See explainer notebook for more information](/explainer-notebook.html)

## Analysis of the text

The corpus of 1601 law texts consists after processing a total of 6,286,773 words and 55,675 unique words. 
The number of words in the laws varies greatly with the minimum and maximum being 8 and 157,473 and the median 758. THe shortest laws are just proposing to ratify an earlier proposition, and these will of course not add much information. There are only 1.6% of the laws have under 50 words after processing, so this does not seem to be a problem. When inspecting the histogram of number of words per law, we see big difference in length, but only focusing on laws under 1000 words confirms that most low word count laws are above 100.

![Wordcloud|100%](/images/word_count_per_law.png)

When inspecting the top 25 word frequency across corpus on the processed text, we see that "fare" is number 1 and "person" is number 6, which resonates with the Corona pandemic of danger to individuals.

![Cumulative word frequency for corpus|150%](/images/cumulative_word_frequency_corpus.png)


## Wordclouds
Below is an example wordcloud representing the law "Lov om arbejdsgiveres adgang til at pålægge lønmodtagere forevisning af coronapas, test for covid-19 m.v". We see that it contains the most prominent words "test", "coronapas", arbejdsgiver", "ansat", "forevisning", "pålægge" which captures the essence of employers being able to require that employees present their Coronapas at the workplace.

![Wordcloud|100%](/images/226405.png)

[Source:https://www.retsinformation.dk/eli/lta/2021/2098](https://www.retsinformation.dk/eli/lta/2021/2098)




