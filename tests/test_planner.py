import unittest
from engine.planner.base_planner import BasePlanner


class TestPlanner(unittest.TestCase):

    def test_order_of_input_plan(self):
        possible_plans = ['plan1', 'plan2', 'plan3', 1, 2, 3]
        s = BasePlanner(possible_plans)
        s.new_plan(possible_plans)
        for p in possible_plans:
            self.assertEqual(
                p,
                s.pop_plan()
            )

    def test_insert_into_plan(self):
        possible_plans = ['plan1', 'plan2', 'plan3', 1, 2, 3]
        s = BasePlanner(possible_plans)
        for p in possible_plans:
            s.insert(p)
        for p in possible_plans:
            self.assertEqual(
                p,
                s.pop_plan()
            )
        s.insert(possible_plans)
        for p in possible_plans:
            self.assertEqual(
                p,
                s.pop_plan()
            )

    def test_invalid_plans(self):
        possible_plans = 'the only true plan'
        s = BasePlanner(possible_plans)
        invalid_plans = [1, 2, 3, 't', 'h', 'e', None, 'foobar', int, input]
        for p in invalid_plans:
            self.assertRaises(
                ValueError,
                s.insert,
                p
            )
            self.assertRaises(
                ValueError,
                s.new_plan,
                p
            )
