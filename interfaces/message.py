class Message:
    def __init__(
            self,
            content,
            options,
            type,
    ):
        self._content = content
        self._options = options
        self._type = type

    @property
    def content(self):
        return self._content

    @property
    def options(self):
        return self._options

    @property
    def type(self):
        return self._type
