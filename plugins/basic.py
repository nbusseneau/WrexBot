# -*- coding: utf-8 -*-
"""Plugin handling basic bot functions."""

import re
from plugin_base import PluginBase


class Basic(PluginBase):
    """Plugin handling basic bot functions."""
    def __init__(self, bot):
        super(Basic, self).__init__(bot)
        self.user_commands = {}
        self.master_commands = {'say': self.say,
                                'join': self.join,
                                'part': self.part,
                                'admins': self.admins,
                                'admin': self.admin,
                                'unadmin': self.unadmin,
                                'ignores': self.ignores,
                                'ignore': self.ignore,
                                'unignore': self.unignore,
                                }

    def say(self, sender, channel, *params):
        self.bot.privmsg(params[0], params[1])

    def join(self, sender, channel, *params):
        for channel in params:
            self.bot.join(channel)

    def part(self, sender, channel, *params):
        for channel in params:
            self.bot.part(channel)

    def admins(self, sender, channel, *params):
        self.privmsg(channel, 'Admins list: {}'.format(' '.join(self.bot.admins)))

    def admin(self, sender, channel, *params):
        for admin in params:
            if admin not in self.bot.admins:
                self.bot.admins.append(admin)

    def unadmin(self, sender, channel, *params):
        for admin in params:
            self.bot.admins.remove(admin)

    def ignores(self, sender, channel, *params):
        self.privmsg(channel, 'Ignore list: {}'.format(' '.join(self.bot.ignores)))

    def ignore(self, sender, channel, *params):
        for ignore in params:
            if ignore not in self.bot.ignores:
                self.bot.ignores.append(ignore)

    def unignore(self, sender, channel, *params):
        for ignore in params:
            self.bot.ignores.remove(ignore)