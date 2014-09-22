import asyncio

from irc import IRCProtocol

class Bot(IRCProtocol):

    def connected(self):
        self.nick('Testing')
        self.user('Testing', 'Testing')
        asyncio.async(self.delayed_join())

    @asyncio.coroutine
    def delayed_join(self):
        yield from asyncio.sleep(2)
        self.join('#test')

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
    bot = Bot.new(loop)
    loop.run_forever()
