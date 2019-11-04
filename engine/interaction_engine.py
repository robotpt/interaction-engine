from messager.base_messenger import BaseMessenger
from interfaces.interface import Interface
from engine.messanger_planner import MessagerPlanner

from robotpt_common_utils import lists


class InteractionEngine:

    def __init__(self, interface, plan, messagers):

        if not issubclass(interface.__class__, Interface):
            raise TypeError

        if type(plan) is not MessagerPlanner:
            raise TypeError

        messagers = lists.make_sure_is_iterable(messagers)
        for m in messagers:
            if not issubclass(m.__class__, BaseMessenger):
                raise TypeError

        self._interface = interface
        self._plan = plan
        self._messagers = dict()
        for m in messagers:
            self._messagers[m.name] = m

    def run(self):
        while self._plan.is_active:
            messager = self._messagers[self._plan.pop_plan()]
            messager.reset()
            while messager.is_active:
                msg = messager.get_message()
                user_response = self._interface.run(msg)
                messager.transition(user_response)


if __name__ == '__main__':

    import os

    from pickled_database import PickledDatabase
    from data_structures import Message

    from interfaces.terminal_interface import TerminalInterface
    from messager.node import Node
    from messager.directed_graph import DirectedGraph
    from text_populator import TextPopulator
    from text_populator.database_populator import DatabasePopulator
    from text_populator.variety_populator import VarietyPopulator

    import atexit

    db_file = 'test_db.pkl'
    db = PickledDatabase(db_file)
    db.create_key_if_not_exists('user_name')
    db.create_key_if_not_exists('question_idx', 0)
    db.create_key_if_not_exists('answers')

    variation_file = 'variation.csv'
    variation_file_contents = """
Code,Text
greeting,Hi
greeting,Hello
greeting,Hola
question,I am the life of the party
question,I am always prepared
question,I get stressed out easily
question,I have a rich vocabulary
foo,foo
foo,fake
foobar,foo-bar
fakebar,fake-bar
"""

    with open(variation_file, 'w', newline='') as csvfile:
        csvfile.write(variation_file_contents.strip())

    atexit.register(lambda: os.remove(db_file))
    atexit.register(lambda: os.remove(variation_file))

    variety_populator_ = VarietyPopulator(variation_file)
    database_populator_ = DatabasePopulator(db_file)
    text_populator = TextPopulator(variety_populator_, database_populator_)

    greeting = DirectedGraph(
        name='greeting',
        nodes=[
            Node(
                name='greeting',
                content="{'var': 'greeting'}",
                options="{'var': 'greeting'}",
                message_type=Message.Type.MULTIPLE_CHOICE,
                result_type=str,
                text_populator=text_populator,
                transitions='exit'
            ),
        ],
        start_node='greeting'
    )
    basic_questions = DirectedGraph(
        name='intro',
        nodes=[
            Node(
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
            ),
            Node(
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
            ),
            Node(
                name='how are they',
                content='How are you?',
                options=['Good', 'Okay', 'Bad'],
                message_type='multiple choice',
                text_populator=text_populator,
                transitions=['exit'],
            ),
        ],
        start_node='ask name'
    )
    psych_question = DirectedGraph(
        name='questions',
        nodes=[
            Node(
                name='psych question',
                content=(
                        "How do you feel about the following statement? " +
                        "'{'var': 'question', 'index': " +
                        "'{'db': 'question_idx', 'post-op': 'increment'}'}'"
                ),
                options=[
                    'Strongly agree',
                    'Agree',
                    'Neutral',
                    'disagree',
                    'Strongly disagree',
                ],
                message_type='multiple choice',
                result_db_key='answers',
                is_append_result=True,
                text_populator=text_populator,
                transitions='exit',
            ),
        ],
        start_node='psych question'
    )
    closing = DirectedGraph(
        name='closing',
        nodes=[
            Node(
                name='closing',
                content="Bye",
                options=['Bye', 'See ya!'],
                message_type=Message.Type.MULTIPLE_CHOICE,
                result_type=str,
                text_populator=text_populator,
                transitions='exit'
            ),
        ],
        start_node='closing'
    )

    graphs_ = [greeting, basic_questions, psych_question, closing]

    plan_ = MessagerPlanner(graphs_)
    plan_.insert(greeting)
    plan_.insert(basic_questions)
    for _ in range(3):
        plan_.insert(psych_question)
    plan_.insert(closing)

    interface_ = TerminalInterface(pickled_database=db)

    engine = InteractionEngine(interface_, plan_, graphs_)
    engine.run()

