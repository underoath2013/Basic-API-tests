import requests
from logger import Logger
from environment import ENV_OBJECT

class MyRequests():
    @staticmethod
    def post(url: str, data:dict = None, headers: dict = None):
        return MyRequests._send(url, data, headers, "POST")

    @staticmethod
    def get(url: str, data:dict = None, headers: dict = None):
        return MyRequests._send(url, data, headers, "GET")

    @staticmethod
    def put(url: str, data:dict = None, headers: dict = None):
        return MyRequests._send(url, data, headers, "PUT")

    @staticmethod
    def delete(url: str, data:dict = None, headers: dict = None):
        return MyRequests._send(url, data, headers, "DELETE")


    @staticmethod
    def _send(url: str, data:dict, headers: dict, method: str):
        
        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if headers is None:
            headers = {}
        if data is None:
            data = {}

        Logger.add_request(url, data, headers, method)

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers)
        elif method == 'POST':
            response = requests.post(url, data=data, headers=headers) 
        elif method == 'PUT':
            response = requests.put(url, data=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, data=data, headers=headers)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")
        
        Logger.add_response(response)

        return response