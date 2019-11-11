import unittest
import os
import random

from interaction_engine.messager import Message
from interaction_engine.text_populator import TextPopulator, VarietyPopulator, DatabasePopulator
from pickled_database import PickledDatabase

db_file = 'test_db.pkl'

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
only one,just one
replace1,{'var': 'replace2'}
replace2,{'var': 'replace3'}
replace3,Works!
foo,foo
foo,fake
foobar,foo-bar
fakebar,fake-bar
"""

class TestMessage(unittest.TestCase):

    def setUp(self) -> None:

        db = PickledDatabase(db_file)
        db.create_key_if_not_exists('user_name')
        db.create_key_if_not_exists('question_idx', 0)
        db.create_key_if_not_exists('answers')

        with open(variation_file, 'w', newline='') as csvfile:
            csvfile.write(variation_file_contents.strip())

        variety_populator_ = VarietyPopulator(variation_file)
        database_populator_ = DatabasePopulator(db_file)
        self._text_populator = TextPopulator(variety_populator_, database_populator_)
        self._db = db

    def tearDown(self) -> None:

        os.remove(db_file)
        os.remove(variation_file)

    def test_string_markup(self):
        greetings = ['Hi', 'Hello', 'Hola', "{'var': 'greeting'}"]
        message = Message(
            content='{greeting}',
            options=greetings,
            message_type=Message.Type.MULTIPLE_CHOICE,
            text_populator=self._text_populator
        )
        for _ in range(10):
            self.assertTrue(message.content in greetings)
            for o in message.options:
                self.assertTrue(o in greetings)

    def test_function_markup(self):
        greetings_fn_return = ['Foo']
        message = Message(
            content=lambda: random.choice(greetings_fn_return),
            options=lambda: greetings_fn_return,
            message_type=Message.Type.MULTIPLE_CHOICE,
            text_populator=self._text_populator
        )
        greetings_fn_return = ['Hi', 'Hello', 'Hola', "{'var': 'greeting'}"]

        true_greetings = ['Hi', 'Hello', 'Hola']
        for _ in range(1):
            content = message.content
            self.assertTrue(content in true_greetings)
            options = message.options
            for o in options:
                self.assertTrue(o in true_greetings)

