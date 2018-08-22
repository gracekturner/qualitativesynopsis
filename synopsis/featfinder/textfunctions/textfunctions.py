import sys
sys.path.append('../')
from globalconstants import *
from input_tester.input_testing import test_inputs

#REMOVE(text, delimeter_list, rep = " ")
# removes any delimeters in the delimeter_list from the string text
#and replaces it with rep (default " "). returns resulting text.
def remove(text, delimeter_list, rep = " "):
    ti = [(text, STR, "text", "remove"),
    (delimeter_list,LIST, "delimeter_list", "remove"),
    (rep, STR, "text", "remove")]
    test_inputs(ti)
    for each in delimeter_list:
        text = text.replace(each, rep)
    return text
