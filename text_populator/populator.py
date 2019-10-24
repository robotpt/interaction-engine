import ast
import random

from text_populator.variety_populator import VarietyPopulator
from text_populator.database_populator import DatabasePopulator


# TODO: Make a TextPopulator class and make it testdriven


def parenthetic_processor(
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


def run_populator(text):
    kwargs = ast.literal_eval(text)
    if 'var' in kwargs:
        vp = VarietyPopulator(variation_file)
        if 'index' in kwargs:
            return vp.get_replacement(
                kwargs['var'], index=kwargs['index'])
        else:
            return vp.get_replacement(kwargs['var'])
    if 'db' in kwargs:
        dp = DatabasePopulator(db)
        value = dp.get_replacement(kwargs['db'])

        if 'post-op' in kwargs:
            db_value = db.get(kwargs['db'])
            if kwargs['post-op'] == 'increment':
                db.set(kwargs['db'], db_value+1)
            elif kwargs['post-op'] == 'decrement':
                db.set(kwargs['db'], db_value-1)

        return value
    if 'rand' in kwargs:
        return random.choice(kwargs['rand'])
    else:
        return str(list(kwargs.keys())[0])


if __name__ == "__main__":

    import os
    from pickled_database import PickledDatabase

    db_file = 'test_db.pkl'
    db = PickledDatabase(db_file)
    #db.clear_database()
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
    #atexit.register(lambda: os.remove(db_file))
    atexit.register(lambda: os.remove(variation_file))

    out = parenthetic_processor(my_str.strip(), run_populator)
    print(out)
