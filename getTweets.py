# This tests the classifier without front end

from classify import classified
import nltk

handle = "Adele"
py_obj = classified(handle)
print(py_obj)

