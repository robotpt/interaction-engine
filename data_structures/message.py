from robotpt_common_utils import lists


class Message:

    class Type:
        MULTIPLE_CHOICE = "multiple choice"
        DIRECT_INPUT = "direct input"

    def __init__(
            self,
            content,
            options,
            message_type,
            result_type=str,
            tests=None,
            error_message="Please enter a valid input",
            error_options=('Okay', 'Oops'),
    ):
        self._content = content

        options = lists.make_sure_is_iterable(options)
        self._options = options

        self._message_type = message_type
        self._result_type = result_type

        if tests is not None:
            tests = lists.make_sure_is_iterable(tests)
        self._tests = tests
        self._error_message = error_message
        self._error_options = error_options

    @property
    def content(self):
        return self._content

    @property
    def options(self):
        return self._options

    @property
    def message_type(self):
        return self._message_type

    @property
    def result_type(self):
        return self._result_type

    @property
    def tests(self):
        return self._tests

    @property
    def error_message(self):
        return Message(
            content=self._error_message,
            options=self._error_options,
            message_type=Message.Type.MULTIPLE_CHOICE
        )

