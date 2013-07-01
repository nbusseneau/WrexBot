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
        regex = re.search(r'(Wrex|Shepard)(.*?|)([,!?.]+)?$', msg, re.I)
        if regex:
            shepwrex, _,  term = regex.groups()
            if 'Wrex' in shepwrex:
                shepwrex = 'Shepard'
            else:
                shepwrex = 'Wrex'
            if term is not '':
                answer = shepwrex + term
            else:
                answer = shepwrex + '.'
            self.bot.privmsg(params[0], answer)