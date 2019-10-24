from robotpt_common_utils import lists

import data_structures


class InteractionEngine:

    def __init__(
            self,
            planner,
            outputer
    ):
        self._planner = planner
        self._outputer = outputer

    def run(self, state):

        msg = self._get_message(state)

        # Make ability to have timeout
        return self._prompt(msg)

    def _update(self, state, msg):
        pass

    def _get_message(self, state):

        contents, options, msg_type = self._planner(state)
        generic_message = data_structures.Message(contents, options, msg_type)

        populated_message = self._populate_message(generic_message)

        return populated_message

    def _populate_message(self, msg):
        return msg

    def _prompt(self, msg):
        return self._outputer(msg)


if __name__ == '__main__':

    # build trees
    # build plan
    plans = ['hello', 'check in', 'where walk', 'bye']

    def simple_planner(state):
        return 'How are you?', ['{{really} good}', 'Okay', 'Bad'], 'multiple choice'

    def simple_input(message):
        return input(message.content)

    ie = InteractionEngine(simple_planner, simple_input)

    state_ = data_structures.state_db
    state_ = ie.run(state_)
