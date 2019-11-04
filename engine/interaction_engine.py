from engine.messager.base_messenger import BaseMessenger
from engine.interfaces.interface import Interface
from engine.planner.messanger_planner import MessagerPlanner

from robotpt_common_utils import lists


class InteractionEngine:

    def __init__(self, interface, plan, messagers):

        if not issubclass(interface.__class__, Interface):
            raise TypeError

        if type(plan) is not MessagerPlanner:
            raise TypeError

        messagers = lists.make_sure_is_iterable(messagers)
        for m in messagers:
            if not issubclass(m.__class__, BaseMessenger):
                raise TypeError

        self._interface = interface
        self._plan = plan
        self._messagers = dict()
        for m in messagers:
            self._messagers[m.name] = m

    def run(self):
        while self._plan.is_active:
            messager = self._messagers[self._plan.pop_plan()]
            messager.reset()
            while messager.is_active:
                msg = messager.get_message()
                user_response = self._interface.run(msg)
                messager.transition(user_response)
