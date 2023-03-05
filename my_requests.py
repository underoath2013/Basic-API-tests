import requests
from logger import Logger
from environment import ENV_OBJECT

class MyRequests():
    @staticmethod
    def post(url: str, data:dict = None, headers: dict = None, json: dict = None, cookies = None):
        return MyRequests._send(url, data, headers, json, cookies, "POST")

    @staticmethod
    def get(url: str, data:dict = None, headers: dict = None, json: dict = None, cookies = None):
        return MyRequests._send(url, data, headers, json, cookies, "GET")

    @staticmethod
    def put(url: str, data:dict = None, headers: dict = None, json: dict = None, cookies = None):
        return MyRequests._send(url, data, headers, json, cookies, "PUT")

    @staticmethod
    def delete(url: str, data:dict = None, headers: dict = None, json: dict = None, cookies = None):
        return MyRequests._send(url, data, headers, json, cookies, "DELETE")


    @staticmethod
    def _send(url: str, data:dict, headers: dict, json: dict, cookies:dict, method: str):
        
        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if headers is None:
            headers = {}
        if data is None:
            data = {}
        if json is None:
            json = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, json, cookies, method)

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, json=json, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, data=data, headers=headers, json=json, cookies=cookies) 
        elif method == 'PUT':
            response = requests.put(url, data=data, headers=headers, json=json, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, data=data, headers=headers, json=json, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")
        
        Logger.add_response(response)

        return response