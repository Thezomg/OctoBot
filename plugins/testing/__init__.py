from octobot.events import bind_event, fire_event
from octobot.plugins import Plugin

class TestingPlugin(Plugin):
    @bind_event("command", "test")
    def testing(self, sender=None, target=None, args=None, *, event=None):
        print("got a test command!", target, sender, args)
