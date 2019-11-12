from interaction_engine.messager.message import Message
from robotpt_common_utils import lists, user_input
from pickled_database import PickledDatabase


class Interface:

    def __init__(
            self,
            multiple_choice_output_fn,
            multiple_choice_input_fn,
            direct_input_output_fn,
            direct_input_input_fn,
            error_output_fn=None,
            error_input_fn=None,
            pickled_database=None,
            is_create_db_key_if_not_exist=False,
    ):
        self._output_input_fns = {
            Message.Type.MULTIPLE_CHOICE: (
                multiple_choice_output_fn, multiple_choice_input_fn
            ),
            Message.Type.DIRECT_INPUT: (
                direct_input_output_fn, direct_input_input_fn
            )
        }

        if error_output_fn is None:
            error_output_fn = multiple_choice_output_fn
        self._error_output_fn = error_output_fn

        if error_input_fn is None:
            error_input_fn = multiple_choice_input_fn
        self._error_input_fn = error_input_fn

        if (
                pickled_database is not None
                and not issubclass(pickled_database.__class__, PickledDatabase)
        ):
            raise TypeError
        self._db = pickled_database
        self._is_create_db_key_if_not_exist = is_create_db_key_if_not_exist

    def run(self, message):

        if type(message) is not Message:
            raise ValueError("Must input message class")

        if message.message_type in self._output_input_fns:
            output_fn, input_fn = self._output_input_fns[message.message_type]
        else:
            raise KeyError(f"Message type '{message.message_type}' not found")

        output_fn(message)
        result_str = input_fn(message)

        # Rerun if user put in bad entry
        try:
            result = message.result_type(result_str)
            is_valid = self._do_tests_pass(message, result)
        except (ValueError, TypeError):
            is_valid = False
        if not is_valid:
            self.run(message.error_message)
            return self.run(message)

        # Ask if what user input is correct, if not rerun
        if message.is_confirm:
            confirm_message = Interface._get_confirm_message(result)
            is_confirmed_str = self.run(confirm_message)
            is_confirmed = user_input.is_yes(is_confirmed_str)
            if not is_confirmed:
                return self.run(message)

        # Write user input into the database
        key = message.result_db_key
        if (
                key is not None
                and self._db is not None
        ):
            if key not in self._db:
                if self._is_create_db_key_if_not_exist:
                    self._db.create_key(key)
                else:
                    raise KeyError(f"'{key}' doesn't exist in the database")

            if message.is_append_result:
                save_result = [result]
                if self._db.is_set(key):
                    save_result = self._db.get(key) + save_result
            else:
                save_result = result

            self._db.set(message.result_db_key, save_result)

        return result

    @staticmethod
    def _get_confirm_message(value):
        return Message(
            content=f"'{str(value)}', right?",
            options=['Yes', 'No'],
            message_type=Message.Type.MULTIPLE_CHOICE,
            result_convert_from_str_fn=str,
            is_confirm=False
        )

    @staticmethod
    def _do_tests_pass(message, result):
        if message.tests is not None:
            tests = lists.make_sure_is_iterable(message.tests)
            for test in tests:
                if test(result) is False:
                    return False
        return True

