# -*- coding: utf-8 -*-
"""Plugin handling basic bot functions."""

from plugin_base import PluginBase


class Basic(PluginBase):
    """Plugin handling basic bot functions."""
    def __init__(self, bot):
        super(Basic, self).__init__(bot)
        self.admin_commands = {'say': self.say,
                                'join': self.join,
                                'part': self.part,
                                'admins': self.admins,
                                'admin': self.admin,
                                'unadmin': self.unadmin,
                                'ignores': self.ignores,
                                'ignore': self.ignore,
                                'unignore': self.unignore,
                                }

    def say(self, sender, recipient, *params):
        if len(params) != 2:
            self.bot.privmsg(recipient, 'Usage: !say [channel_or_user] [msg]')
        else:
            self.bot.privmsg(params[0], ' '.join(params[1:]))

    def join(self, sender, recipient, *params):
        if len(params) < 1:
            self.bot.privmsg(recipient, 'Usage: !join [#channel] [#channel]...')
        else:
            for channel in params:
                if not channel.startswith('#'):
                    channel = '#' + channel
                self.bot.join(channel)

    def part(self, sender, recipient, *params):
        if len(params) < 1:
            self.bot.privmsg(recipient, 'Usage: !part [#channel] [#channel]...')
        else:
            for channel in params:
                if not channel.startswith('#'):
                    channel = '#' + channel
                self.bot.part(channel)

    def admins(self, sender, recipient, *params):
        self.bot.privmsg(recipient, 'Admins list: {}'.format(' '.join(self.bot.admins)))

    def admin(self, sender, recipient, *params):
        if len(params) < 1:
            self.bot.privmsg(recipient, 'Usage: !admin [username] [username]...')
        else:
            for admin in params:
                if admin not in self.bot.admins:
                    self.bot.admins.append(admin)

    def unadmin(self, sender, recipient, *params):
        if len(params) < 1:
            self.bot.privmsg(recipient, 'Usage: !unadmin [username] [username]...')
        else:
            for admin in params:
                self.bot.admins.remove(admin)

    def ignores(self, sender, recipient, *params):
        self.bot.privmsg(recipient, 'Ignore list: {}'.format(' '.join(self.bot.ignores)))

    def ignore(self, sender, recipient, *params):
        if len(params) < 1:
            self.bot.privmsg(recipient, 'Usage: !ignore [username] [username]...')
        else:
            for ignore in params:
                if ignore not in self.bot.ignores:
                    self.bot.ignores.append(ignore)

    def unignore(self, sender, recipient, *params):
        if len(params) < 1:
            self.bot.privmsg(recipient, 'Usage: !unignore [username] [username]...')
        else:
            for ignore in params:
                self.bot.ignores.remove(ignore)