# -*- coding: utf-8 -*-

import asyncore
import asynchat
import socket
import sys
import datetime
import logging
from os.path import normpath, join, dirname

# Some RFC constants
RPL_WELCOME = '001'
ERR_ERRONEUSNICKNAME = '432'
ERR_NICKNAMEINUSE = '433'
ERR_NICKCOLLISION = '436'

try:
    from settings import *
except ImportError:
    # In case settings.py does not exist, defaults are loaded:
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    PLUGIN_DIR = normpath(join(dirname(__file__), 'plugins'))
    PLUGINS = []


def now(date=True, fmt=DATE_FORMAT):
    """Current (Date)time formatted string

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
    def __init__(self, nick, *channels):
        """IRC WrexBot, ready for duty o/

        :param nick: bot nickname
        :type nick: string
        :param channels: channels to join
        :type channels: list of strings
        :return: a WrexBot instance
        :rtype: WrexBot
        """
        asynchat.async_chat.__init__(self)
        self.collect_incoming_data = self._collect_incoming_data
        self.set_terminator('\n')
        self.nick = nick
        self.channels = channels

    def shepardify(self, host, port=6667):
        """Connect to host:port and start operations

        :param host: IRC server address
        :type host: string
        :param port: connection port
        :type port: integer
        """
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        asyncore.loop()

    def found_terminator(self):
        """Handle data reception"""
        # Take out \r if server follows RFC
        data = self._get_data().rstrip('\r')

        logging.debug(data)

        if data.startswith(':'):
            sender, data = data.split(' ', 1)
        else:
            sender = ':'
        parts = data.split(' :', 1)
        parts = parts[0].split(' ') + parts[1:]
        self.dispatch(parts[0], sender[1:], *parts[1:])

    def dispatch(self, command, sender, *args):
        logging.info('RECEIVED: {} {} {}'.format(command, sender, ' '.join(args)))

        if 'PING' in command:
            self.write('PONG', args[0])

        elif 'PRIVMSG' in command:
            self.print_msg(args[0], sender, args[1])

        elif RPL_WELCOME in command:
            for channel in self.channels:
                self.join(channel)

        elif ERR_ERRONEUSNICKNAME in command:
            print 'Invalid nickname'

        elif ERR_NICKNAMEINUSE in command or ERR_NICKCOLLISION in command:
            print 'Nickname already in use'

        else:
            for plugin in PLUGINS:
                if PLUGIN_DIR.plugin.accept(command):
                    print PLUGIN_DIR.plugin.handle(command, sender, *args)

    def write(self, *args):
        args = [arg.encode('utf-8') for arg in args]
        msg = ' '.join(args)
        logging.info('SENT: {}'.format(msg))
        self.push(msg + '\r\n')

    def handle_connect(self):
        self.write('NICK', self.nick)
        self.write('USER', self.nick, self.nick, self.nick, ":" + self.nick)

    def join(self, channel):
        self.write('JOIN', channel)

    def send_msg(self, recipient, message):
        self.write('PRIVMSG', recipient, message)
        print

    def print_msg(self, channel, sender, msg):
        print "[{}] {} | {}: {}".format(now(), channel, sender.split('!', 1)[0], msg)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt=DATE_FORMAT, stream=sys.stdout)
    logging.getLogger().setLevel(logging.DEBUG)
    wrex_bot = WrexBot('WrexBot', '#test-bot')
    wrex_bot.shepardify('irc.epiknet.org')