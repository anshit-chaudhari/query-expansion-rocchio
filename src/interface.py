from typing import List
from .config import Config
from .document import Document
from .google_utils import get_results
from .brain import brain_func


class Session:
    def __init__(self, config: Config):
        self.config = config

    def __run_iteration(self, query: List[str]) -> (float, List[Document], List[Document]):
        # Query the search engine for results, and return them to get 
        # user relevance evaluation.

        relevant_docs = []
        irrelevant_docs = []
        docs = get_results(query, self.config)

        print("Google Search Results:")
        print("===========================")

        for i, doc in enumerate(docs):
            # For each document, get user relevance feedback,
            # then put the document in one of the two lists
            # according to the feedback.
            print('Result {}'.format(i + 1))
            doc.print()
            print("-----")

            # Collect feedback here
            collect_feedback(relevant_docs, irrelevant_docs, doc)

        precision = len(relevant_docs) / 10

        return precision, relevant_docs, irrelevant_docs

    def run(self):

        # Print out user provided parameters
        query = self.config.query
        precision = self.config.precision
        dev_key = self.config.dev_key
        engine_key = self.config.engine_key

        if precision < 0 or precision > 1:
            raise Exception("Usage: Precision must be greater than or equal to 0, smaller than or equal to 1.")


        # Loop to get results until precision is reached
        # or until precision is zero.
        while True:
            print("Parameters:")
            print("Client key = " + dev_key)
            print("Engine key = " + engine_key)
            print("Query = ", " ".join(query))
            print("Precision = ", precision)

            # Get query results
            cur_precision, relevant_docs, irrelevant_docs = self.__run_iteration(query)

            print("===========================")
            print("FEEDBACK SUMMARY")
            print("Query: ", " ".join(query))
            print("Precision: ", cur_precision)

            if cur_precision >= precision:
                print("Desired precision reached, done.")
                break

            elif cur_precision == 0:
                print("No relevant documents found. Terminating the program")
                break

            else:
                print("Still below the required precision of ", precision)

            # Augment the query
            query = brain_func(relevant_docs, irrelevant_docs, query, cur_precision)

            print("Augmenting by: " + query[-1])


def collect_feedback(relevant_docs: List[Document], irrelevant_docs: List[Document], doc: Document):
    if doc.title and doc.desc:
        f = input("Relevant (Y/N)?")

        while True:
            if f.lower() == 'y':
                relevant_docs.append(doc)
                return

            elif f.lower() == 'n':
                irrelevant_docs.append(doc)
                return

            else:
                print("Please answer \"y\" or \"n\".")
                f = input("Relevant (Y/N)?")

    else:
        # We found out that non-html pages do not have description (snippet). Also, without description (snippet) we
        # cannot meaningfully represent a page, hence we decided to ignore such pages in our computation. Thus, only the
        # pages with non-empty title and description will be processed. That said, such pages are extremely rare.
        print("Either/Both of title and description are missing. Not using this page in computation.")
