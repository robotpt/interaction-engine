from pickled_database import PickledDatabase
from interaction_engine.text_populator.base_populator import BasePopulator


class DatabasePopulator(BasePopulator):

    class Tags:
        MAIN = 'db'
        POST_OP = 'post-op'
        DEFAULT_VALUE = 'default value'

    def __init__(
            self,
            database,
    ):

        super().__init__(
            main_tags=[self.Tags.MAIN],
            option_tags=[
                self.Tags.POST_OP,
                self.Tags.DEFAULT_VALUE
            ]
        )

        if type(database) is str:
            self._db = PickledDatabase(database)
        else:
            self._db = database

    _common_fns = {
        'increment': lambda x: x+1,
        'decrement': lambda x: x-1,
    }

    def get_replacement(
            self,
            key,
            default_value=None,
            convert_fn=str,
            modify_before_resaving_fn=None,
    ):
        if self._db.is_set(key):
            value = self._db.get(key)
        elif default_value is not None:
            value = default_value
        else:
            raise KeyError("No key found and no default value provided")

        if modify_before_resaving_fn is not None:
            if modify_before_resaving_fn in DatabasePopulator._common_fns:
                modify_before_resaving_fn = DatabasePopulator._common_fns[modify_before_resaving_fn]
            new_value = modify_before_resaving_fn(value)
            self._db.set(key, new_value)

        return convert_fn(value)

    def __contains__(self, key):
        return key in self._db