# adv-db-proj-1
Advanced Databases Project 1

### Project Description

http://www.cs.columbia.edu/~gravano/cs6111/proj1.html

### Install

After cloning this project on your machine, you should run the commands below

```{bash}
pip3 install -r requirements.txt
python3 -m nltk.downloader stopwords punkt
```

### Run

```{bash}
python3 run.py <API Key> <Engine Key> <Precision> <Query>
```

Use the API and Engine Key below
```
API Key: AIzaSyAXqKtB1mQUHZmrFmMW_EhNK3JAyWRAK9o
Engine Key: 2c6600e3a2ae8bcd0
```

### Algorithm

Once we have a list of relevant documents and a list of irrelevant documents, we will extract the title and snippet of 
each document. The title + snippet string is viewed as the entire document. 

We then calculate the tf-idf vector for all the documents and the query. We do this calculation after doing some simple string formatting first,
such as eliminating non-alphabetical characters and eliminating stop words. If a document is missing a title or a snippet, we do not consider them in the query update process. This means that non-html documents or broken documents are not used to update the query, even though we do ask the user to provide feedbacks on them to calculate the precision. 

Once we have the tf-idf vector for each document and the query, we will use Rocchio's algorithm to obtain a new qeury vector. 
The code for implementing Rocchio's algorithm is obtained from this website: 
https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
We are using the Sklearn package which has built in functions to do such calculations. 

Once we obtain a new query vector, we will calculate the difference between the new query vector and the old one. We will identify
the word with the biggest positive change in its value. In other words, we are finding the direction in which the query vector 
has moved the most. The word corresponding to that direction is the new query word. We only add one new word at a time, and 
we simply append them without any orderings.
