from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, reverse
import featfinder.forms as forms
import sys
sys.path.append('../')
import openpyxl
from globalconstants import *
import pandas
from . import models
from datetime import datetime
from . import controlF



#whichform decides which form it is and returns the function name and relevant args
def whichform(request, id = ""):
    formdf = {}
    #formdf["DownloadData"] = []
    formdf["AssignTopic"] = [("AssignTopic_Text", "req", "text"), ("AssignTopic_TextID", "req", "textid"),
     ("AssignTopic_Topic", "req", "topic")]
    formdf["UploadData"] = [('UploadData_Column_Name', "req", "col"),("UploadData_Sheet_Name", "req", "sheet"),
    ("UploadData_File", "file", "file")]
    formdf["CustomerFeedback"] = [('CustomerFeedback_Text', "req", "text")]
    #formdf["DeleteTextTopic"] = [("DeleteTextTopic_Topic", "req", "topic"), ("DeleteTextTopic_TextID", "req", "textid")]
    #formdf["DeleteTextTopicMachine"] = [("DeleteTextTopicMachine_Topic", "req", "topic"),
    #("DeleteTextTopicMachine_TextID", "req", "textid")]
    formdf["AddTopic"] = [("AddTopic_Topic", "req", "topic")]
    formdf["DeleteTopic"] = [("DeleteTopic_Topic", "req", "topic")]
    formdf["AddFeature"] = [("AddFeature_Topic", "req", "topic"),("AddFeature_Feature", "req", "feature")]
    formdf["DeleteFeatureTopic"] = [("DeleteFeatureTopic_Topic", "req", "topic"),("DeleteFeatureTopic_Feature", "req", "feature")]
    name = request.POST.get('FormName')

    if name not in formdf:
        raise TypeError("This form name %s does not exist in views.whichform", name)

    ls = formdf[name]
    args = {}
    args["id"] = id
    for each in ls:
        if each[1] == "req":
            args[each[2]] = request.POST.get(each[0])
        if each[1] == "file":

            args[each[2]] = []

            if each[0] in request.FILES:
                args[each[2]] = request.FILES[each[0]]

    return name, args


# index is the view that handles the homepage ("home.html") including the
#different use paths of uploading a dataset (e.g. the different ways to upload
#it wrong, when it is uploaded correctly, etc.)
def index(request):
    #error and returning (if there is an error, ret is None, and vice versa)
    err = None
    ret = None
    if request.method == 'POST':
        #process the form
        name, args = whichform(request)

        err = forms.return_error( name, args)
        args = forms.return_results(name, args)
        # if there are no errors in the form
        if err == None:
            if name == "CustomerFeedback":
                err = controlF.run_function(name, args)[RESULTS]

            if name == "UploadData":

                #create workspace
                dobj = controlF.return_results("MakeWorkspace", args)
                #redirect to workspace key
                return redirect('controlF_view', id = dobj.url_key)

    #regardless if the method is GET or POST, return err as error_message
    #the default for err is None afterall
    args = {"error_message": err}
    return render(request, 'featfinder/index.html', args)



#controlF(request, id) is a view function that returns the appropriate dataset
#for analysis by the user (using id - a randomly generated 32 part key). Is connected
# to featfinder/workspace.html. Only controlF features
def controlF_view(request, id):
    #get the appropriate dataobject and convert dobj.data into a usable dictionary
    err = None

    #rendr = pull_workspace(data, err)
    #do stuff when a form is submitted
    if request.method == "POST":
        #THINKING ABOUT THIS:
        #assigntopic, deleteinstanceoftopic, probably deletetopic in general
        #figure out which form it is
        name, args = whichform(request, id)


        #get processed results based on form type
        err = forms.return_error(name, args)
        ret = forms.return_results(name, args)

        #do something with them based on form type
        if err == None:
            res = controlF.run_function(name, ret)
            if name == "DownloadData":
                return res[RESULTS]
            if name == "CustomerFeedback":
                err = res[RESULTS]


    #get the new dataframe
    dobj = models.Data.objects.get(url_key=id)
    data = eval(dobj.data)


    #pull the results (recalculate features, apply features,
    #convert into something that is html friendly)
    rendr = controlF.pull_workspace(data, err)




    return render(request, 'featfinder/controlF.html', rendr)
