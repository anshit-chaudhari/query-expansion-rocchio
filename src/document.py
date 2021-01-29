class Document:
    def __init__(self, title: str, url: str, desc: str):
        self.title = title
        self.url = url
        self.desc = desc

    def print(self):
        print('[')
        print(' URL: {}'.format(self.url))
        print(' Title: {}'.format(self.title))
        print(' Summary: {}'.format(self.desc))
        print(']')

        # Constructed with basic fields. Add more if needed
