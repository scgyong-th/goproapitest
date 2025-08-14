class HttpGetRequest:
    def __init__(self, path):
        self.path = path

    def toForwardPath(self):
        return f'/http{self.path}'

