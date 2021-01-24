from typing import List

# Originally this line was "from src.document .."
# Deleted "src." because it cannot be found. Now the code
# works without error. 
from document import Document

import json



def get_results(query: List[str]) -> List[Document]:
    """
    Search the query using Google Engine and return list of document objects
    """
    pass

print("I'm here")

import pprint

from googleapiclient.discovery import build


def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyAXqKtB1mQUHZmrFmMW_EhNK3JAyWRAK9o")

  res = service.cse().list(
      q='Linear Algebra Lectures',
      cx='2c6600e3a2ae8bcd0',
    ).execute()

  json_object = json.loads(res['items'][0])

  json_formatted_str = json.dumps(json_object, indent=2)

  print(json_formatted_str)
#   pprint.pprint(res)

if __name__ == '__main__':
  main()