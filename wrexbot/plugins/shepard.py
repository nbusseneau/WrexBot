# -*- coding: utf-8 -*-
"""Plugin handling Shepard/Wrex interaction and some other triggers."""

import re
import random
from plugin_base import PluginBase


class Shepard(PluginBase):
    """Plugin handling Shepard/Wrex interaction and some other triggers."""
    def __init__(self, bot):
        super(Shepard, self).__init__(bot)
        self.commands = {'PRIVMSG': self.privmsg}

    def privmsg(self, sender, params, msg):
        print (sender, params, msg)

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

        regex = re.search(r'(?<!\w)(Ni)(?!\w).*?([\W1_]+)?$', msg, re.I+re.U)
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

        regex = re.search(r'(?<!\w)(Hodor(?:(?:at)?ing|e(?:u)?r)?)(?!\w).*?([\W1]+)?$', msg, re.I+re.U)
        if regex:
            self.bot.privmsg(channel, self.hodor())

    def hodor(self, max_o=3, max_words=3, max_sentences=4):
        """Hoooodoor hodor! Hodor. Hodor? ...Hodor, hodor!!"""
        def get_punctuation(weak=False):
            """Return weak or strong punctuation for inbetween words/sequences"""
            if not weak:
                if random.random() < 0.2:
                    punctuation = '?'
                elif random.random() < 0.2:
                    punctuation = '!'
                else:
                    punctuation = '.'
            else:
                if random.random() < 0.75:  # 75% chance to have a space
                    punctuation = ''
                else:  # 25% to have a comma
                    punctuation = ','

            # Ten percent chance to triple punctuation if '.' or add a '!' if '?' or '!'
            if random.random() < 0.1:
                if punctuation in ['.']:
                    punctuation *= 3
                elif punctuation in ['?', '!']:
                    punctuation += '!'

            if punctuation == ' ':
                punctuation = ''
            return punctuation

        def get_word():
            """Return 'hodor' lexeme (variants: 'hoooodooor' and 'hodooor')"""
            o = lambda x: 'o' * int(random.triangular(1, x+2, 1))
            # 5% chance to have something like 'hooodooor'
            if random.random() < 0.05:
                return 'ho{}do{}r'.format(o(max_o), o(max_o))
            # 15% chance to have something like 'hodooor'
            elif random.random() < 0.15:
                return 'hodo{}r'.format(o(max_o))
            # 80% to have plain 'hodor'
            else:
                return 'hodor'

        def get_sentence():
            """Return a simple sentence of 'hodor' words."""
            # Between 1 and max_words words (max probability: 2 word-long)
            num_words = int(random.triangular(1, max_words+1, (max_words+1)/3))
            words = [get_word() + get_punctuation(weak=True) for i in range(num_words)]
            sentence = ' '.join(words).rstrip(',')
            if random.random() < 0.05:  # 5% chance to yell
                return sentence.upper()
            elif random.random() < 0.05:  # 5% chance to whisper
                return '...' + sentence.capitalize()
            else:
                return sentence.capitalize()

        def get_quote():
            """Return an "Hodor seal of approval" quote."""
            # Between 1 and max_sentences sentences (max probability: 2 sentence-long)
            num_sequences = int(random.triangular(1, max_sentences+1, 2))
            quote = [get_sentence()+get_punctuation(weak=False) for i in range(num_sequences)]
            return ' '.join(quote)

        return get_quote()