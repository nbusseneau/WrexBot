# -*- coding: utf-8 -*-
"""Simple Python IRC bot written for fun."""

import asyncore
import asynchat
import socket
import sys
import datetime
import logging
from os.path import normpath, join, dirname

# Some RFC constants
RPL_WELCOME = '001'
ERR_CANNOTSENDTOCHAN = '404'
ERR_ERRONEUSNICKNAME = '432'
ERR_NICKNAMEINUSE = '433'
ERR_NICKCOLLISION = '436'

# Some settings
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'  # Datetime format for logs and stdout
PLUGIN_DIR = normpath(join(dirname(__file__), 'plugins'))  # Plugins directory


def now(date=True, fmt=DATE_FORMAT):
    """Current (Date)time formatted string.

    :keyword date: if Date should be returned as well (default=True)
    :type date: boolean
    :keyword fmt: strftime datetime format
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

    def __init__(self, nick, *channels):
        """Create an IRC WrexBot, ready for duty o/

        :param nick: bot nickname
        :type nick: string
        :param channels: default channels to join
        :type channels: list of strings
        :return: a WrexBot instance
        :rtype: WrexBot

        """
        asynchat.async_chat.__init__(self)
        self.set_terminator('\n')
        self.nick = nick
        self.ignore_list = [self.nick]
        self.masters = []
        self.channels = channels

    def set_channels(self, *channels):
        """Set list of default connected channels."""
        self.channels = channels

    def set_ignore_list(self, *ignore_list):
        """Set list of ignored users."""
        self.ignore_list = list(ignore_list).append(self.nick)

    def _ignore(self, ignore):
        """Add ignore to the ignore list."""
        self.ignore_list.append(ignore)

    def _unignore(self, ignore):
        """Remove ignore from the ignore list."""
        self.ignore_list.remove(ignore)

    def set_masters(self, *masters):
        """Set list of bot masters users."""
        self.masters = list(masters)

    def _master(self, master):
        """Add master to the masters list."""
        self.masters.append(master)

    def _unmaster(self, master):
        """Remove master from the masters list."""
        self.masters.remove(master)

    def set_plugins(self, *plugins):
        """"""

    def collect_incoming_data(self, data):
        """Decode incoming data and encode it in utf-8."""
        encoding = iter(['utf-8', 'cp1252', 'iso-8859-1'])
        ENCODING_FOUND_OR_NOT_SUPPORTED = False
        while not ENCODING_FOUND_OR_NOT_SUPPORTED:
            try:
                data = data.decode(encoding.next())
                ENCODING_FOUND_OR_NOT_SUPPORTED = True
            except UnicodeDecodeError:
                pass  # Try next encoding
            except StopIteration:
                logging.info('Data not decoded.')
                ENCODING_FOUND_OR_NOT_SUPPORTED = True
        self.incoming.append(data.encode('utf-8'))

    def shepardify(self, host, port=6667):
        """Connect to host:port and start operations.

        :param host: IRC server address
        :type host: string
        :param port: connection port
        :type port: integer

        """
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        asyncore.loop()

    def found_terminator(self):
        """Handle data reception."""
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

        if sender not in self.ignore_list:
            self.dispatch(command, sender, msg, *params)

    def dispatch(self, command, sender, msg, *params):
        """Dispatch received data based on command.

        :param command: received RFC command
        :type command: string
        :param sender: received data sender
        :type sender: string
        :param msg: received message
        :type msg: string
        :args params: RFC command parameters
        :type params: list of strings

        """
        logging.info('RECEIVED: {} {} {} {}'.format(command, sender,
                                                    ' '.join(params), msg))

        if 'PING' in command:
            self.write('PONG', msg)

        elif 'PRIVMSG' in command:
            self.print_msg(params[0], sender, msg)
            if msg.startswith('!'):
                parts = msg.split(' ')
                command = parts[0][1:]  # we take out the '!'
                params = parts[1:]  # can be an empty list
                if sender in self.masters:
                    self.master_command(command, sender, *params)
                else:
                    self.user_command(command, sender, *params)

        elif RPL_WELCOME in command:
            for channel in self.channels:
                self.join(channel)

        elif ERR_CANNOTSENDTOCHAN in command:
            self.print_msg(self.nick, sender, 'Cannot send to chan')

        elif ERR_ERRONEUSNICKNAME in command:
            self.print_msg(self.nick, sender, 'Invalid nickname')

        elif ERR_NICKNAMEINUSE in command or ERR_NICKCOLLISION in command:
            self.print_msg(self.nick, sender, 'Nickname already in use')

        else:
            for plugin in PLUGINS:
                if plugin.accept(command):
                    plugin.dispatch(command, sender, msg, *params)

    def user_command(self, command, sender, *params):
        """Execute a user command.
        
        :param command: user command
        :type command: string
        :param sender: sender
        :type sender: string
        :args params: command parameters
        :type params: list of strings
        
        """
        # There are no user command by default
        for plugin in PLUGINS:
            if plugin.accept(command):
                plugin.execute(command, sender, *params)

    def master_command(self, command, sender, *params):
        """Execute a master command.
        
        :param command: master command
        :type command: string
        :param sender: sender
        :type sender: string
        :args params: command parameters
        :type params: list of strings
        
        """
        command = command.lower()

        if 'say' in command:
            if len(params) != 2:
                self.send_msg(sender, 'Usage: !say user_or_channel message')
            else:
                self.send_msg(params[0], params[1])

        elif 'join' in command:
            for channel in params:
                self.join(channel)

        elif 'part' in command:
            for channel in params:
                self.part(channel)

        elif 'unmaster' in command:
            for master in params:
                self._unmaster(master)

        elif 'master' in command:
            for master in params:
                self._master(master)

        elif 'unignore' in command:
            for ignore in params:
                self._unignore(ignore)

        elif 'ignore' in command:
            for ignore in params:
                self._ignore(ignore)

        else:
            for plugin in PLUGINS:
                if plugin.accept(command):
                    plugin.execute(command, sender, *params)

    def write(self, *args):
        """Process args and push them to the server."""
        msg = ' '.join(args)
        logging.info('SENT: {}'.format(msg))
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

    def send_msg(self, recipient, msg):
        """RFC PRIVMSG message.

        :param recipient: a channel or a user
        :type recipient: string
        :param msg: the message
        :type msg: string
        
        """
        self.write('PRIVMSG', recipient, ':' + msg)
        self.print_msg(recipient, self.nick, msg)

    def print_msg(self, recipient, sender, msg):
        """Format and print a received message.
        
        :param recipient: message recipient (typically WrexBot or a channel)
        :type recipient: string
        :param sender: message sender
        :type sender: string
        :param msg: message
        :type msg: string
        
        """
        print "[{}] {} | {}: {}".format(now(), recipient, sender, msg)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt=DATE_FORMAT, stream=sys.stdout)
    logging.getLogger().setLevel(logging.DEBUG)
    wrex_bot = WrexBot('WrexBot', '#test-bot')
    wrex_bot.add_master('Skymirrh')
    wrex_bot.shepardify('irc.epiknet.org')