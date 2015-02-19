from octobot.events import bind_event, fire_event
from octobot.plugins import Plugin

class TestingPlugin(Plugin):

    @bind_event("plugin_load")
    def plugin_load(self, *, event=None):
        yield from fire_event('command-register', command='test', description='Test function', helpmsg='Help message')

    @bind_event("command", "test")
    def testing(self, sender=None, target=None, args=None, *, event=None):
        print("got a test command!", target, sender, args)

    @bind_event("command", "echo")
    def echo(self, sender=None, target=None, args=None, *, event=None):
        if target.startswith('#'):
            t = target
        else:
            t = sender
        yield from fire_event('bot', 'privmsg', target=t, message=' '.join(args))

