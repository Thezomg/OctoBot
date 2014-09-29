from octobot.events import bind_event, fire_event
from octobot.plugins import Plugin

class CommandPlugin(Plugin):

    def __init__(self):
        self.__commands = {}

    @bind_event("privmsg")
    def on_message(self, sender=None, target=None, message=None, *, event=None):
        print("command plugin")
        if message.startswith(','):
            command, *args = message[1:].split(' ')
            fire_event('command', command, sender=sender, target=target, args=args)

    @bind_event("command", "help")
    def on_cmd_help(self, sender=None, target=None, args=None, *, event=None):
        if len(args) > 0:
            if args[0].lower() in self.__commands:
                c = self.__commands[args[0].lower()]
                print("{}: {}, {}".format(args[0].lower(), *c[0]))
            else:
                print("Help not provided for that command")
        pass # handle help message

    @bind_event("command-register")
    def on_command_register(self, command, description, helpmsg, *, event=None):
        self.__commands[command.lower()] = (description, helpmsg,)
        pass