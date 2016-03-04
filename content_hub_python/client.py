import urllib.parse
# from .content_hub import ContentHub
from .common import HttpError

class Client:
    def __init__(self, connector, id, name):
        self.connector = connector
        self.id = id
        self.name = name


    def get_entities(self, uuid = None, all_revision = False):
        uuid = int(uuid)
        url = urllib.parse.urljoin(self.connector.host, "/entities")
        if uuid:
            url = urllib.parse.urljoin(url, "/" + str(uuid))
            if all_revision:
                url = urllib.parse.urljoin(url, "/revisions")

        r = self.connector.send(url, "GET", self.id)
        if r.status_code != 200:
            raise HttpError(r)
        return r.text

    def create_entity(self, entity):
        url = urllib.parse.urljoin(self.connector.host, "/entities")

        r = self.connector.send(url, "POST", self.id, entity)
        if r.status_code != 202:
            raise HttpError(r)
        return r.text

    def delete_entity(self, uuid):
        uuid = int(uuid)
        url = urllib.parse.urljoin(self.connector.host, "/entities/" + str(uuid))

        r = self.connector.send(url, "DELETE", self.id)
        if r.status_code != 202:
            raise HttpError(r)
        return r.text
