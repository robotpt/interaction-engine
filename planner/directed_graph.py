from data_structures import Message
from robotpt_common_utils import lists
from planner.node import Node


# TODO: check that can reach exit from all nodes, eventually


class DirectedGraph:

    def __init__(
            self,
            nodes,
            start_node,
            exit_code='exit'
    ):

        self._nodes_dict = {}
        nodes = lists.make_sure_is_iterable(nodes)
        for node in nodes:
            self._add_node(node)

        if start_node not in self._nodes_dict:
            raise KeyError

        self._start_node_name = start_node
        self._exit_code = exit_code

        self._current_node_name = None
        self._is_active = None
        self.reset()

    def reset(self):
        self._current_node_name = self._start_node_name
        self._is_active = True

    def _add_node(self, node):

        if type(node) is not Node:
            raise TypeError

        if node.name in self._nodes_dict:
            raise KeyError("Cannot have multiple nodes with the same name")

        self._nodes_dict[node.name] = node

    def get_message(self):
       return self.current_node.message

    def get_nodes(self):
        return list(self._nodes_dict)

    @property
    def current_node(self):
        return self._nodes_dict[self.current_node_name]

    @property
    def current_node_name(self):
        return self._current_node_name

    @property
    def is_active(self):
        return self._is_active

    def transition(self, user_input):
        new_node = self.current_node.get_transition(user_input)
        if new_node is self._exit_code:
            self._is_active = False
        else:
            self._current_node_name = new_node


if __name__ == '__main__':

    from interfaces.terminal_interface import TerminalInterface

    multiple_choice_message1 = Message(
        content='How are you?',
        options=['Good', 'Okay', 'Bad'],
        message_type='multiple choice',
    )
    multiple_choice_message2 = Message(
        content='Do you love me?',
        options='Yes!',
        message_type='multiple choice',
    )
    real_number_entry_message = Message(
        content='How old are you?',
        options='years_old',
        message_type='direct input',
        result_type=float,
        tests=[
            lambda x: x >= 0,
            lambda x: x <= 120,
        ],
        error_message='Enter a number between 0 and 120',
    )
    string_entry_message = Message(
        content="What's your name?",
        options='Okay',
        message_type='direct input',
        result_type=str,
        tests=lambda x: len(x) > 1,
        error_message='Enter something with at least two letters',
    )

    node1 = Node(
        name='node1',
        message=multiple_choice_message1,
        transitions=['node2', 'node2', 'node3'],
    )
    node2 = Node(
        name='node2',
        message=multiple_choice_message2,
        transitions='node3'
    )
    node3 = Node(
        name='node3',
        message=string_entry_message,
        transitions='exit'
    )

    nodes = [node1, node2, node3]
    directed_graph = DirectedGraph(
        nodes=nodes,
        start_node='node1'
    )
    interface = TerminalInterface()
    while directed_graph.is_active:
        msg = directed_graph.get_message()
        user_response = interface.run(msg)
        directed_graph.transition(user_response)


