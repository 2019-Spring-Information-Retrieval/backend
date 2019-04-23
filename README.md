# SayYourMoive



> **Content**
> 1. Introduce
> 
>
> 
> . Ranking


## Introduce


## 

## 

##


## Ranking


### TF-IDF & Cosine Similarity



Based on the indexing results of on title, plot and script, here we merge the results together and measure a rank of the search results. (refer to []())


For word frequency indexes, we use TF-IDF (skLearn) to measure the ranking scores; while for positional indexes, we use Cosine Similarity (numpy) to measure the ranking scores. (refer to []())


### Learning Index Weights

Based on the ranking scores of different indexes, we measure the weighted sum of ranking scores as the final ranking scores of every candidate search result. (refer to []())

We use Logistic Regression to learn the weights of every ranking score, where the loss function meansuring distance between target ranking order and predicted ranking order. (refer to []())


### Labs Features

In this project, we also explore some amazing features to boost the searching results, with the help of Neural Network.


#### Latent Answer Detecting

The feature of Latent Answer Detecing aiming to extract some valuable phrases from document, which would likely to be the potential answer of searching question, or related context of user-descripted conditions. The idea is simple that some phrases might be summarization or details for the whole text, which is more likely to be queried.

Given a text as input, the model will output a sequence of B-I-O labels for every token in the text. The phrase started with 'B' and ended with the last 'I' is taken as one valuable phrases. (trained model refer to []() and code refer to []())



#### Question Word Generating

The feature of Qustion Word Generating aiming to generate some complement words with query words, which would extend the original query words of searching. The idea is strainforwad that query words might be different to the expression of related content, which required to add more "guessing words" to search the target.

Given a short text as input, the model will output a list of predicted query words. The original words of input text and model-generated words will togather to treated as query words for searching. (code refer to []())






