class DatabasePopulator:

    def __init__(
            self,
            pickled_database
    ):
        self._db = pickled_database

    def get_replacement(
            self,
            key,
            default_value=None,
            convert_fn=str,
    ):
        if self._db.is_set(key):
            value = self._db.get(key)
        elif default_value is not None:
            value = default_value
        else:
            raise KeyError("No key found and no default value provided")

        return convert_fn(value)
