from robotpt_common_utils import lists
from engine.messager.node import Node
from engine.messager.base_messenger import BaseMessenger


# TODO: check that can reach exit from all nodes, eventually


class DirectedGraph(BaseMessenger):

    def __init__(
            self,
            name,
            nodes,
            start_node,
            exit_code='exit'
    ):

        super().__init__(name)
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
        return self._nodes_dict[self.current_node].message

    def get_nodes(self):
        return list(self._nodes_dict)

    @property
    def current_node(self):
        if self._is_active:
            return self._current_node_name
        else:
            return None

    @property
    def is_active(self):
        return self._is_active

    def transition(self, user_input):
        if not self.is_active:
            raise RuntimeError("Currently inactive")
        new_node = self._nodes_dict[self.current_node].get_transition(user_input)
        if new_node is self._exit_code:
            self._is_active = False
        else:
            self._current_node_name = new_node


if __name__ == '__main__':

    import os
    from pickled_database import PickledDatabase
    from engine.text_populator import TextPopulator
    from engine.text_populator import DatabasePopulator
    from engine.text_populator.variety_populator import VarietyPopulator

    db_file = 'test_db.pkl'
    db = PickledDatabase(db_file)
    db.create_key_if_not_exists('key1', 1)
    db.create_key_if_not_exists('key2', 'two')
    db.create_key_if_not_exists('no_value_key')
    db.create_key_if_not_exists('user_name', 'Audrow')
    db.create_key_if_not_exists('question_idx', 1)

    variation_file = 'variation.csv'
    variation_file_contents = """
Code,Text
greeting,Hi
greeting,Hello
greeting,Hola
question,Do you like green?
question,Do you like dogs?
question,Do you like apples?
question,Do you like me?
foo,foo
foo,fake
foobar,foo-bar
fakebar,fake-bar
        """

    with open(variation_file, 'w', newline='') as csvfile:
        csvfile.write(variation_file_contents.strip())

    import atexit
    atexit.register(lambda: os.remove(db_file))
    atexit.register(lambda: os.remove(variation_file))

    variety_populator_ = VarietyPopulator(variation_file)
    database_populator_ = DatabasePopulator(db_file)
    text_populator = TextPopulator(variety_populator_, database_populator_)

    ask_name = Node(
        name='ask name',
        content="What's your name?",
        options='Okay',
        message_type='direct input',
        result_db_key='user_name',
        result_type=str,
        tests=lambda x: len(x) > 1,
        error_message='Enter something with at least two letters',
        is_confirm=True,
        text_populator=text_populator,
        transitions='ask age'
    )
    ask_age = Node(
        name='ask age',
        content="Alright, {'db': 'user_name'}, how old are you?",
        options='years_old',
        message_type='direct input',
        result_type=float,
        result_db_key='user_age',
        tests=[
            lambda x: x >= 0,
            lambda x: x <= 200,
        ],
        error_message='Enter a number between 0 and 200',
        text_populator=text_populator,
        transitions='how are they'
    )
    how_are_they = Node(
        name='how are they',
        content='How are you?',
        options=['Good', 'Okay', 'Bad'],
        message_type='multiple choice',
        text_populator=text_populator,
        transitions=['psych question', 'psych question', 'exit'],
    )
    do_love_me = Node(
        name='psych question',
        content="{'var': 'question', 'index': '{'db': 'question_idx', 'post-op': 'increment'}'}",
        options="Yes!",
        message_type='multiple choice',
        text_populator=text_populator,
        transitions='exit',
    )

    nodes_ = [ask_age, ask_name, how_are_they, do_love_me]
    directed_graph = DirectedGraph(
        name='graph1',
        nodes=nodes_,
        start_node='ask name'
    )

    from engine.interfaces.terminal_interface import TerminalInterface
    from pickled_database import PickledDatabase

    interface = TerminalInterface(pickled_database=db)
    while directed_graph.is_active:
        msg = directed_graph.get_message()
        user_response = interface.run(msg)
        directed_graph.transition(user_response)

    print("=========================")
    print("Currently in the database")
    print(db)
