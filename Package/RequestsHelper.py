import requests
from Package.Utils import print_data

response = 'response'
request = 'request'
error = 'error'
access_token = 'access_token'


def make_request(url, method, params, files=None):
    r = requests.request(method, url, params=params, files=files)
    r.close()
    result = RequestResult(r)
    print_data(request, '===>', result.get_request_url())
    print_data(response, '<===', result.get_json())
    print()
    return result


class RequestResult:
    result = None

    def __init__(self, result):
        self.result = result

    def get_json(self):
        return self.result.json()

    def get_request_headers(self):
        return self.result.request.headers

    def get_response_url(self):
        return self.result.url

    def get_request_url(self):
        return self.result.request.url

    def get_text(self):
        return self.result.text

    def get_args(self):
        return self.get_json()["args"]

    def get_response_headers(self):
        return self.get_json()["headers"]
