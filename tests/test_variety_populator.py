import unittest
import os

from interaction_engine.text_populator.variety_populator import VarietyPopulator

file1_path = 'file1.csv'
file1_contents = """
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

file2_path = 'file2.csv'
file2_contents = """
Code,Text
greeting,Bonjour
greeting,Hei
new,bar
"""

duplicate_entry_path = 'duplicate_entry.csv'
duplicate_entry_contents = """
Code,Text
foo,foo
foo,foo
"""

files = (
    (file1_path, file1_contents),
    (file2_path, file2_contents),
    (duplicate_entry_path, duplicate_entry_contents),
)


def write_file(path, contents):
    with open(path, 'w', newline='') as csvfile:
        csvfile.write(contents.strip())


def delete_file(path):
    os.remove(path)


class TestVarietyPopulator(unittest.TestCase):

    def setUp(self):
        for path, contents in files:
            write_file(path, contents)

    def tearDown(self):
        for path, _ in files:
            delete_file(path)

    def test_get_replacement(self):
        vp = VarietyPopulator(file1_path)
        num_entries = vp.get_num_variations('greeting')
        self.assertEqual(
            3,
            num_entries
        )
        entries = []
        for i in range(num_entries):
            entries.append(vp.get_replacement(
                'greeting',
                index=i,
            ))

        for _ in range(100):
            self.assertTrue(
                vp.get_replacement('greeting') in entries
            )

    def test_wrap_index_error(self):

        vp = VarietyPopulator(file1_path)
        num_entries = vp.get_num_variations('greeting')
        entries = []
        for i in range(num_entries):
            entries.append(vp.get_replacement(
                'greeting',
                index=i,
            ))

        for i in range(100):
            self.assertEqual(
                entries[i % num_entries],
                vp.get_replacement(
                    'greeting',
                    index=i,
                    is_wrap_index=True,
                )
            )

        for i in range(num_entries + 1, 100):
            self.assertRaises(
                IndexError,
                vp.get_replacement,
                'greeting',
                index=i,
                is_wrap_index=False,
            )

    def test_create_dict_from_file(self):
        variation_dict = VarietyPopulator._create_dict(file1_path)

        self.assertTrue('Code' not in variation_dict)
        self.assertTrue('Text' not in variation_dict)
        for k in ['greeting', 'question', 'foo', 'foobar', 'fakebar']:
            self.assertTrue(k in variation_dict)
        self.assertEqual(
            3,
            len(variation_dict['greeting'])
        )
        self.assertEqual(
            4,
            len(variation_dict['question'])
        )
        self.assertEqual(
            'fake-bar',
            variation_dict['fakebar'][0]
        )

    def test_create_dict_from_multiple_files(self):

        variation_dict1 = VarietyPopulator._create_dict([file1_path, file2_path])

        variation_dict2 = VarietyPopulator._create_dict(file1_path)
        variation_dict2 = VarietyPopulator._create_dict(file2_path, variation_dict2)

        variation_dict3 = VarietyPopulator._create_dict(file2_path)
        variation_dict3 = VarietyPopulator._create_dict(file1_path, variation_dict3)

        for vd in [variation_dict1, variation_dict2, variation_dict3]:

            for k in ['greeting', 'question', 'foo', 'foobar', 'fakebar', 'new']:
                self.assertTrue(k in vd)
            self.assertEqual(
                5,
                len(vd['greeting'])
            )

    def test_duplicate_items(self):
        self.assertRaises(
            ValueError,
            VarietyPopulator._create_dict,
            duplicate_entry_path
        )
