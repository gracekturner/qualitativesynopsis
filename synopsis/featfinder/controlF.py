from . import models
from globalconstants import *
from django.utils.crypto import get_random_string
import pandas
from datetime import datetime
import sys
sys.path.append('../')
from textfunctions.feature_finder import  scrub
##controlF is the current algorithm ("control F on steroids")
##it contains anything that pulls to and from models.Data, as well
##as the topic assignment algorithms etc.
##it uses data like this:
##DATA[RAW] = array of the raw data
##DATA[DATANAME] = the name of the column
##DATA[TOPIC] = a dictionary of a pandas dataframe with: (topic, id, feature)
##DATA[FEATURE] = a dictionary of a pandas dataframe with: (topic, feature)


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

#update workspace using function_name, args
#name is the function name (which tells which processing function to use)
#args is any args + the id of the workspace (to pull the correct data)
def run_function(function_name, args):
    #testing the type of the input arguments
#    test_inputs([(function_name, STR, "function_name", "run_function"),
#    (args, DICT, "function_name", "run_function")
#    ])


    function_pos = {}
    function_pos["AddTopic"] = assign_topic
    function_pos["MakeWorkspace"] = make_workspace
    function_pos["AddFeature"] = assign_topic
    function_pos["DeleteTopic"] = delete_topic
    function_pos["DeleteFeatureTopic"] = delete_feature_topic
    function_pos["CustomerFeedback"] = customer_feedback


    #check that function_name exists
    if function_name not in function_pos:
        raise TypeError("function_name %s does not exist for run_function", function_name)

    #run function.
    res =  function_pos[function_name](args)

    #make sure the output is a dict
    #test_input((res, DICT, "output", "run_function"))

    #double check that it returned both ERROR and RESULTS
    for each in [ERROR, RESULTS]:
        if each not in res:
            raise TypeError("%s did not return %s", function_name, each)

    return res

#check args double checks that the args were sent correctly
#and then pulls the data attached to args's id
def check_args(args, ls, return_data = True):
    #check that args are correct
    for each in ls:
        if each not in args:
            raise TypeError("missing %s in models.delete_text_topic", each)

    if not return_data:
        return

    #return data (if asked)
    key = args["id"]
    dobj = models.Data.objects.get(url_key=key)
    data = eval(dobj.data)
    #data = make_complete_data(data)

    return dobj, data
#save data saves the data.
def save_data(dobj, data):
    dobj.data = repr(data)
    dobj.save()

#builds a control-F workspace (one that only has user generated features)
def make_workspace(args):
    #get the uploaded (or arbitrary) data
    check_args(args, ["data"], False)
    ret = pandas.Series(args["data"])

    #generate a random key
    key = get_random_string(length = 32)

    #NOTE need to do something here to prevent multiple matching keys
    #create a data object with that key and ret (a pandas.Series)
    dobj = models.Data(url_key = key)

    #making the data part using ret
    data = {}
    data[DATA_NAME] = ret.name
    #raw data
    data[RAW] = list(ret.values)
    #these are the topics
    data[FEATURE] = {"topic": [], "feature": []}
    data[TOPIC] = {"id": range(len(data[RAW]))}
    data[TOPIC]["topic"] = ""
    data[TOPIC]["feature"] = ""
    dobj.data = repr(data)
    dobj.save()

    return {ERROR: None, RESULTS: dobj}

#assign topic adds the topic:feature to the list of them
#and then runs through the raw data and assigns the topic
#based on the feature
def assign_topic(args):
    dobj, data = check_args(args, ["topic"])
    #feature
    if  "feature" not in args:
        args["feature"] = ""
    topic = pandas.DataFrame(data[TOPIC])
    feature = pandas.DataFrame(data[FEATURE])
    feature = feature.append({"topic":args["topic"], "feature": args["feature"]},ignore_index = True)
    #if it only created a topic
    if args["feature"] == "":
        data[TOPIC] = topic.to_dict()
        data[FEATURE] = feature.to_dict()
        save_data(dobj, data)

        return {ERROR: None, RESULTS: None}
    #applying feature
    for i in range(len(data[RAW])):

        if args["feature"] in scrub(data[RAW][i]):
            topic = topic.append({"topic": args["topic"], "id": i, "feature": args["feature"]}, ignore_index = True)

    data[TOPIC] = topic.to_dict()
    data[FEATURE] = feature.to_dict()
    save_data(dobj, data)

    return {ERROR: None, RESULTS: None}

