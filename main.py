import asyncio

from octobot import Bot
from octobot.plugins import PluginManager

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    bot = Bot.new(loop, 'localhost', 6667)
    loop.run_forever()
    #plugin_manager = PluginManager(['plugins'])
    #plugin_manager.find_plugins()
