import asyncio

from octoirc import IRCProtocol
from .events import EventManager, fire_event, bind_event
from .plugins import PluginManager
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('octobot')

class Bot(IRCProtocol):

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.plugin_manager = PluginManager(['plugins'])
        self.plugin_manager.find_plugins()
        self.event_manager_thread = asyncio.async(EventManager.handleEvents())
        asyncio.async(fire_event("plugin_load"))
        EventManager.register_class(self)

    def connected(self):
        self.nick('Testing')
        self.user('Testing', 'Testing')

    def _handle_rpl_welcome(self, prefix, args):
        self.join("#test")

    @bind_event('bot', 'privmsg')
    def send_privmsg(self, target=None, message=None, *, event=None):
        self.message(target, message)

    @asyncio.coroutine
    def on_message(self, sender, target, message):
        yield from fire_event("privmsg", sender=sender, target=target, message=message)

    @classmethod
    def new(cls, loop, host, port):
        asyncio.async(loop.create_connection(Bot, host, port))