def delete_topic(args):
    dobj, data = check_args(args, ["topic"])
    topic = pandas.DataFrame(data[TOPIC])
    feature = pandas.DataFrame(data[FEATURE])
    topic = topic[topic["topic"] != args["topic"]]
    feature = feature[feature["topic"] != args["topic"]]
    data[TOPIC] = topic.to_dict()
    data[FEATURE] = feature.to_dict()
    save_data(dobj, data)

    return {ERROR: None, RESULTS: None}

def delete_feature_topic(args):
    dobj, data = check_args(args, ["topic"])
    topic = pandas.DataFrame(data[TOPIC])
    feature = pandas.DataFrame(data[FEATURE])
    topic = topic[~(topic["feature"] == args["feature"]) | ~(topic["topic"] == args["topic"])]
    feature = feature[~(feature["feature"] == args["feature"]) | ~(feature["topic"] == args["topic"])]
    data[TOPIC] = topic.to_dict()
    data[FEATURE] = feature.to_dict()
    save_data(dobj, data)

    return {ERROR: None, RESULTS: None}

def customer_feedback(args):
    check_args(args, ["text"],False)
    text = args["text"]
    try:
        dobj = models.Data.objects.get(url_key="CUSTOMERFEEDBACK")
    except:
        dobj = models.Data(url_key = "CUSTOMERFEEDBACK")
        data = {}
        data[DATA_NAME] = "Customer Feedback"
        #raw data
        data[RAW] = list([])
        #these are the topics
        data[FEATURE] = {"topic": [], "feature": []}
        data[TOPIC] = {"id": range(len([]))}
        data[TOPIC]["topic"] = ""
        data[TOPIC]["feature"] = ""
        dobj.data = repr(data)



    data = eval(dobj.data)
    data[RAW].append(text)
    topic = pandas.DataFrame(data[TOPIC])
    topic = topic.append({"id": len(data[RAW])-1, "topic": "", "feature": ""},ignore_index = True)
    data[TOPIC] = topic.to_dict()
    save_data(dobj, data)
    return {ERROR: None, RESULTS: "Thanks so much for your feedback!"}

#pull_workspace builds the html version
def pull_workspace(data,err):
    rendr = {}
    rendr["error_message"] = err

    rendr["data_name"] = data["data_name"]

    rendr["results"] = build_results(data)

    rendr["topic_overview"] = build_topic_overview(data)

    return rendr

#build_results builds the results...(applys some groupby)
def build_results(data):
    topic = pandas.DataFrame(data[TOPIC])
    df = {}
    topic = topic.drop_duplicates(topic.columns.difference(['feature']))
    top = topic.groupby("id")['topic'].apply(list).reset_index()
    top["data"] = pandas.Series(data[RAW], index=top.index)
    return top.to_dict('records')

#build_topic_overview builds the topic overview (gets the frequencies, etc.)
def build_topic_overview(data):
    topic = pandas.DataFrame(data[TOPIC])
    feature = pandas.DataFrame(data[FEATURE])
    topic = topic.drop_duplicates(topic.columns.difference(['feature']))

    top = topic.groupby("topic").size().reset_index(name = "frequency")
    feat = feature.groupby("topic")["feature"].apply(list).reset_index()

    res = pandas.merge(top, feat, on='topic', how='outer')

    res = res.fillna("")
    res = res[res["topic"] != ""]

    return res.to_dict('records')
