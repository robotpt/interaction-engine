import csv
import random

from robotpt_common_utils import lists


class VarietyPopulator:

    def __init__(
            self,
            files,
            code_key_in_file='Code',
            text_key_in_file='Text',
    ):
        self._variations = VarietyPopulator._create_dict(
            files,
            code_key_in_file=code_key_in_file,
            text_key_in_file=text_key_in_file,
        )

    def get_replacement(self, key, index=None, is_wrap_index=True):
        if index is None:
            return random.choice(self._variations[key])
        else:
            if not is_wrap_index and index > self.get_num_variations(key):
                raise IndexError
            i = index % self.get_num_variations(key)
            return self._variations[key][i]

    def get_num_variations(self, key):
        return len(self._variations[key])

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
                        raise ValueError("Duplicate entry")
                    variations_dict[code].append(text)
                else:
                    variations_dict[code] = [text]

        return variations_dict


if __name__ == '__main__':

    file_ = '../variation.csv'
    variations_dict_ = VarietyPopulator._create_dict(file_)
    print(variations_dict_)
