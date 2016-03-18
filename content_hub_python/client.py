try:
    import urllib.parse as urlparse
except:
    import urlparse as urlparse
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

        self.connector = connector;
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
        if uuid is not None:
            uuid = int(uuid)
        url = urlparse.urljoin(self.connector.host, "/entities")
        if uuid:
            url = urlparse.urljoin(url, "/" + str(uuid))
            if all_revision:
                url = urlparse.urljoin(url, "/revisions")

        r = self.connector.send(url, "GET", self.id)
        if r.status_code != 200:
            raise HttpError(r)
        return r.text

    def create_entities(self, entity):
        '''
        Creates one or more entity in Content Hub
        :param entity: Raw CDF that lists all entities to upload
        :return:
        '''
        url = urlparse.urljoin(self.connector.host, "/entities")

        r = self.connector.send(url, "POST", self.id, entity)
        if r.status_code != 202:
            raise HttpError(r)
        return r.text

    def update_entities(self, entities, uuid=None):
        '''
        Updates one or more entities
        :param entities: Updated entities in a raw CDF
        :param uuid: If set only only the entitiy with that uuid will be updated.
        If set, "entities" can only contain one entity, and unchanged fields can be omitted.
        :return:
        '''
        if uuid is not None:
            uuid = int(uuid)
        url = urlparse.urljoin(self.connector.host, "/entities")

        if uuid:
            url = urlparse.urljoin(url, "/" + str(uuid))
        r = self.connector.send(url, "PUT", self.id, entities)
        if r.status_code != 202:
            raise HttpError(r)
        return r.text

    def delete_entity(self, uuid):
        '''
        Deletes an entity.
        :param uuid: Uuid of the entity to be deleted.
        :return: True if succesful
        '''
        uuid = int(uuid)
        url = urlparse.urljoin(self.connector.host, "/entities/" + str(uuid))

        r = self.connector.send(url, "DELETE", self.id)
        if r.status_code != 202:
            raise HttpError(r)
        return True

    def search(self, search):
        '''
        Performs a search on content hub's elasticsearch cluster.
        :param search: An elasticsearch search in json
        :return: Result from elasticsearch in json
        '''
        url = urlparse.urljoin(self.connector.host, "/_search")

        r = self.connector.send(url, "POST", self.id, search)
        if r.status_code != 200:
            raise HttpError(r)
        return r.text

    def get_settings(self):
        '''
        Returns information about the current subscription
        '''
        url = urlparse.urljoin(self.connector.host, "/settings")

        r = self.connector.send(url, "GET", self.id)
        if r.status_code != 200:
            raise HttpError(r)
        return r.text
