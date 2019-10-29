from data_structures import Message
from robotpt_common_utils import lists, user_input


class Interface:

    def __init__(
            self,
            multiple_choice_output_fn,
            multiple_choice_input_fn,
            direct_input_output_fn,
            direct_input_input_fn,
            error_output_fn=None,
            error_input_fn=None,
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

    def run(self, message):

        if type(message) is not Message:
            raise ValueError("Must input message class")

        if message.message_type in self._output_input_fns:
            output_fn, input_fn = self._output_input_fns[message.message_type]
        else:
            raise KeyError(f"Message type '{message.message_type}' not found")

        output_fn(message)
        result_str = input_fn(message)

        try:
            result = message.result_type(result_str)
            is_valid = Interface._do_tests_pass(message, result)
        except (ValueError, TypeError):
            is_valid = False

        if not is_valid:
            self.run(message.error_message)
            return self.run(message)

        if message.is_confirm:
            confirm_message = Interface._get_confirm_message(result)
            is_confirmed_str = self.run(confirm_message)
            is_confirmed = user_input.is_yes(is_confirmed_str)
            if not is_confirmed:
                return self.run(message)

        return result

    @staticmethod
    def _get_confirm_message(value):
        return Message(
            content=f"'{str(value)}', right?",
            options=['Yes', 'No'],
            message_type=Message.Type.MULTIPLE_CHOICE,
            result_type=str,
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

