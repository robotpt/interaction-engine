import json
import logging
import os

logging.basicConfig(level=logging.INFO)


class Database:

    def __init__(
            self,
            database_file_name
    ):

        self._database_file = self._make_sure_database_file_is_valid(
            database_file_name
        )

        if not os.path.exists(database_file_name):
            self._create_new_database_file(self._database_file)

        self._database = self._load_database_from_file(self._database_file)

    def _make_sure_database_file_is_valid(self, database_file_name):
        if type(database_file_name) is not str:
            raise TypeError("Not a valid file name.")

        if not database_file_name.endswith(".json"):
            raise TypeError("Must be a .json file.")

        return database_file_name

    def _check_default_database_keys(self, default_database_keys):
        if default_database_keys is not None:
            if type(default_database_keys) is not list:
                raise TypeError("Database keys must be a list.")
            for key in default_database_keys:
                if type(key) is not str:
                    raise TypeError("Database key must be a string.")

    def _load_database_from_file(self, db_file):
        with open(db_file) as f:
            try:
                database = json.load(f)
            except json.JSONDecodeError:
                logging.info("Error decoding JSON file, defaulting to empty database")
                database = {}
        return database

    def _create_new_database_file(self, database_file_name):
        directory = os.path.dirname(database_file_name)
        if directory != "":
            os.makedirs(directory, exist_ok=True)
        with open(self._database_file, "w"):
            self.save_to_database_file({})

    def __getitem__(self, item):
        return self._database[item]

    def __setitem__(self, key, value):
        if type(key) is not str:
            raise TypeError("Key must be a string.")
        if value is None:
            value = ""
        elif type(value) is not str:
            raise TypeError("Values must be a string.")
        self._database[key] = value
        self.save_to_database_file(self._database)

    def get_keys(self):
        return self._database.keys()

    def save_to_database_file(self, database):
        with open(self._database_file, "w") as f:
            json.dump(database, f)

    def clear_entire_database(self):
        for key in self._database:
            self.clear_value(key)

    def clear_value(self, key):
        self._database[key] = ""

    def reset_database(self):
        for key in self._database.keys():
            self.delete_key(key)

    def delete_key(self, key):
        try:
            self._database.pop(key)
        except KeyError as e:
            logging.info(e)
            pass
        self.save_to_database_file(self._database)

    def delete_database_file(self):
        os.remove(self._database_file)

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        if type(database) is not dict:
            raise TypeError("Database must be a dict.")
        self._database = database

    @property
    def database_file(self):
        return self._database_file
