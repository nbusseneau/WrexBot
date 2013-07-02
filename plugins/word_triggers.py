# -*- coding: utf-8 -*-
"""Plugin handling word triggers in messages."""

import re
from plugin_base import PluginBase
import hodor


class WordTriggers(PluginBase):
    """Plugin handling word triggers in messages."""
    def __init__(self, bot):
        super(WordTriggers, self).__init__(bot)
        self.commands = {'PRIVMSG': self.privmsg}

    def privmsg(self, sender, msg, *params):
        channel = params[0]
        regex = re.search(r'(Ni)(?!\w).*?([\W1_]+)?$', msg, re.I)
        if regex:
            answer = 'Ekke ekke ekke ekke ptangya ziiinnggggggg ni'
            ni, term = regex.groups()
            if ni.isupper():
                answer = answer.upper()
            if term is not None:
                answer += term
            else:
                answer += '!'
            self.bot.privmsg(channel, answer)

        regex = re.search(r'(Hodor)(?!\w).*?([\W1]+)?$', msg, re.I)
        if regex:
            self.bot.privmsg(channel, hodor.hodor())