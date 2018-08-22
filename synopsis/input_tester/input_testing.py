import pandas
import sys
sys.path.append('../')
from globalconstants import *

# input tester was written to reduce workload on input testing and to standardize
# input type error messages.

#CHECK_INPUT_MATCH()
#checks that the type of data and type matches
# returns true if match, false otherwise
def check_input_match(input, type):
    #corner case: if it asks to test for a list-like object (list, tuple, etc.)
    #checks that it is both iterable and index-able NOTE need to do indexable bit
    if type  == LIST:
        try:
            listy = iter(input)
        except:
            return False
        if isinstance(input, str):
            return False
    if type == EXCEL:

        try:
            pandas.read_excel(input)
        except:
            return False
    #if datatype is in DATATYPE_DICT (from globalconstants) use isinstance
    if type in DATATYPE_DICT:
        if not isinstance(input, DATATYPE_DICT[type]):
            return False
    return True


#TEST_INPUT()
#test_input(input) is individual input testing: variable input is a tuple of form
#(variable, datatype, variable_name, function_name)
# where variable is the variable being tested
#datatype must be from the set {STR, INT, PANDAS, DICT, LIST} to work
#variable_name is what the variable is called (e.g. "list_of_inputs")
#function_name is the name of the function that called test_input() (that
#variable belongs to)
#LIST only tests if datatype is iterable NOTE should also test if is index-able
#returns a TypeError if it finds a mismatch between datatype and variable type,
#returns a ValueError if it finds something wonky with the input NOTE
# should make this less hacky

def test_input(input):

    # testing the inputs of the test_input (lol)
    if not isinstance(input, tuple):
        raise ValueError("test_input's input should be of type tuple")
    if len(input) != 4:
        raise ValueError("test_input's input should be a tuple of length 4")
    if input[1] != LIST and input[1] not in DATATYPE_DICT:
        raise ValueError("test_input's input[1] should be a datatype from globalconstants.py")
    if not isinstance(input[2], str):
        raise ValueError("test_input's input[2] should be of type str")
    if not isinstance(input[3], str):
        raise ValueError("test_input's input[3] should be of type str")

    # output if error
    error_text = str(input[3]) + "'s " + str(input[2]) + " should be type "
    error_text += str(input[1])

    if not check_input_match(input[0], input[1]):
        raise TypeError(error_text)


#TEST_INPUTS()
#test_inputs(list_of_inputs) tests a list of inputs of form (variable, datatype,
# variable_name, function_name). see test_input() for basic case.
def test_inputs(list_of_inputs):
    test_input((list_of_inputs,LIST,"list_of_inputs","test_inputs"))
    for input in list_of_inputs:
        test_input(input)
