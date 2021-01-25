from typing import List

# Originally this line was "from src.document .."
# Deleted "src." because it cannot be found. Now the code
# works without error. 
from document import Document

import json

import pprint

from googleapiclient.discovery import build



def get_results(query: List[str]) -> List[Document]:
    """
    Search the query using Google Engine and return list of document objects
    """
    ret = []

    if len(query) == 0:
      return []
    
    concat_query = ' '.join(query)

    service = build("customsearch", "v1",
            developerKey="AIzaSyAXqKtB1mQUHZmrFmMW_EhNK3JAyWRAK9o")

    res = service.cse().list(
      q = concat_query,
      cx = '2c6600e3a2ae8bcd0',
    ).execute()

    list_of_results = res['items']

    for item in list_of_results:
      title = item["title"]
      url = item["link"]
      desc = item["snippet"]

      doc = Document(title, url, desc)

      ret.append(doc)


    for item in ret:
      item.print_doc()
      
    return ret

    # json_object = json.loads(json.dumps(res['items'], indent = 4))

    # json_formatted_str = json.dumps(json_object, indent=2)

    # print(json_formatted_str)







# def main():
#   # Build a service object for interacting with the API. Visit
#   # the Google APIs Console <http://code.google.com/apis/console>
#   # to get an API key for your own application.

#   que = ["image", "processing"]

#   get_results(que)

# if __name__ == '__main__':
#   main()