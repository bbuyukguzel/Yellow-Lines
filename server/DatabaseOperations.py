from pymongo import MongoClient
from pymongo import errors
from functools import wraps


class DatabaseOperations:
    def __init__(self):
        self._client = ''
        self._database = ''
        self._collection = ''
        self.__establish_connection()

    def __establish_connection(self):
        self._client = MongoClient('mongodb://localhost:27017/')
        self. _database = self._client['yellowdb']
        self._collection = self._database['yellowcollection']

    def is_connected(self):
        try:
            self._client.server_info()
            return True
        except errors as err:
            # TODO: think later
            pass
        return False

    def connection_required(fn):
        @wraps(fn)
        def wrap(self, *args, **kwargs):
            if self.is_connected():
                return fn(self, *args, **kwargs)

        return wrap

    @connection_required
    def insert_new_task(self, json_data):
        self._collection.insert_one(json_data)
