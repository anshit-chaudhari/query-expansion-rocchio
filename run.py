import sys

from src import Config, Session

if __name__ == '__main__':
    if len(sys.argv) != 5:
        raise Exception("Usage: python run.py <API Key> <Engine Key> <Precision> <Query>")

    config = Config(
        dev_key=sys.argv[1],
        engine_key=sys.argv[2],
        precision=float(sys.argv[3]),
        query=sys.argv[4].split(" ")
    )

    Session(config).run()
