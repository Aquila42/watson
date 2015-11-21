import re
str = "Hi I am 1234 years old"
print re.sub('[0-9]+',"DIGIT",str)
