from data_structures import Message
from robotpt_common_utils import lists, math_tools


class Node:

    def __init__(
            self,
            name,
            message,
            transitions,
            transition_fn=None,
    ):
        """
        :param name:
        :param message:
        :param transitions:
        :param transition_fn: A function that returns the index of a location in transitions
        """
        self._name = name

        if type(message) is not Message:
            raise TypeError("message should be an instance of the message class")
        self._message = message

        transitions = lists.make_sure_is_iterable(transitions)
        if not Node._is_transitions_valid(message, transitions, transition_fn):
            raise ValueError("Transitions should agree with message options")
        self._transitions = transitions

        if transition_fn is not None and not callable(transition_fn):
            raise ValueError('Transition function must be callable')
        self._transition_fn = transition_fn

    @property
    def name(self):
        return self._name

    @property
    def message(self):
        return self._message

    def get_transition(self, user_input):
        if len(self._transitions) is 1:
            return self._transitions[0]
        elif self._transition_fn is None:
            return self._transitions[
                self.message.options.index(user_input)
            ]
        else:
            idx = self._transition_fn(user_input)
            if not math_tools.is_int(idx):
                raise IOError("Transition function must return an index")
            return self._transitions[idx]

    @staticmethod
    def _is_transitions_valid(message, transitions, transitions_fn=None):

        is_transition_fn = transitions_fn is not None
        if is_transition_fn and not callable(transitions_fn):
            raise IOError("'transitions_fn' must be callable")

        num_transitions = len(transitions)
        num_options = len(message.options)

        if message.message_type is Message.Type.MULTIPLE_CHOICE:
            return Node._is_valid_multiple_choice(is_transition_fn, num_options, num_transitions)
        elif message.message_type is Message.Type.DIRECT_INPUT:
            return Node._is_valid_direct_entry(is_transition_fn, num_options, num_transitions)
        else:
            return NotImplementedError("Invalid message type")

    @staticmethod
    def _is_valid_direct_entry(is_transition_fn, num_options, num_transitions):
        is_one_option = num_options == 1
        if is_transition_fn:
            is_one_or_more_transitions = num_transitions >= 1
            return is_one_option and is_one_or_more_transitions
        else:
            is_one_transition = num_transitions == 1
            return is_one_option and is_one_transition

    @staticmethod
    def _is_valid_multiple_choice(is_transition_fn, num_options, num_transitions):
        if is_transition_fn:
            return False
        else:
            is_transition_for_each_option = num_options == num_transitions
            is_one_transition_for_all_options = (
                    num_transitions == 1 and num_options >= 1
            )
            return is_transition_for_each_option or is_one_transition_for_all_options
