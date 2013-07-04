# -*- coding: utf-8 -*-
"""Plugin handling some basic admins commands."""

from operator import lt, le, eq, ne, ge, gt
from collections import OrderedDict
from plugin_base import PluginBase


class Admin(PluginBase):
    """Plugin handling basic admin commands."""
    def __init__(self, bot):
        super(Admin, self).__init__(bot)
        # We use an OrederedDict so that when we use .items() to list
        # all available commands, it keeps the order of the dict
        self.admin_commands = OrderedDict([
            # ('command', (number of parameters for dispatch, operator, handler,
            #             'usage',
            #             'help_msg')),
            ('help', (2, ge, self.help,
                     'help [command]',
                     'Show list of usable commands or command usage.')),
            ('say', (2, ne, self.say,
                    'say [channel_or_user] [msg]',
                    'Send a message to a channel or a user.')),
            ('join', (1, lt, self.join,
                     'join [#channel] [#channel]...',
                     'Join one or several channels.')),
            ('part', (1, lt, self.part,
                     'part [#channel] [#channel]...',
                     'Part one or several channels.')),
            ('admins', (0, lt, self.admins,
                       'admins',
                       'Show the list of bot admins.')),
            ('admin', (1, lt, self.admin,
                      'admin [username] [username]...',
                      'Add one or several bot admins.')),
            ('unadmin', (1, lt, self.unadmin,
                        'unadmin [username] [username]...',
                        'Remove one or several bot admins.')),
            ('ignores', (0, lt, self.ignores,
                        'ignores',
                        'Show the list of ignored users')),
            ('ignore', (1, lt, self.ignore,
                       'ignore [username] [username]...',
                       'Add one or several ignored users.')),
            ('unignore', (1, lt, self.unignore,
                         'unignore [username] [username]...',
                         'Remove one or several ignored users.')),
        ])

    def dispatch(self, sender, command, params, msg, custom=False, admin=False):
        """Dispatch according to command and pass the other parameters.

        Base dispatch function is overloaded so we can have a cleaner approach
        to handle admin commands with usage and help messages.

        What happens is:
            * we receive an admin command.
            * we check the number of parameters supplied.
            * if the number of parameters is invalid, we print command usage.
            * if the number of parameters is valid, we call command handler.

        """
        if custom and admin:  # we care only about admin commands
            recipient = params[0]
            # In case of PRIVMSG to the bot, answer to the sender
            # Else respond in channel
            if recipient == self.bot.nick:
                recipient = sender
            parts = msg.split(' ')
            command = parts[0].lstrip(self.bot.prefix)
            params = parts[1:]  # can be an empty list
            nb_params, operator, handler, usage, help_msg = self.admin_commands[command]
            if operator(len(params), nb_params):
                self.bot.privmsg(recipient, self.usage(usage))
            else:
                handler(sender, params, recipient)

    def usage(self, usage):
        return 'Usage: {}{}\n\t'.format(self.bot.prefix, usage)

    def help(self, sender, params, recipient):
        args = len(params)
        if args == 0:
            self.bot.privmsg(recipient, 'List of available admin commands:')
            for command, data in self.admin_commands.items():
                self.bot.privmsg(recipient, '{} -> {}'.format(command, data[-1]))
            self.bot.privmsg(recipient, 'Use "!help [command]" for command usage.')
        else:
            admin_command = params[0]
            try:
                data = self.admin_commands[admin_command]
                self.bot.privmsg(recipient, '{}\n{}'.format(self.usage(data[-2]), data[-1]))
            except KeyError:
                self.bot.privmsg(recipient, "Admin command: '{}' doesn't exist.".format(admin_command))

    def say(self, sender, params, recipient):
        self.bot.privmsg(params[0], ' '.join(params[1:]))

    def join(self, sender, params, recipient):
        for channel in params:
            self.bot.join(channel)

    def part(self, sender, params, recipient):
        for channel in params:
            self.bot.part(channel)

    def admins(self, sender, params, recipient):
        self.bot.privmsg(recipient, 'Admins list: {}'.format(' '.join(self.bot.admins)))

    def admin(self, sender, params, recipient):
        for admin in params:
            if admin not in self.bot.admins:
                self.bot.admins.append(admin)

    def unadmin(self, sender, params, recipient):
        for admin in params:
            self.bot.admins.remove(admin)

    def ignores(self, sender, params, recipient):
        self.bot.privmsg(recipient, 'Ignore list: {}'.format(' '.join(self.bot.ignores)))

    def ignore(self, sender, params, recipient):
        for ignore in params:
            if ignore not in self.bot.ignores:
                self.bot.ignores.append(ignore)

    def unignore(self, sender, params, recipient):
        for ignore in params:
            self.bot.ignores.remove(ignore)