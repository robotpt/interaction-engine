import unittest
from planner.directed_graph import DirectedGraph, Node
from data_structures import Message


class TestDirectedGraph(unittest.TestCase):

    pass


class TestNode(unittest.TestCase):

    def test_multiple_choice_transition(self):
        options = ['Good', 'Okay', 'Bad']
        transitions = ['great', 'good', 'too bad']
        n = Node(
            name='name',
            message=Message(
                content='How are you?',
                options=options,
                message_type='multiple choice'
            ),
            transitions=transitions
        )
        self.assertEqual(
            len(transitions),
            len(options)
        )
        for i in range(len(options)):
            self.assertEqual(
                transitions[i],
                n.get_transition(options[i])

            )

    def test_single_choice_transitions(self):
        options = ['Good', 'Okay', 'Bad']
        transition = 'oh'
        n = Node(
            name='name',
            message=Message(
                content='How are you?',
                options=options,
                message_type='multiple choice'
            ),
            transitions=transition
        )
        for i in range(len(options)):
            self.assertEqual(
                transition,
                n.get_transition(options[i])
            )

    def test_fn_transition(self):

        def transition_fn(input):
            if input < 0:
                return 'negative'
            if input == 0:
                return 'zero'
            if input > 0:
                return 'positive'

        options = ['Good', 'Okay', 'Bad']
        n = Node(
            name='name',
            message=Message(
                content='How are you?',
                options=options,
                message_type='multiple choice'
            ),
            transitions=transition_fn
        )
        for i in range(-10, 0):
            self.assertEqual(
                'negative',
                n.get_transition(i)
            )
        self.assertEqual(
            'zero',
            n.get_transition(0)
        )
        for i in range(1, 11):
            self.assertEqual(
                'positive',
                n.get_transition(i)
            )

