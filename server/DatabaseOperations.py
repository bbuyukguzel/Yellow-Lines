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
        self._tasks = self._database['tasks']
        self._users = self._database['users']

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
            result = self._tasks.insert_one(json_data)
            return result.inserted_id
        except errors.WriteError as err:
            print('Task cannot be inserted to database')
            return None

    @connection_required
    def get_data(self, object_id, *keys):
        ret = {}
        document = self._tasks.find_one({'_id': object_id})

        if document is not None:
            for key in keys:
                if key in document:
                    ret[key] = document[key]
                else:
                    print('Given key {} cannot be found in {}'.format(key, document))
        else:
            print('Given object {} cannot be found'.format(object_id))

        return ret

    @connection_required
    def add_user(self, email, password):
        try:
            result = self._users.insert_one({'email': email, 'password': password})
        except errors.WriteError as err:
            print('User cannot be inserted to database {}'.format(err))
            return None

    @connection_required
    def get_user_details(self, email):
        return self._users.find_one({'email': email})
