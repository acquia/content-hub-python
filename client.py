import urllib.parse

class Client:
    def __init__(self, connector, id, name):
        self.connector = connector
        self.id = id
        self.name = name


    def list_from_cache(self):
        url = urllib.parse.urljoin(self.connector.host, "/entities")

        r = self.connector.send(url, "GET", self.id)
        if r.status_code != 200:
            return False
        return r.text
