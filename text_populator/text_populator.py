import ast

my_str = """
{'var': 'greeting'}, {'db': 'user_name'}. 
{'rand': ["What's up", 'How are you', "How's it going"]}?
{'var': 'question', 'ordered': True}
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
    return str(list(kwargs.keys())[0])


if __name__ == "__main__":

    expr = my_str
    out = parenthetic_processor(expr, turn_to_dictionary_and_print_first_key)
    print(out)
