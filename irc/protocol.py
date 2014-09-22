import asyncio
import re

class IRCProtocol(asyncio.Protocol):
    """
    IRC protocol class
    """

    MSG_PATTERN = re.compile(
        r'''\A
        (?: : (?P<prefix>[^ ]+) [ ]+ )?
        (?P<command> \d{3} | [_a-zA-Z]+ )
        (?P<args>
            (?: [ ]+ [^: \x00\r\n][^ \x00\r\n]* )*
        )
        (?:
            [ ]+ [:] (?P<trailing> [^\x00\r\n]*)
        )?
        [ ]*
        \Z''',
        flags=re.VERBOSE)

    def connected(self):
        pass

    def on_message(self, sender, target, message):
        pass

    def write(self, data):
        print("Sent: {}".format(data))
        data = '{}\n'.format(data).encode('utf8')
        self.transport.write(data)

    def nick(self, nickname):
        self.write('NICK {}'.format(nickname))

    def user(self, user, name):
        self.write('USER {} 8 * : {}'.format(user, name))

    def message(self, recv, message):
        self.write('PRIVMSG {} :{}'.format(recv, message))

    def join(self, channel):
        self.write('JOIN {}'.format(channel))

    def connection_made(self, transport):
        self.transport = transport
        self.connected()

    def connection_lost(self, exc):
        pass

    def data_received(self, data):
        data = data.decode('utf8')
        lines = data.split('\r\n')
        for line in lines:
            if len(line.strip()) == 0:
                continue
            print('Got: {}'.format(repr(line)))
            command, args, prefix = self._parse(line)
            if command == 'PING':
                self.write('PONG :{}'.format(''.join(args)))
            elif command == 'PRIVMSG':
                target, message = args
                sender = self._parse_user(prefix)
                self.on_message(sender, target, message)

    def _parse_user(self, hostmask):
        username, hostmask = hostmask.split('!')
        ident, hostname = hostmask.split('@')
        return username, ident, hostname

    def _parse(self, data):
        m = IRCProtocol.MSG_PATTERN.match(data)
        if not m:
            raise ValueError("Error: received invalid str. {}".format(data))

        argstr = m.group('args').lstrip(' ')
        if argstr:
            args = re.split(' +', argstr)
        else:
            args = []

        if m.group('trailing'):
            args.append(m.group('trailing'))

        return m.group('command'), args, m.group('prefix')

    def eof_received(self):
        self.transport.close()

