from data_structures import Message
from robotpt_common_utils import lists


class DirectedGraph:

    def __init__(self, nodes, start_node):

        self._nodes_dict = {}
        nodes = lists.make_sure_is_iterable(nodes)
        for node in nodes:
            self._add_node(node)

        if start_node not in self._start_node_name:
            raise KeyError

        self._start_node_name = start_node
        self._current_node_name = start_node

    def _add_node(self, node):

        if type(node) is not Node:
            raise TypeError

        if node.name in self._nodes_dict:
            raise KeyError("Cannot have multiple nodes with the same name")

        self._nodes_dict[node.name] = node

    def get_message(self):
        pass

    def node(self):
        return self._current_node_name

    def transition(self, user_input):
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

    def get_transition(self, user_input):
        if callable(self._transitions):
            return self._transitions(user_input)
        else:
            return self._transitions[
                self.message.options.index(user_input)
            ]

