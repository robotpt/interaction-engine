import time

from interaction_engine.messager.base_messenger import BaseMessenger
from interaction_engine.interfaces.interface import Interface
from interaction_engine.planner.messanger_planner import MessagerPlanner

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

        self._is_running = False

    def run(self):
        self._is_running = True
        while self._plan.is_active and self._is_running:
            self.run_next_plan()

    def run_next_plan(self):

        message_name, pre_hook, post_hook = self._plan.pop_plan(is_return_hooks=True)

        messager = self._messagers[message_name]
        messager.reset()

        pre_hook()
        while messager.is_active and self._is_running:
            msg = messager.get_message()
            user_response = self._interface.run(msg)
            try:
                messager.transition(user_response)
            except ValueError:
                self._is_running = False
        post_hook()
