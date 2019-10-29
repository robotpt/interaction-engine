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

    multiple_choice_message1 = Message(
        content='How are you?',
        options=['Good', 'Okay', 'Bad'],
        message_type='multiple choice',
    )
    multiple_choice_message2 = Message(
        content='Do you love me?',
        options='Yes!',
        message_type='multiple choice',
        is_confirm=True,
    )
    real_number_entry_message = Message(
        content='How old are you?',
        options='years_old',
        message_type='direct input',
        result_type=float,
        result_db_key='user_age',
        tests=[
            lambda x: x >= 0,
            lambda x: x <= 200,
        ],
        error_message='Enter a number between 0 and 200',
    )
    string_entry_message = Message(
        content="What's your name?",
        options='Okay',
        message_type='direct input',
        result_db_key='user_name',
        result_type=str,
        tests=lambda x: len(x) > 1,
        error_message='Enter something with at least two letters',
        is_confirm=True,
    )

    ask_name = Node(
        name='ask name',
        message=string_entry_message,
        transitions='ask age'
    )
    ask_age = Node(
        name='ask age',
        message=real_number_entry_message,
        transitions='how are they'
    )
    how_are_they = Node(
        name='how are they',
        message=multiple_choice_message1,
        transitions=['do love me', 'exit', 'exit'],
    )
    do_love_me = Node(
        name='do love me',
        message=multiple_choice_message2,
        transitions='exit'
    )

    nodes = [ask_age, ask_name, how_are_they, do_love_me]
    directed_graph = DirectedGraph(
        nodes=nodes,
        start_node='ask name'
    )

    from interfaces.terminal_interface import TerminalInterface
    from pickled_database import PickledDatabase

    import os
    import atexit

    atexit.register(lambda: os.remove(db_file))

    db_file = "memory.pkl"
    db = PickledDatabase(db_file)

    interface = TerminalInterface(pickled_database=db)
    while directed_graph.is_active:
        msg = directed_graph.get_message()
        user_response = interface.run(msg)
        directed_graph.transition(user_response)

    print("=========================")
    print("Currently in the database")
    print(db)

