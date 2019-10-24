from data_structures import Message
from robotpt_common_utils import lists


class DirectedGraph:

    def __init__(self):
        pass


class Node:

    def __init__(
            self,
            name,
            message,
            transitions,
    ):
        self._name = name

        if type(message) is not Message:
            raise TypeError("message should be an instance of the message class")
        self._message = message

        if not callable(transitions):
            transitions = lists.make_sure_is_iterable(transitions)
            if len(transitions) is 1:
                transitions = transitions*len(message.options)
            if len(transitions) is not len(message.options):
                raise IOError("Transitions should agree with message options")
        self._transitions = transitions

    @property
    def name(self):
        return self._name

    @property
    def message(self):
        return self._message

    def get_transition(self, input):
        if callable(self._transitions):
            return self._transitions(input)
        else:
            return self._transitions[
                self.message.options.index(input)
            ]

