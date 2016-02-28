import requests
import urllib.parse

from httphmac.request import Request
from httphmac.v2 import V2Signer as Signer

import hashlib
import uuid

class ContentHub:

    def __init__(self, host):
        self.host = host
        self.session = requests.Session()
        self.responses = []
        self.max_response_stack = 10
        self.client_id = ""
        self.secret_key = ""
        self.signer = Signer(hashlib.sha256)

    def save_stack(self, response):
        if self.max_response_stack > len(self.responses):
            del(self.responses[0])
        self.responses.append(response)


    def send(self, url, method, body = None):

        auth = {
            "id": "Access-key",
            "nonce": uuid.uuid4(),
            "realm": "Plexus",
            "version": "2.0",
        }

        request = Request().with_method(method).with_url(url).with_time()
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


    def list_from_cache(self):
        url = urllib.parse.urljoin(self.host, "/entities")

        r = self.send(url, "GET")
        self.save_stack(r)
        if r.status_code != 200:
            return False
        return r.text

