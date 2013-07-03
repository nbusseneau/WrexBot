# -*- coding: utf-8 -*-
"""Simple Python IRC bot written for fun."""

import asyncore
import asynchat
import socket
import sys
import datetime
import logging
import re

# Some RFC constants
RPL_WELCOME = '001'
ERR_CANNOTSENDTOCHAN = '404'
ERR_ERRONEUSNICKNAME = '432'
ERR_NICKNAMEINUSE = '433'
ERR_NICKCOLLISION = '436'

# Some settings
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'  # Datetime format for logs and stdout
PLUGIN_DIR = 'plugins'  # Plugins directory


def now(date=True, fmt=DATE_FORMAT):
    """Current (Date)time formatted string.

    :keyword date: if Date should be returned as well (default=True)
    :type date: boolean
    :keyword fmt: strftime datetime format (default=DATE_FORMAT)
    :type fmt: string
    :return: current time (and date, if Date is True)
    :rtype: string

    """
    if date:
        return str(datetime.datetime.today().strftime(fmt))
    else:
        return str(datetime.time.today().strftime(fmt))


class WrexBot(asynchat.async_chat):
    """Simple Python IRC Bot written for fun."""
    def __init__(self,
                 nick='WrexBot',
                 channels=None,
                 plugins_to_load=None,
                 ignores=None,
                 admins=None,
                 custom_commands_prefix='!'):
        """Create an IRC WrexBot, ready for duty o/

        :param nick: bot nickname (default=WrexBot)
        :type nick: string
        :param channels: channels to join upon connection (default=[])
        :type channels: list of string
        :param plugins_to_load: plugins to load at startup
                                (default=['Shepard', 'Basic'])
        :type plugins_to_load: list of string
        :param ignores: users to ignore (default=[self.nick])
        :type ignores: list of string
        :param admins: users with admin rights on the bot (default=[])
        :type admins: list of string
        :param custom_commands_prefix: prefix for users/admins custom commands
                                       (default='!')
        :type custom_commands_prefix: string
        :return: a bot instance
        :rtype: WrexBot

        """
        # Replace None placeholders with default values:
        if channels is None:
            channels = []
        if plugins_to_load is None:
            plugins_to_load = ['Shepard', 'Basic']
        if ignores is None:
            ignores = [nick]  # avoid loops
        if admins is None:
            admins = []

        asynchat.async_chat.__init__(self)
        self.set_terminator('\n')
        self.nick = nick
        self.channels = channels
        self.plugins_to_load = plugins_to_load
        self.plugins = []
        for plugin_class in self.plugins_to_load:
            self.load_plugin(plugin_class)
        self.ignores = ignores
        self.admins = admins
        self.custom_commands_prefix = custom_commands_prefix

    def load_plugin(self, plugin_class):
        """Import plugin_class and append an instance to self.plugins"""
        # Plugin filenames and classes must follow convention, see README
        plugin_file = '_'.join(re.findall('[A-Z][^A-Z]*', plugin_class)).lower()
        _temp = __import__('{}.{}'.format(PLUGIN_DIR, plugin_file),
                           fromlist=[plugin_class])
        init = getattr(_temp, plugin_class)
        self.plugins.append(init(self))

    def unload_plugin(self, plugin_class):
        """Remove plugin_class from self.plugins"""
        for plugin in self.plugins:
            if plugin_class in str(plugin.__class__):
                self.plugins.remove(plugin)

    def shepardify(self, host, port=6667, encoding='utf-8'):
        """Connect to host:port and start operations."""
        self.encoding = encoding
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        asyncore.loop()

    def collect_incoming_data(self, data):
        """Decode incoming data using self.encoding and encode it in utf-8.

        When decoding fails, raw data is processed (should work in most cases).
        This is to allow the bot to connect to servers using for example latin-1
        charset in their welcome message but utf-8 as regular charset otherwise.

        """
        try:
            data = data.decode(self.encoding)
            self.incoming.append(data.encode('utf-8'))
        except (UnicodeDecodeError, UnicodeEncodeError):
            logging.warning('Warning: data not decoded from {}'.format(self.encoding))
            self.incoming.append(data)

    def found_terminator(self):
        """Handle data reception.

        Split data in command (with its additional parameters), sender and msg.

        """
        # Take out \r if server follows RFC
        data = self._get_data().rstrip('\r')
        logging.debug(data)
        # Take out sender (prefixed with the first ':')
        if data.startswith(':'):
            sender, data = data.split(' ', 1)
            sender = sender[1:].split('!', 1)[0]  # take out ':' and rubbish
        else:
            sender = ''
        # Take out message (after the second ':')
        try:
            parts, msg = data.split(' :', 1)
        except ValueError:  # in case there's no message
            parts = data
            msg = ''
        # Split RFC command (e.g. PRIVMSG) and its parameters
        parts = parts.split(' ')
        command = parts[0]
        params = parts[1:]  # can be an empty list

        # Process data (unless we ignore sender)
        if sender not in self.ignores:
            self.dispatch(command, sender, msg, *params)

    def dispatch(self, command, sender, msg, *params):
        """Dispatch received data based on command."""
        logging.info('RECEIVED: {} {} {} {}'.format(command, sender,
                                                    ' '.join(params), msg))

        if 'PING' in command:
            self.write('PONG', msg)
        elif 'PRIVMSG' in command:
            recipient = params[0]
            self.print_msg(recipient, sender, msg)
            # Custom commands handling
            if msg.startswith(self.custom_commands_prefix):
                parts = msg.split(' ')
                custom_command = parts[0].lstrip(self.custom_commands_prefix)
                custom_params = parts[1:]  # can be an empty list
                for plugin in self.plugins:
                    if plugin.accept(custom_command):
                        plugin.dispatch(custom_command, sender, recipient,
                                        *custom_params, custom=True,
                                        admin=sender in self.admins)
        elif RPL_WELCOME in command:  # connect to default channels upon welcome
            for channel in self.channels:
                self.join(channel)
        # Various RFC constants handlers
        elif ERR_CANNOTSENDTOCHAN in command:
            self.print_msg(self.nick, sender, 'Cannot send to chan')
        elif ERR_ERRONEUSNICKNAME in command:
            self.print_msg(self.nick, sender, 'Invalid nickname')
        elif ERR_NICKNAMEINUSE in command or ERR_NICKCOLLISION in command:
            self.print_msg(self.nick, sender, 'Nickname already in use')

        # Plugin handlers
        for plugin in self.plugins:
            if plugin.accept(command):
                plugin.dispatch(command, sender, msg, *params)

    def write(self, *args):
        """Try to encode message and push it to the server."""
        msg = ' '.join(args)
        logging.info('SENT: {}'.format(msg))
        try:
            self.push(msg.encode(self.encoding) + '\r\n')
        except (UnicodeDecodeError, UnicodeEncodeError):
            self.push(msg + '\r\n')

    def handle_connect(self):
        """RFC connection protocol."""
        self.write('NICK', self.nick)
        self.write('USER', self.nick, self.nick, self.nick, ":" + self.nick)

    def join(self, channel):
        """RFC JOIN message."""
        self.write('JOIN', channel)

    def part(self, channel):
        """RFC PART message."""
        self.write('PART', channel)

    def privmsg(self, recipient, msg):
        """RFC PRIVMSG message."""
        self.write('PRIVMSG', recipient, ':' + msg)
        self.print_msg(recipient, self.nick, msg)

    def print_msg(self, recipient, sender, msg):
        """Format and print a received message."""
        print "[{}] {} | {}: {}".format(now(), recipient, sender, msg)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt=DATE_FORMAT, stream=sys.stdout)
    logging.getLogger().setLevel(logging.DEBUG)
    wrex_bot = WrexBot('WrexBot', channels=['#test-bot'], admins=['Skymirrh'])
    wrex_bot.load_plugin('WordTriggers')
    wrex_bot.shepardify('irc.epiknet.org')