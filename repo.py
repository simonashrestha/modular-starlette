from abc import ABC, abstractmethod
from starlette.requests import Request

class AbstractRepository(ABC):
    @abstractmethod
    def post(self, request: Request):
        raise NotImplementedError()
    @abstractmethod
    def get(self, request: Request):
        raise NotImplementedError()
    @abstractmethod
    def put(self, request: Request):
        raise NotImplementedError()
    @abstractmethod
    def delete(self, request: Request):
        raise NotImplementedError() 

class AbstractRepositoryforUser(ABC):
    @abstractmethod
    def register(self, request: Request):
        raise NotImplementedError()