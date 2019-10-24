import ast

from text_populator.variety_populator import VarietyPopulator
from text_populator.database_populator import DatabasePopulator


my_str = """
{'var': 'greeting'}, {'db': 'user_name'}. 
{'rand': ["What's up", 'How are you', "How's it going"]}?
{'var': 'question', 'index': '{'db': 'question_idx'}'}
{'var': '{'var': 'foo'}bar'}
"""


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


def turn_to_dictionary_and_print_first_key(text):
    kwargs = ast.literal_eval(text)
    if 'var' in kwargs:
        vp = VarietyPopulator('../variation.csv')
        """
        if 'index' in kwargs:
            return vp.get_replacement(kwargs['var'], index=kwargs['index'])
        else:
            return vp.get_replacement(kwargs['var'])
        """
        return vp.get_replacement(kwargs['var'])
    if 'db' in kwargs:
        dp = DatabasePopulator(db)
        return dp.get_replacement(kwargs['db'])
    else:
        return str(list(kwargs.keys())[0])


if __name__ == "__main__":

    import os
    from pickled_database import PickledDatabase

    db_file = 'test_db.pkl'
    db = PickledDatabase(db_file)
    db.create_key('key1', 1)
    db.create_key('key2', 'two')
    db.create_key('no_value_key')
    db.create_key('user_name', 'Audrow')
    db.create_key('question_idx', 1)

    expr = my_str
    out = parenthetic_processor(expr, turn_to_dictionary_and_print_first_key)
    print(out)

    os.remove(db_file)
