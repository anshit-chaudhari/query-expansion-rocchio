# Resource: https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76

from typing import List

from .config import Config
from .document import Document

from googleapiclient.discovery import build


def get_results(query: List[str], config: Config) -> List[Document]:
    """
    Search the query using Google Engine and return list of document objects
    """
    ret = []

    if len(query) == 0:
        return []

    concat_query = ' '.join(query)

    service = build("customsearch", "v1",
                    developerKey=config.dev_key)

    res = service.cse().list(
        q=concat_query,
        cx=config.engine_key,
    ).execute()

    list_of_results = res['items']

    list_of_results = list_of_results[0:10]

    for item in list_of_results:
        title = item.get("title", "")
        url = item.get("link", "")
        desc = item.get("snippet", "")

        doc = Document(title, url, desc)

        ret.append(doc)

    return ret
