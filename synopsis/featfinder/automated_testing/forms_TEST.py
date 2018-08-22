from django.test import TestCase
import sys
sys.path.append('../')
from synopsis.featfinder.forms import *
import unittest
import pandas
# Create your tests here.
class TestReturnErrorResults(unittest.TestCase):
    #checks for invalid inputs
    def test_bad_input(self):
        bad_input = [(1, {}), ("hello", {}), ("DataUploadExcel", [])
        ]
        for each in bad_input:
            with self.assertRaises(TypeError):
                return_results_and_error(each[0], each[1])
            with self.assertRaises(TypeError):
                return_error(each[0], each[1])
            with self.assertRaises(TypeError):
                return_results(each[0], each[1])

    # check that good input doesn't start problems
    def test_good_input(self):
        good_input = [("DataUploadExcel", {"file": "", "col": "", "sheet": ""})]
        for each in good_input:
            return_results_and_error(each[0], each[1])
            return_results(each[0], each[1])
            return_error(each[0], each[1])

class TestDataUploadExcel(unittest.TestCase):
    #checks for invalid inputs
    def test_bad_input(self):
        bad_input = [{}, "str", {"file": "", "col": ""}]
        for each in bad_input:
            with self.assertRaises(TypeError):
                return_results("DataUploadExcel", each)
                #NOTE INSERT FUNCTION HERE

    # check if input matches output
    def test_bad_output(self):
        bad_outputs = [{"args": {"file": "string", "sheet": "Sheet1", "col": "PHRASE"},
         "error": "error: you did not upload an .xlsx file.", "results": None},
         {"args": {"file": "../synopsis/featfinder/automated_testing/bathroom_training.xlsx", "sheet": "asdas", "col": "PHRASE"},
          "error": "error: the sheet you named does not exist.", "results": None},
         {"args": {"file": "../synopsis/featfinder/automated_testing/bathroom_training.xlsx", "sheet": "Sheet1", "col": "asds"},
          "error": "error: this column does not exist.", "results": None},
         {"args": {"file": "../synopsis/featfinder/automated_testing/bathroom_training.xlsx", "sheet": "Sheet1", "col": "PHRASE"},
          "error": None, "results": pandas.read_excel("../synopsis/featfinder/automated_testing/bathroom_training.xlsx", "Sheet1")["PHRASE"]},
        ]
        for each in bad_outputs:
            ret = upload_data_excel(each["args"])
            self.assertEqual(ret[ERROR], each["error"])
            if not isinstance(ret[RESULTS], pandas.Series):
                self.assertEqual(ret[RESULTS], each["results"])
            else:
                self.assertEqual(True, ret[RESULTS].equals(each["results"]))
            #TEST FUNCTION HERE
