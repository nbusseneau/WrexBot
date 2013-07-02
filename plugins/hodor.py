# -*- coding: utf-8 -*-

import random


def hodor(max_o=3, max_words=3, max_sentences=4):
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


if __name__ == '__main__':
    print hodor()