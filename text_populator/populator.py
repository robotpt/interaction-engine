import ast
import random

from text_populator.variety_populator import VarietyPopulator
from text_populator.database_populator import DatabasePopulator


# TODO: Move kwargs handling inside of each populator class
# TODO: Allow populator to have n args put in that are each checked for keywords
# TODO: Test TextPopulator


class TextPopulator:

    def __init__(
            self,
            variety_populator,
            database_populator,
    ):
        self._variety_populator = variety_populator
        self._database_populator = database_populator

    def run(self, text):
        return TextPopulator._parenthetic_processor(
            text,
            self._handle_string_input,
            open_symbol='{',
            closed_symbol='}',
        )

    def _handle_string_input(self, text):
        kwargs = ast.literal_eval(text)

        if 'var' in kwargs:

            handle = kwargs['var']

            if 'index' in kwargs:
                return self._variety_populator.get_replacement(
                    handle, index=kwargs['index'])
            else:
                return self._variety_populator.get_replacement(handle)

        elif 'db' in kwargs:

            key = kwargs['db']

            if 'post-op' in kwargs:
                fn = kwargs['post-op']
                value = self._database_populator.get_replacement(key, modify_before_resaving_fn=fn)
            else:
                value = self._database_populator.get_replacement(key)

            return value

        elif 'rand' in kwargs:
            return random.choice(kwargs['rand'])
        else:
            return "<< not expanded" + str(list(kwargs.keys())[0]) + ">>"

    @staticmethod
    def _parenthetic_processor(
            text,
            fn,
            open_symbol='{',
            closed_symbol='}',
    ):
        open_parenthesis_stack = []

        itr = 0
        while itr < len(text):

            if text[itr:itr+len(open_symbol)] == open_symbol:
                open_parenthesis_stack.append(itr)

            elif text[itr:itr+len(closed_symbol)] == closed_symbol:
                if len(open_parenthesis_stack) == 0:
                    raise ValueError("Not all closing symbols matched")

                start_idx = open_parenthesis_stack.pop()
                end_idx = itr+1
                segment = text[start_idx:end_idx]
                replacement = fn(segment)

                text = "".join((
                    text[:start_idx],
                    replacement,
                    text[end_idx:]
                ))
                itr = start_idx

            itr += 1
        if len(open_parenthesis_stack) == 0:
            return text
        else:
            raise ValueError("Not all open symbols matched")


if __name__ == "__main__":

    import os
    from pickled_database import PickledDatabase

    db_file = 'test_db.pkl'
    db = PickledDatabase(db_file)
    db.create_key_if_not_exists('key1', 1)
    db.create_key_if_not_exists('key2', 'two')
    db.create_key_if_not_exists('no_value_key')
    db.create_key_if_not_exists('user_name', 'Audrow')
    db.create_key_if_not_exists('question_idx', 1)

    my_str = """
{'var': 'greeting'}, {'db': 'user_name'}. 
{'rand': ["What's up", 'How are you', "How's it going"]}?
{'var': 'question', 'index': '{'db': 'question_idx', 'post-op': 'increment'}'}
{'var': '{'var': 'foo'}bar'}
    """

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
    for _ in range(4):
        out = text_populator.run(my_str)
        print(out)
