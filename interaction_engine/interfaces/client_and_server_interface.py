from interaction_engine.messager.message import Message
from interaction_engine.interfaces.interface import Interface
from pickled_database import PickledDatabase


class ClientAndServerInterface(Interface):

    def __init__(
            self,
            multiple_choice_output_fn,
            multiple_choice_input_fn,
            direct_input_output_fn,
            direct_input_input_fn,
            pickled_database=None,
            is_create_db_key_if_not_exist=False,
    ):
        super().__init__(
            input_fn=self._message_fn_from_dict(
                {
                    Message.Type.MULTIPLE_CHOICE: multiple_choice_input_fn,
                    Message.Type.DIRECT_INPUT: direct_input_input_fn,
                }
            ),
            output_fn=self._message_fn_from_dict(
                {
                    Message.Type.MULTIPLE_CHOICE: multiple_choice_output_fn,
                    Message.Type.DIRECT_INPUT: direct_input_output_fn,
                }
            ),
            pickled_database=pickled_database,
            is_create_db_key_if_not_exist=is_create_db_key_if_not_exist
        )

        if (
                pickled_database is not None
                and not issubclass(pickled_database.__class__, PickledDatabase)
        ):
            raise TypeError
        self._db = pickled_database
        self._is_create_db_key_if_not_exist = is_create_db_key_if_not_exist

    @staticmethod
    def _message_fn_from_dict(dict):
        def _fn(msg: Message):
            return dict[msg.message_type](msg)
        return _fn
