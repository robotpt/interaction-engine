import unittest
import os

from text_populator.database_populator import DatabasePopulator
from pickled_database import PickledDatabase


class TestDatabasePopulator(unittest.TestCase):

    def setUp(self):
        self.file = 'test_db.pkl'
        db = PickledDatabase(self.file)
        db.create_key('key1', 1)
        db.create_key('key2', 'two')
        db.create_key('no_value_key')
        self.dp = DatabasePopulator(db)

    def tearDown(self):
        os.remove(self.file)

    def test_get_replacement(self):

        self.assertEqual(
            1,
            self.dp.get_replacement('key1')
        )
        self.assertEqual(
            'two',
            self.dp.get_replacement('key2')
        )

    def test_key_with_no_value(self):
        self.assertRaises(
            KeyError,
            self.dp.get_replacement,
            'no_value_key'
        )
        self.assertEqual(
            3,
            self.dp.get_replacement('no_value_key', default_value=3)
        )

    def test_key_that_doesnt_exist(self):
        self.assertRaises(
            KeyError,
            self.dp.get_replacement,
            'not_a_key'
        )

