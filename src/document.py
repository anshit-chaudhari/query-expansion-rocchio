class Document:
    def __init__(self, title: str, url: str, desc: str):
        self.title = title
        self.url = url
        self.desc = desc

    def print_doc(self):
        print("title: " + self.title)
        print("url: " + self.url)
        print("desc: " + self.desc)
        print("")

        # Constructed with basic fields. Add more if needed
