class Search:
    def __init__(self, url, description):
        self.url = url
        self.description = description

    def to_dict(self):
        return self.__dict__