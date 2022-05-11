---
title: Danish Legislation analysis
layout: single
next: data-description
---

<style>

h2{
    font-weight: 500;
}
.card {
  /* Add shadows to create the "card" effect */
    box-shadow: 0 6px 10px 0 rgba(0,0,0,0.3);
    transition: 0.3s;
    padding: 12px 20px;
    margin: 16px;
    border-radius: 15px;
}

/* On mouse-over, add a deeper shadow */
.card:hover {
  box-shadow: 0 12px 20px 0 rgba(0,0,0,0.3);
}

.cardContainer {
    display: flex;
    flex: row;
    flex-wrap: wrap;
    width: 100%;
}

/* Add some padding inside the card container */

</style>

Influenced by the corona pandemic, Danish lawmakers made amendments to existing laws and created new laws. By evaluating common links between all new laws containing "pandemic" keywords we seek to establish the one most relevant document for the creation of future laws. Although highly accessible, the Danish law may not be easily understood by everyone. Subjecting the documents to impartial and unbiased computer algorithms we seek to establish a logical chain of links and establish significant areas of importance in the Danish body of law.

## The project consists of three parts

<div class="cardContainer">
    <div class="card">
        <h2>Data</h2>
        <ul>
            <li>Collecting</li>
            <li>Pre-Processing</li>
        </ul>
        <a href="data-description">See more</a>
    </div>
    <div class="card">
        <h2>Network analysis</h2>
         <ul>
            <li>Network definition</li>
            <li>Centrality measures and communities</li>
        </ul>
        <a href="network-analysis">See more</a>
    </div>
    <div class="card">
        <h2>Text analysis</h2>
        <ul>
            <li>NLP Processing</li>
            <li>Wordclouds</li>
        </ul>
        <a href="text-analysis">See more</a>
    </div>
</div>

## We were able to identify the top 3 influental laws:

1: Bekendtgørelse af kildeskatteloven:
![Wordcloud|100%](/images/168178.png)


2: Lov om ændring af tinglysningsafgiftsloven og forskellige andre love og om ophævelse af lov om afgift af antibiotika og vækstfremmere anvendt i foderstoffer (Afgiftssaneringspakke m.v.):
![Wordcloud|100%](/images/206304.png)


3: Lov om ændring af registreringsafgiftsloven og forskellige andre love (Styrket regelefterlevelse på motorområdet, skærpet bødepraksis ved overtrædelse af registreringsafgiftsloven og øvrige punktafgiftslove og øvrige tilpasninger af reglerne på motorområdet)
![Wordcloud|100%](/images/211184.png)

<a href="future-perspectives">See more</a>

The code for fetching the data and doing the analysis can be found by clicking the bellow link:

## [Explainer Notebook](explainer-notebook.html)
