# -*- coding: utf-8 -*-
"""Plugin handling Shepard/Wrex interaction."""

import re
from plugin_base import PluginBase


class Shepard(PluginBase):
    """Plugin handling Shepard/Wrex interaction."""
    def __init__(self, bot):
        super(Shepard, self).__init__(bot)
        self.commands = {'PRIVMSG': self.privmsg}

    def privmsg(self, sender, msg, *params):
        channel = params[0]
        if channel == self.bot.nick:
            channel = sender
        regex = re.search(r'(?<!\w)(Wrex|Shepard)(?!\w).*?([\W1_]+)?$', msg, re.I+re.U)
        if regex:
            shepwrex, term = regex.groups()
            if re.match(r'Wrex', shepwrex, re.I):
                shepwrex = 'Shepard'.upper() if shepwrex.isupper() else 'Shepard'
            else:
                shepwrex = 'Wrex'.upper() if shepwrex.isupper() else 'Wrex'
            if term is not None:
                answer = shepwrex + term
            else:
                answer = shepwrex + '.'
            self.bot.privmsg(channel, answer)