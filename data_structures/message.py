class Message:
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
        self._options = options
        self._message_type = message_type
        self._result_type = result_type
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
            message_type='multiple choice'
        )
