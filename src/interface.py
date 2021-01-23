from typing import List

from src.document import Document


class Config:
    def __init__(self, precision: float, client_key: str, engine_key: str):
        self.precision = precision
        self.client_key = client_key
        self.engine_key = engine_key


class Session:
    def __init__(self, config: Config, initial_query: List[str]):
        self.config = config
        self.initial_query = initial_query

    def __run_iteration(self, query: List[str]) -> (float, List[Document]):
        """
        Returns the precision and the relevant documents
        """

        relevant_docs = []
        docs = []
        # docs = fetch documents from Google utils

        for i, doc in enumerate(docs):
            display_result(i, doc)
            collect_feedback(relevant_docs, doc)

        # TODO: write logic to exclude non-html pages from this count
        precision = len(relevant_docs) / 10

        return precision, relevant_docs

    def run(self):


def display_result(i: int, doc: Document):
    print('Result {}'.format(i))
    print('[')
    print(' URL: {}'.format(doc.url))
    print(' Title: {}'.format(doc.title))
    print(' Summary: {}'.format(doc.desc))
    print(']')


def collect_feedback(relevant_docs: List[Document], doc: Document):
    f = input("Relevant (Y/N)?")

    if f.lower() == 'y':
        relevant_docs.append(doc)
