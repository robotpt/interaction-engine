from engine.planner.base_planner import BasePlanner
from robotpt_common_utils import lists
from engine.messager.base_messenger import BaseMessenger


class MessagerPlanner(BasePlanner):

    def __init__(self, possible_plans):

        names = self._list_of_names(possible_plans)
        super().__init__(names)

    def insert(self, plan):
        names = self._list_of_names(plan)
        super().insert(names)

    def new_plan(self, plan):
        names = self._list_of_names(plan)
        super().new_plan(names)

    @staticmethod
    def _list_of_names(plans):
        plans = lists.make_sure_is_iterable(plans)
        for p in plans:
            if not issubclass(p.__class__, BaseMessenger):
                raise TypeError
        return [p.name for p in plans]
