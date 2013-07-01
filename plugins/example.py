# -*- coding: utf-8 -*-
"""Plugin example."""

from plugin_base import PluginBase


class Example(PluginBase):
    """Plugin example."""
    def __init__(self, bot):
        super(Example, self).__init__(bot)
        self.commands = {'RFC_command': self.rfc_command_handler}
        self.user_commands = {'user_command': self.user_command_handler}
        self.admin_commands = {'admin_command': self.admin_command_handler}

    # Note that in the handlers, you must have all parameters to be consistent
    # with the PluginBase switches, even if you don't use them all.
    # Make calls to self.bot functions when needed.
    def rfc_command_handler(self, sender, msg, *params):
        # Process command using sender, msg and params
        self.bot.privmsg(sender, 'RFC_command has been processed.')

    def user_command_handler(self, sender, *params):
        # Process command using sender and params
        self.bot.privmsg(sender, 'user_command has been processed.')

    def admin_command_handler(self, sender, *params):
        # Process command using sender and params
        self.bot.privmsg(sender, 'admin_command has been processed.')