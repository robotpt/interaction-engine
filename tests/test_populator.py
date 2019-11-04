import unittest
import os
from pickled_database import PickledDatabase
from interaction_engine.text_populator import TextPopulator
from interaction_engine.text_populator.database_populator import DatabasePopulator
from interaction_engine.text_populator.variety_populator import VarietyPopulator

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
foo,foo
foo,fake
foobar,foo-bar
fakebar,fake-bar
    """


class TestTextPopulator(unittest.TestCase):

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

    def test_plain_text_entry(self):
        for t in ['text', 'a', '0', 'a sentence']:
            self.assertTrue(
                self._text_populator.is_valid(t)
            )
            self.assertEqual(
                t,
                self._text_populator.run(
                    t
                )
            )

    def test_replacement_in_string(self):
        for text_to_include in ['aeunheu neuhaen ', 'abc', 'a', '']:
            text = "{'var': 'only one'}"
            self.assertTrue(
                self._text_populator.is_valid(
                    text_to_include + text + text_to_include
                )
            )
            self.assertEqual(
                text_to_include + 'just one' + text_to_include,
                self._text_populator.run(
                    text_to_include + text + text_to_include
                )
            )

            text = "{'var': 'greeting'}"
            self.assertTrue(
                self._text_populator.is_valid(
                    text_to_include + text + text_to_include
                )
            )
            self.assertTrue(
                self._text_populator.run(
                    text_to_include + text + text_to_include
                ) in [
                    text_to_include + t + text_to_include for t in [
                        'Hi', 'Hello', 'Hola'
                    ]
                ]
            )

    def test_bad_string(self):
        for text_to_include in ['aeunheu neuhaen ', 'abc', 'a', '']:
            text = "{'not a key': 'greeting'}"
            self.assertRaises(
                KeyError,
                self._text_populator.is_valid,
                text_to_include + text + text_to_include,
            )
            self.assertRaises(
                KeyError,
                self._text_populator.run,
                text_to_include + text + text_to_include
            )

            text = "{'ey: 'greeting'}"
            self.assertRaises(
                SyntaxError,
                self._text_populator.is_valid,
                text_to_include + text + text_to_include
            )
            self.assertRaises(
                SyntaxError,
                self._text_populator.run,
                text_to_include + text + text_to_include
            )

    def test_recursive_tags(self):
        test_str = (
                "{'var': 'question', 'index': " +
                "'{'db': 'question_idx', 'post-op': 'increment'}'}"
        )
        for i in range(4):
            for _ in range(10):
                self._text_populator.is_valid(test_str)
            self.assertEqual(
                i,
                self._db.get('question_idx')
            )
            self._text_populator.run(test_str)
            self.assertEqual(
                i+1,
                self._db.get('question_idx')
            )

        test_str = "{'var': '{'var': 'foo'}bar'}"
        for text_to_include in ['aeunheu neuhaen ', 'abc', 'a', '']:
            self.assertTrue(
                self._text_populator.run(
                    text_to_include + test_str + text_to_include
                ) in [
                    text_to_include + t + text_to_include for t in [
                        'foo-bar', 'fake-bar'
                    ]
                ]
            )


