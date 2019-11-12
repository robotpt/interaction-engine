import csv
import random

from robotpt_common_utils import lists, math_tools, strings
from interaction_engine.text_populator.base_populator import BasePopulator


class VarietyPopulator(BasePopulator):

    class Tags:
        MAIN = 'var'
        INDEX = 'index'
        IS_WRAP_INDEX = 'is_wrap_index'

    def __init__(
            self,
            files,
            code_key_in_file='Code',
            text_key_in_file='Text',
            wild_card_symbol='*',
    ):
        super().__init__(
            main_tags=self.Tags.MAIN,
            option_tags=[
                self.Tags.INDEX,
                self.Tags.IS_WRAP_INDEX
            ]
        )

        self._variations = VarietyPopulator._create_dict(
            files,
            code_key_in_file=code_key_in_file,
            text_key_in_file=text_key_in_file,
        )
        self._wild_card_symbol = wild_card_symbol

    def get_replacement(
            self,
            key,
            index=None,
            is_wrap_index=True
    ):
        choices = self.values(key)
        if index is None:
            return random.choice(choices)
        else:
            if not is_wrap_index and index > self.get_num_variations(key):
                raise IndexError
            if math_tools.is_int(index):
                index = int(index)
            else:
                raise ValueError("Index must be an int")
            i = index % self.get_num_variations(key)
            return choices[i]

    def get_num_variations(self, key):
        return len(self.values(key))

    def __contains__(self, key):
        return key in self._variations

    @property
    def keys(self):
        return list(self._variations.keys())

    def values(self, key):
        active_keys = strings.wildcard_search_in_list(key, self.keys)
        values = []
        for active_key in active_keys:
            values += self._variations[active_key]
        return values

    @staticmethod
    def _create_dict(
            files,
            variations_dict=None,
            code_key_in_file='Code',
            text_key_in_file='Text',
    ):
        files = lists.make_sure_is_iterable(files)
        for f in files:
            variations_dict = VarietyPopulator._create_dict_from_one_file(
                    f,
                    variations_dict=variations_dict,
                    code_key_in_file=code_key_in_file,
                    text_key_in_file=text_key_in_file,
            )

        return variations_dict

    @staticmethod
    def _create_dict_from_one_file(
            file,
            variations_dict=None,
            code_key_in_file='Code',
            text_key_in_file='Text',
    ):

        if variations_dict is None:
            variations_dict = dict()

        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:

                code = row[code_key_in_file]
                text = row[text_key_in_file]
                if code in variations_dict:
                    if text in variations_dict[code]:
                        raise ValueError(f"Duplicate entry '{code}': '{text}'")
                    variations_dict[code].append(text)
                else:
                    variations_dict[code] = [text]

        return variations_dict


if __name__ == '__main__':

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

    import os
    import atexit

    # atexit.register(lambda: os.remove(db_file))
    atexit.register(lambda: os.remove(variation_file))

    variety_populator = VarietyPopulator(variation_file)
    variations_dict_ = VarietyPopulator._create_dict(variation_file)
    print(variations_dict_)
