import requests
import urllib.parse

from httphmac.request import Request
from httphmac.v2 import V2Signer as Signer

import hashlib
import uuid
import json

class ContentHub:

    def __init__(self, host):
        self.host = host
        self.session = requests.Session()
        self.responses = []
        self.max_response_stack = 10
        self.pub_key = None
        self.secret_key = ""
        self.signer = Signer(hashlib.sha256)

    def save_stack(self, response):
        if self.max_response_stack > len(self.responses):
            del(self.responses[0])
        self.responses.append(response)


    def send(self, url, method, client_id = None, body = None):

        auth = {
            "id": self.pub_key,
            "nonce": uuid.uuid4(),
            "realm": "Plexus",
            "version": "2.0",
        }

        request = Request().with_method(method).with_url(url).with_time()
        if client_id is not None:
            request.with_header("X-Acquia-Plexus-Client-Id", client_id)
        if body is not None:
            databytes = body.encode('utf-8')
            request.with_json_body(databytes)
        self.signer.sign_direct(request, auth, self.secret_key)
        response = request.do()
        return response


    def ping(self):
        url = urllib.parse.urljoin(self.host, "ping")
        r = self.session.get(url)
        self.save_stack(r)
        if r.status_code != 200:
            return False
        return True

    def register_client(self, name):
        "Returns a client with name and uuid"
        url = urllib.parse.urljoin(self.host, "/register")

        data = {
            "name": name,
        }
        r = self.send(url, "POST", None, json.dumps(data))
        if r.status_code != 200:
            print("register:", r, r.text)
            return False
        client_data = json.loads(r.text)
        client = Client(self, client_data["uuid"], client_data["name"])
        return client


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
