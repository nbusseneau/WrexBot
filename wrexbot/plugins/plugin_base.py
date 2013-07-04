# -*- coding: utf-8 -*-
"""Base class from which plugins should inherit.

Implementation examples
-----------------------
    * example.py provides a complete dummy plugin for you to read
    * shepard.py may interest you if you're looking for a word trigger plugin
    * admin.py may interest you if you're looking for a custom commands plugin


PEP 8 -- Style Guide for Python Code (and Plugins)
--------------------------------------------------
http://www.python.org/dev/peps/pep-0008/#naming-conventions

For the bot to handle plugins in a simple way, filenames and classes names
must respect PEP 8 namings conventions:
    * filenames are all-lowercase, with underscores separating words
    * class names use the CapitalizedWords (or CamelCase) convention

Examples (formatted as "filename > class name"):
    * plugin_base.py > PluginBase
    * shepard.py > Shepard
    * outstanding_non_non_unrivaled_plugin.py > OutstandingNonNonUnrivaledPlugin

"""


class PluginBase(object):
    """Base class from which plugins should inherit."""
    def __init__(self, wrex_bot):
        """Create a PluginBase associated to bot wrex_bot."""
        self.bot = wrex_bot
        self.commands = {}
        self.user_commands = {}
        self.admin_commands = {}

    def dispatch(self, sender, command, params, msg, custom=False, admin=False):
        """Dispatch according to command and pass the other parameters."""
        if not custom and command in self.commands:
            self.commands[command](sender, params, msg)
        elif custom:
            recipient = params[0]
            # In case of PRIVMSG to the bot, answer to the sender
            # Else respond in channel
            if recipient == self.bot.nick:
                recipient = sender
            parts = msg.split(' ')
            command = parts[0].lstrip(self.bot.prefix)
            params = parts[1:]  # can be an empty list
            if admin and command in self.admin_commands:
                self.admin_commands[command](sender, params, recipient)
            elif command in self.user_commands:
                self.user_commands[command](sender, params, recipient)