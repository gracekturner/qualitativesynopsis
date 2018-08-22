import sys
sys.path.append('../')
from globalconstants import *
from input_tester.input_testing import *
import pandas

# return_error(function_name, args) sends the arguments along to
#run_function() and returns res[ERROR]
def return_error(function_name, args):
    res = run_function(function_name,args)
    return res[ERROR]

#return_results(function_name, args) sends the arguments along to
# run_function and returns res[RESULTS]
def return_results(function_name, args):
    res = run_function(function_name,args)
    return res[RESULTS]

#runs the function function_name with args. Assumes that it gives me a
#function_name and args and its only used
def run_function(function_name, args):

    #testing the type of the input arguments
    test_inputs([(function_name, STR, "function_name", "run_function"),
    (args, DICT, "function_name", "run_function")
    ])

    #the function_name switchboard
    function_pos = {}
    function_pos["UploadData"] = upload_data_excel
    function_pos["AssignTopic"] = assign_topic
    #function_pos["DeleteTextTopic"] = no_form_check
    #function_pos["DeleteTextTopicMachine"] = no_form_check
    function_pos["DownloadData"] = no_form_check
    function_pos["AddTopic"] = add_topic
    function_pos["DeleteTopic"] = no_form_check
    function_pos["AddFeature"] = add_feature
    function_pos["DeleteFeatureTopic"] = no_form_check
    function_pos["CustomerFeedback"] = customer_feedback
    #check that function_name exists
    if function_name not in function_pos:
        raise TypeError("function_name %s does not exist for run_function", function_name)

    #run function.
    res =  function_pos[function_name](args)

    #make sure the output is a dict
    test_input((res, DICT, "output", "run_function"))

    #double check that it returned both ERROR and RESULTS
    for each in [ERROR, RESULTS]:
        if each not in res:
            raise TypeError("%s did not return %s", function_name, each)

    return res

#upload_data_excel(args) checks a dataset and returns error messages if the data
#wasn't uploaded correctly
def upload_data_excel(args):
    #checks that args contains all the appropriate arguments
    list = ["file", "sheet", "col"]
    for each in list:
        if each not in args:
            raise TypeError("upload_data_excel's args does not contain %s", each)
    file = args["file"]
    sheet = args["sheet"]
    col = args["col"]
    print(file, type(file), sheet, type(sheet))
    #check that the file is excel
    if not check_input_match(file, EXCEL):
        return {ERROR:"error: you did not upload an .xlsx file.",RESULTS: None}
    #check that the sheetname exists
    try:
        df = pandas.read_excel(file,sheet)
    except:
        return {ERROR:"error: the sheet you named does not exist.", RESULTS:None}

    #check that the column exists
    if col not in df.columns:
        return {ERROR:"error: this column does not exist.", RESULTS: None}

    #returns successful result (if it reaches here)
    return {ERROR: None, RESULTS: {"data":df[col]}}

def assign_topic(args):
    topic = args["topic"]
    text = args["text"]
    textid = args["textid"]

    #check that topic isn't null (if so return error)
    if str(topic).strip() == "":

        return {ERROR: "You did not create a valid topic (topic cannot be blank or white space).",
        RESULTS: None}
    #check that text exists (not just whitespace)
    if str(text).strip() == "":
        return {ERROR: "You did not highlight a valid phrase (phrase cannot be blank or white space).",
        RESULTS: None}


    return {ERROR: None, RESULTS: args}

def add_topic(args):
    topic = args["topic"]
    if str(topic).strip() == "":
        return {ERROR: "You did not create a valid topic (topic cannot be blank or white space).",
        RESULTS: None}
    return {ERROR: None, RESULTS: args}

def add_feature(args):
    feature = args["feature"]
    if str(feature).strip() == "":
        return {ERROR: "You did not create a valid feature (feature cannot be blank or white space).",
        RESULTS: None}
    return {ERROR: None, RESULTS: args}


def customer_feedback(args):
    text = args["text"]
    if str(text).strip() == "":
        return {ERROR: "How do we improve with blank feedback? Try that again please.",
        RESULTS: None}
    return {ERROR: None, RESULTS: args}

def no_form_check(args):
    #as far as I can tell, there isn't any user error issues here.
    #Like, its a delete button.
    return {ERROR: None, RESULTS: args}
