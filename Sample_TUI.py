'''A terminal program demonstrating the use of Markov Bot Py'''

import Formatter
from MarkovBot import MarkovBot
import Tokenizer

fname = 'seuss.txt'
tokens = Tokenizer.group_aware(Tokenizer.read_all(fname))
bot = MarkovBot(tokens)

print('Five random Dr. Seuss sentences that start with sam and (most likely) end in a period:')
for i in range(5):
    walk = bot.walk(20, start = 'sam', stop = '.')
    print(Formatter.capped_sentences(walk))
