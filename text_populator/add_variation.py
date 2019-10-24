import csv
from robotpt_common_utils import lists


def create_dict(
        files,
        variations_dict=None,
        code_key_in_file='Code',
        text_key_in_file='Text',
):
    files = lists.make_sure_is_iterable(files)
    for f in files:
        variations_dict = _create_dict(
                f,
                variations_dict=variations_dict,
                code_key_in_file=code_key_in_file,
                text_key_in_file=text_key_in_file,
        )

    return variations_dict


def _create_dict(
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
    variations_dict_ = _create_dict(file_)
    print(variations_dict_)
