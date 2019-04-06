from pymongo import MongoClient
from pymongo import errors
from functools import wraps


class DatabaseOperations:
    def __init__(self):
        self._client = ''
        self._database = ''
        self._collection = ''
        self.__establish_connection()
        self.__mockdb = {'admin': 'admin'}

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
        try:
            result = self._collection.insert_one(json_data)
            return result.inserted_id
        except errors.WriteError as err:
            print('Task cannot be inserted to database')
            return None

    @connection_required
    def get_data(self, object_id, *keys):
        ret = {}
        document = self._collection.find_one({'_id': object_id})

        if document is not None:
            for key in keys:
                if key in document:
                    ret[key] = document[key]
                else:
                    print('Given key {} cannot be found in {}'.format(key, document))
        else:
            print('Given object {} cannot be found'.format(object_id))

        return ret

    def add_user(self, email, password):
        self.__mockdb[email] = password

    def get_user_details(self, email):
        if email in self.__mockdb:
            return self.__mockdb[email]
        else:
            return None
