from robotpt_common_utils import lists


class BasePlanner:

    def __init__(self, possible_plans):
        possible_plans = lists.make_sure_is_iterable(possible_plans)
        self._possible_items = possible_plans.copy()

        self._plan = []

    def insert(self, plan):
        plan = lists.make_sure_is_iterable(plan)
        if not self._is_valid_plan(plan):
            raise ValueError("Invalid plan")
        self._plan += plan

    def new_plan(self, plan):
        plan = lists.make_sure_is_iterable(plan)
        if not self._is_valid_plan(plan):
            raise ValueError("Invalid plan")
        self._plan = [] + plan

    def _is_valid_plan(self, plan):
        plan = lists.make_sure_is_iterable(plan)
        for p in plan:
            if p not in self._possible_items:
                return False
        return True

    @property
    def plan(self):
        return self._plan

    def pop_plan(self):
        return self._plan.pop(0)

    @property
    def is_active(self):
        return len(self._plan) > 0

    def __eq__(self, other):
        if not issubclass(other.__class__, BasePlanner):
            raise ValueError
        if len(self.plan) != len(other.plan):
            return False
        for i in range(len(self.plan)):
            if self.plan[i] != other.plan[i]:
                return False
        return True



