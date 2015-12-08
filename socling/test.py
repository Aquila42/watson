from tweetokenize import Tokenizer
import enchant
'''
gettokens = Tokenizer()
print gettokens.tokenize("thing.")

f = open("../gend_train/215__chris.txt")
line = f.readline()
line_list = (gettokens.tokenize(line))
print(line_list)
word = u'\U0001f339'
word_utf = word.encode("utf-8")
print(word == '\xF0\x9F\x8C\xB9')
print(word_utf == '\xF0\x9F\x8C\xB9')
'''
d = enchant.Dict("en")
print d.check("colour white")

