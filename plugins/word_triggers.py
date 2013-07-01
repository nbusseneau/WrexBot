# -*- coding: utf-8 -*-
"""Plugin handling word triggers in messages."""

import re
from plugin_base import PluginBase


class WordTriggers(PluginBase):
    """Plugin handling word triggers in messages."""
    def __init__(self, bot):
        super(WordTriggers, self).__init__(bot)
        self.commands = {'PRIVMSG': self.privmsg}

    def privmsg(self, sender, msg, *params):
        channel = params[0]
        regex = re.search(r'(ni)( .*?|)([,!?.]+)?$', msg, re.I)
        if regex:
            answer = 'EKKE EKKE EKKE EKKE PTANGYA ZIIINNGGGGGGG NI'
            term = regex.groups()[2]
            if term is not '' and term is not None:
                answer += term
            else:
                answer += '!'
            self.bot.privmsg(channel, answer)

        if "/fliptables" in msg:
            self.bot.privmsg(channel, "┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻")

        elif "/fliptable" in msg:
            self.bot.privmsg(channel, "(╯°□°)╯︵ ┻━┻")

        elif "/angryfliptable" in msg:
            self.bot.privmsg(channel, "(ノಠ益ಠ)ノ彡┻━┻")