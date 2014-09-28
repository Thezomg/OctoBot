import asyncio

from irc import IRCProtocol
from irc.events import EventManager
from irc.plugins import PluginManager
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('octobot')

class Bot(IRCProtocol):

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.plugin_manager = PluginManager(['plugins'])
        self.plugin_manager.load_plugins()
        self.event_manager_thread = asyncio.async(EventManager.handleEvents())

    def connected(self):
        self.nick('Testing')
        self.user('Testing', 'Testing')

    def _handle_rpl_welcome(self, prefix, args):
        self.join("#test")

    def on_message(self, sender, target, message):
        if target.startswith('#'):
            self.message(target, message[::-1])
        else:
            if message.startswith('join'):
                self.join(message.split(' ')[1])
                self.message(sender[0], 'Joining...')
            self.message(sender[0], message[::-1])

    @classmethod
    def new(cls, loop):
        asyncio.async(loop.create_connection(Bot, 'localhost', 6667))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    bot = Bot.new(loop)
    loop.run_forever()
