from data_structures import Message
from text_populator.populator import TextPopulator
from planner.directed_graph import Node

from robotpt_common_utils import lists


# TODO: Test


def is_valid_node(text_populator, node):

    if type(text_populator) is not TextPopulator:
        raise TypeError

    if type(node) is not Node:
        raise TypeError

    return _is_valid_message(node.message)


def _is_valid_message(text_populator, message):

    if type(text_populator) is not TextPopulator:
        raise TypeError

    if type(message) is not Message:
        raise TypeError

    options = lists.make_sure_is_iterable(message.options)
    for text in [message.content] + options:
        if not text_populator.test(text):
            return False

    return True
