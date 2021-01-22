# adv-db-proj-1
Advanced Databases Project 1

http://www.cs.columbia.edu/~gravano/cs6111/proj1.html

Project Description:
In this project, you will implement an information retrieval system that exploits user-provided relevance feedback to improve the search results returned by Google. The relevance feedback mechanism is described in Singhal: Modern Information Retrieval: A Brief Overview, IEEE Data Engineering Bulletin, 2001, as well as in Chapter 9, “Relevance Feedback & Query Expansion,” of the Manning, Raghavan, and Schütze Introduction to Information Retrieval textbook, available online.

User queries are often ambiguous. For example, a user who issues a query [jaguar] might be after documents about the car or the animal, and in fact search engines like Bing and Google return pages on both topics among their top 10 results for the query. In this project, you will design and implement a query-reformulation system to disambiguate queries and improve the relevance of the query results that are produced. Here’s how your system, which should be written in Python, should work:

Receive as input a user query, which is simply a list of words, and a value—between 0 and 1—for the target “precision@10” (i.e., for the precision that is desired for the top-10 results for the query, which is the fraction of pages that are relevant out of the top-10 results).
Retrieve the top-10 results for the query from Google, using the Google Custom Search API (see below), using the default value for the various API parameters, without modifying these default values.
Present these results to the user, so that the user can mark all the webpages that are relevant to the intended meaning of the query among the top-10 results. For each page in the query result, you should display its title, URL, and description returned by Google.
IMPORTANT NOTE: You should display the exact top-10 results returned by Google for the query (i.e., you cannot add or delete pages in the results that Google returns). Also, the Google Custom Search API has a number of search parameters. Please do not modify the default values for these search parameters.
If the precision@10 of the results from Step 2 for the relevance judgments of Step 3 is greater than or equal to the target value, then stop. If the precision@10 of the results is zero, then you should also stop. Otherwise, use the pages marked as relevant to automatically (i.e., with no further human input at this point) derive new words that are likely to identify more relevant pages. You may introduce at most 2 new words during each round. 
IMPORTANT NOTE 1: You cannot delete any words from the original query or from the query from the previous iteration; you can just add words, up to 2 new words in each round. Also, your queries must consist of just keywords, without any additional operators (e.g., you cannot use negation, quotes, or any other operator in your queries). 
IMPORTANT NOTE 2: The order of the words in the expanded query is important. Your program should automatically consider the alternate ways of ordering the words in a modified query, and pick the order that is estimated to be best. In each iteration, you can reorder all words—new and old—in the query, but you cannot delete any words, as explained in the note above.
Modify the current user query by adding to it the newly derived words and ordering all words in the best possible order, as determined in Step 4, and go to Step 2.
The key challenge in the project is in designing Step 4, for which you should be creative and use the ideas that we discussed in class—as well as the above bibliography and the course reading materials—as inspiration. You are welcome to borrow techniques from the research literature at large (either exactly as published or modified as much as you feel necessary to get good performance in our particular query setting), but make sure that you cite the specific publications on which you based your solution. As a hint on how to search for relevant publications, you might want to check papers on “query expansion” in the main IR conference, SIGIR, at https://dblp.uni-trier.de/db/conf/sigir/index.html. If you choose to implement a technique from the literature, you still need to make sure that you adapt the chosen technique as much as necessary so that it works well for our specific query setting and scenario, since you will be graded based on how well your technique works. If you want to do stopword elimination (this is of course optional), you can find a list of stopwords here.

You will use the Google Custom Search API (https://developers.google.com/custom-search/) in this project: this is Google’s web service to enable the creation of customized search engines. Furthermore, the code that you submit for your project must run on the Google Cloud, so it is a good idea to develop your code on a VM on the Google Cloud from the very beginning (see below), rather than writing it on a different platform and then adapting it to the Google Cloud for submission.

As a first step to develop your project, you should set up your Google Cloud account carefully following our instructions provided here. Our instructions also explain how you should set up a VM on the cloud, to develop and run your project. Please make sure that you do all this over your Lionmail account, not your personal Gmail account.

As a second step, you will have to sign up for the Programmable Search Engine service (https://programmablesearchengine.google.com/about/):

Log off from all Gmail/Google accounts and then log on only your Lionmail account. (Google doesn't let you switch between accounts when you are setting up a Google Programmable Search Engine service.)
Press the "Get Started" button on the top right corner.
Create a new search engine by clicking the “New search engine” button on the top left corner.
Specify the following field values:
“Sites to search” should be "www.wikipedia.com" for now
“Language” should be "English"
“Name of search engine” should be "cs6111"
Press the “CREATE” button.
Select “Edit search engine” on the left, choose search engine “cs6111,” and click "Setup."
Under the top “Basics" button, turn on the "Search the entire web" button.
Under the top "Basics" button, under the "Sites to search" heading, select the "www.wikipedia.com" site and press the “Delete” button. This will enable the creation of a search engine to search the entire web but without an emphasis on any particular website (i.e., you will be using the general Google search engine).
Copy your “Search engine ID,” which you will need for querying.
Do not modify or change other settings.
Check the Google Custom Search JSON API documentation and obtain a JSON API key by clicking on "Get a Key"; you will have to select the Google Cloud project that you have already created using our instructions above.
You will use your search engine ID, your JSON API key, and a query as parameters to encode a search request URL. When requested from a web browser, or from inside a program, this URL will return a document with the query results. Please refer to the Google Custom Search JSON API documentation for details on the URL syntax and document schema. You should parse the response document in your program to extract the title, link, and description of each query result, so you can use this information in your algorithm. Here is a Python example of use of the Google Custom Search API that should be helpful: example (note that q refers to your query, developerKey refers to your Google Custom Search API key, and cx refers to your search engine ID).

By default, the Google Custom Search JSON API has a quota of 100 queries per day for free. Additional requests cost $5 per 1,000 queries, which will be deducted from the coupon credit that Columbia provided to you (see above). Please refer to the JSON API documentation for additional details, which you should check carefully to avoid billing-related surprises.