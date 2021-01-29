from src import Config, Session

if __name__ == '__main__':
    config = Config(
        dev_key="AIzaSyAXqKtB1mQUHZmrFmMW_EhNK3JAyWRAK9o",
        engine_key="2c6600e3a2ae8bcd0"
    )

    Session(config).run()
