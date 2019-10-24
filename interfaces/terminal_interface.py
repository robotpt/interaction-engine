from interfaces.interface import Interface
from data_structures import Message
from robotpt_common_utils import math_tools, lists


def print_content(message):
    if type(message) is not Message:
        raise ValueError("Must input message class")
    print("=====================")
    print(message.content)


def print_multiple_choice(message):

    print_content(message)
    _print_enumerated_list(message.options)


def _print_enumerated_list(options):
    options = lists.make_sure_is_iterable(options)
    for i in range(len(options)):
        print(f" {i}. " + options[i])


def input_multiple_choice(message):

    if type(message) is not Message:
        raise ValueError("Must input message class")

    response = None
    while response not in range(len(message.options)):
        response_str = input(">>> ")
        if math_tools.is_int(response_str):
            response = int(response_str)

    return message.options[response]


def direct_input(_):
    response = ''
    while len(response) is 0:
        response = input(">>> ")

    return response


if __name__ == '__main__':

    multiple_choice_message1 = Message(
        content='How are you?',
        options=['Good', 'Okay', 'Bad'],
        message_type='multiple choice',
    )
    multiple_choice_message2 = Message(
        content='Do you love me?',
        options='Yes!',
        message_type='multiple choice',
    )
    real_number_entry_message = Message(
        content='How old are you?',
        options='years_old',
        message_type='direct input',
        result_type=float,
        tests=[
            lambda x: x >= 0,
            lambda x: x <= 120,
        ],
        error_message='Enter a number between 0 and 120',
    )
    string_entry_message = Message(
        content="What's your name?",
        options='Okay',
        message_type='direct input',
        result_type=str,
        tests=lambda x: len(x) > 1,
        error_message='Enter something with at least two letters',
    )

    fns = [
        print_multiple_choice,
        input_multiple_choice,
        print_content,
        direct_input,
    ]
    interface = Interface(*fns)
    for msg in [
        #multiple_choice_message1,
        #multiple_choice_message2,
        real_number_entry_message,
        string_entry_message,
    ]:
        out = interface.run(msg)
        print(out)
