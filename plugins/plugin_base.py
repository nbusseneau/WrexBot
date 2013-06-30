# -*- coding: utf-8 -*-
"""Base class from which plugins should inherit."""


class PluginBase(object):
    """Base class from which plugins should inherit."""
    def __init__(self, wrex_bot):
        """Create a PluginBase associated to bot wrex_bot"""
        self.bot = wrex_bot
        self.commands = {}
        self.custom_commands = {}

    def accept(self, command):
        """Return true if command is to be processed by the plugin"""
        if command in self.commands or command in self.custom_commands:
            return True
        else:
            return False

    def dispatch(self, command, sender, msg, *params):
        """Dispatch according to command and pass the other parameters"""
        self.commands[command](sender, msg, *params)

    def execute(self, command, sender, *params):
        """Execute custom command by passing the other parameters"""
        self.custom_commands[command](sender, *params)