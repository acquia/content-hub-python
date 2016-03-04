import urllib.parse
# from .content_hub import ContentHub
from .common import HttpError

class Client:
    def __init__(self, connector, id, name):
        '''
        Constructor for the client.
        :param connector: A ContentHub instance that represents the Content Hub endpoint to work with.
        :param id: Uuid of the Client
        :param name: Name of the client
        '''

        self.connector = connector
        self.id = id
        self.name = name

    def get_entities(self, uuid=None, all_revision=False):
        '''
        Gets one or all entities from Content Hub.
        :param uuid: (optional) If set, only the entity with the given uuid will be returned.
        :param all_revision: If true, all revisions for the given entity will be returned.
        If False only the last one will be returned. Note that a true value is ignored if uuid is not set.
        :return: Raw CDF with all the returned entities.
        '''

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

    def update_entities(self, entities, uuid=None):
        uuid = int(uuid)
        url = urllib.parse.urljoin(self.connector.host, "/entities")

        if uuid:
            url = urllib.parse.urljoin(url, "/" + str(uuid))
        r = self.connector.send(url, "PUT", self.id, entities)
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
