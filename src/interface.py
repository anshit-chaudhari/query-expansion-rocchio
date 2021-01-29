from typing import List

from .config import Config
from .document import Document
from .google_utils import get_results


class Session:
    def __init__(self, config: Config):
        self.config = config

    def __run_iteration(self, query: List[str]) -> (float, List[Document]):
        """
        Returns the precision and the relevant documents
        """

        relevant_docs = []
        docs = get_results(query, self.config)

        for i, doc in enumerate(docs):
            print('Result {}'.format(i))
            doc.print()
            print("-----")
            collect_feedback(relevant_docs, doc)

        # TODO: write logic to exclude non-html pages from this count
        precision = len(relevant_docs) / 10

        return precision, relevant_docs

    def run(self):
        query = input("Please input your query").split(" ")
        precision = float(input("What is your desired precision?"))
        cur_precision = 0

        while cur_precision < precision:
            cur_precision, relevant_docs = self.__run_iteration(query)
            # query = brain_func(relevant_docs)


def collect_feedback(relevant_docs: List[Document], doc: Document):
    f = input("Relevant (Y/N)?")

    if f.lower() == 'y':
        relevant_docs.append(doc)
