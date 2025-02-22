from requests import Request, Session, post
from enum import Enum
from PIL import Image
import base64
# from shared import *

class Method(Enum):
    get = "GET"
    post = "POST"



class RequestBulder:

    def __init__(self):
        self._method: str | None = None
        self._url: str | None = None
        self._body: dict | None = None
        self._headers: dict | None = None
        self._params: dict | None = None
        self._file: dict | None = None

    def method(self, method: Method):
        self._method = method.value
        return self 
    
    def url(self, url: str):
        self._url = url
        return self 
    
    def params(self, params: dict):
        self._params = params
        return self 

    def body(self, body: dict):
        self._body = body
        return self
    
    def file(self, file: dict):
        self._file = file
        return self 
    
    def headers(self, headers: dict):
        self._headers = headers
        return self


    def build(self) -> Request :
          if not self._url:
            raise ValueError("URL이 설정되지 않았습니다.")
          
          match self._method:
            case "GET":
                return Request(method=self._method, url=self._url, headers=self._headers, params=self._params)
            case "POST":
                return Request(method=self._method, url=self._url, headers=self._headers, params=self._params ,data=self._body, files=self._file)

    