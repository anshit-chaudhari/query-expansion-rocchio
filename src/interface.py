from typing import List

from .config import Config
from .document import Document
from .google_utils import get_results
from .brain import brain_func


class Session:
    def __init__(self, config: Config):
        self.config = config

    def __run_iteration(self, query: List[str]) -> (float, List[Document], List[Document]):
        """
        Returns the precision and the relevant documents
        """

        relevant_docs = []
        irrelevant_docs = []
        docs = get_results(query, self.config)

        for i, doc in enumerate(docs):
            print('Result {}'.format(i))
            doc.print()
            print("-----")
            collect_feedback(relevant_docs, irrelevant_docs, doc)

        precision = len(relevant_docs) / 10

        return precision, relevant_docs, irrelevant_docs

    def run(self):
        query = input("Please input your query: ").split(" ")
        precision = float(input("Please enter your desired precision: "))

        while True:
            cur_precision, relevant_docs, irrelevant_docs = self.__run_iteration(query)
            print("Current precision: {}".format(cur_precision))

            if cur_precision >= precision:
                print("Current precision is greater than or equal to desired precision. Stopping iteration")
                break

            elif cur_precision == 0:
                print("No relevant documents found. Terminating the program")
                break

            query = brain_func(relevant_docs, irrelevant_docs, query)


def collect_feedback(relevant_docs: List[Document], irrelevant_docs: List[Document], doc: Document):
    f = input("Relevant (Y/N)?")

    if f.lower() == 'y':
        relevant_docs.append(doc)

    else:
        irrelevant_docs.append(doc)
