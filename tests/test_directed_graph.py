import unittest
from messager.directed_graph import DirectedGraph, Node
from data_structures import Message

content = 'Question'
options = ['left', 'right']


message = Message(
    content=content,
    options=options,
    message_type=Message.Type.MULTIPLE_CHOICE,
)


def left_option():
    return options[0]


def right_option():
    return options[1]


node1 = Node(
    name='node1',
    message=message,
    transitions=['node2', 'node1']
)
node2 = Node(
    name='node2',
    message=message,
    transitions=['node1', 'node3']
)
node3 = Node(
    name='node3',
    message=message,
    transitions=['exit', 'exit']
)


class TestDirectedGraph(unittest.TestCase):

    def test_step_through_nodes(self) -> None:
        nodes_ = [node1, node2, node3]
        directed_graph = DirectedGraph(
            name='graph1',
            nodes=nodes_,
            start_node='node1'
        )

        for _ in range(10):
            self.assertEqual(
                message,
                directed_graph.get_message()
            )

            for _ in range(10):
                self.assertTrue(directed_graph.is_active)
                directed_graph.transition(right_option())
                self.assertEqual(
                    node1.name,
                    directed_graph.current_node,
                )

            self.assertTrue(directed_graph.is_active)
            directed_graph.transition(left_option())

            for _ in range(10):
                directed_graph.transition(left_option())
                directed_graph.transition(left_option())
                self.assertEqual(
                    node2.name,
                    directed_graph.current_node,
                )
                self.assertTrue(directed_graph.is_active)

            directed_graph.transition(right_option())
            self.assertTrue(directed_graph.is_active)
            directed_graph.transition(left_option())
            self.assertFalse(directed_graph.is_active)

            for _ in range(10):
                self.assertRaises(
                    RuntimeError,
                    directed_graph.transition,
                    left_option()
                )
                self.assertIsNone(
                    directed_graph.current_node
                )

            directed_graph.reset()
