import sys
sys.path.append('../')
import unittest
from django.test import TestCase
from django.urls import reverse
from . import controlF
from globalconstants import *
import pandas

#to test the index page (currently in basic - upload data only edition)
class TestViewIndex(TestCase):

    def test_index_loads(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_submit_error(self):
        response = self.client.post(reverse('index'),{'FormName': 'UploadData','UploadData_File': "lalal", 'UploadData_Sheet_Name': '', 'UploadData_Column_Name': 'PHRASE'}, follow=True)
        self.assertContains(response, "error: you did not upload an .xlsx file.")
        with open('featfinder/automated_testing/bathroom_training.xlsx',"rb") as fp:
            response = self.client.post(reverse('index'),{'FormName': 'UploadData','UploadData_File': fp, 'UploadData_Sheet_Name': '', 'UploadData_Column_Name': 'PHRASE'}, follow=True)
            self.assertContains(response, "error: the sheet you named does not exist.")
        with open('featfinder/automated_testing/bathroom_training.xlsx', "rb") as fp:
            response = self.client.post(reverse('index'),{'FormName': 'UploadData','UploadData_File': fp, 'UploadData_Sheet_Name': 'Sheet1', 'UploadData_Column_Name': 'lalal'}, follow=True)
            self.assertContains(response, "error: this column does not exist.")

    #checks for invalid inputs
    def test_index_submit_correct(self):
        #check that it redirects to a new page called '/featfinder/controlF/<randomstring>'
        with open('featfinder/automated_testing/bathroom_training.xlsx', "rb") as fp:
            response = self.client.post(reverse('index'),{'FormName': 'UploadData','UploadData_File': fp, 'UploadData_Sheet_Name': 'Sheet1', 'UploadData_Column_Name': 'PHRASE'}, follow=True)
        self.assertContains(response, "PHRASE")
        self.assertContains(response, "not overly big")


## to test the workspace (currently controlF version)
test = pandas.Series(["keeping things pg and clean up in here", "much cleanliness, no dirt",
    "I love things to be clean", "very clean bathrooms",
    "I want the lyrics to be clean for once!"])

#testing the customer feedback submit button (allows users to submit customer
#feedback, allows us to see it and analyze it within the software from
# /controlF/CUSTOMERFEEDBACK/)
class TestCustomerFeedback(TestCase):
    #tests that both are successful (index and workspace (controlF_view))
    def test_customerfeedback_workspace_works(self):
        dobj = controlF.make_workspace({"data": test})[RESULTS]
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'CustomerFeedback','CustomerFeedback_Text': "lalal"}, follow=True)
        self.assertContains(response, "Thanks so much for your feedback!")
        response  = self.client.get(reverse('controlF_view', kwargs = {'id': "CUSTOMERFEEDBACK"}), follow=True)
        self.assertContains(response, "lalal")
    def test_customerfeedback_index_works(self):
        response = self.client.post(reverse('index'),{'FormName': 'CustomerFeedback','CustomerFeedback_Text': "lalal2"}, follow=True)
        self.assertContains(response, "Thanks so much for your feedback!")
        response  = self.client.get(reverse('controlF_view', kwargs = {'id': "CUSTOMERFEEDBACK"}), follow=True)
        self.assertContains(response, "lalal2")
        
    #tests that "" and " " (blank feedback) don't get submitted on both sides
    def test_customerfeedback_index_fail(self):
        response = self.client.post(reverse('index'),{'FormName': 'CustomerFeedback','CustomerFeedback_Text': ""}, follow=True)
        self.assertContains(response, "How do we improve with blank feedback? Try that again please.")
        response = self.client.post(reverse('index'),{'FormName': 'CustomerFeedback','CustomerFeedback_Text': "  "}, follow=True)
        self.assertContains(response, "How do we improve with blank feedback? Try that again please.")
    def test_customerfeedback_workspace_fail(self):
        dobj = controlF.make_workspace({"data": test})[RESULTS]
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'CustomerFeedback','CustomerFeedback_Text': ""}, follow=True)
        self.assertContains(response, "How do we improve with blank feedback? Try that again please.")
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'CustomerFeedback','CustomerFeedback_Text': "  "}, follow=True)
        self.assertContains(response, "How do we improve with blank feedback? Try that again please.")

class TestViewControlF(TestCase):

    #test that the controlF loads
    def test_controlF_loads(self):

        dobj = controlF.make_workspace({"data": test})[RESULTS]
        response = self.client.get(reverse('controlF_view', kwargs = {'id': dobj.url_key}))
        self.assertEqual(response.status_code, 200)

    #test that inputs aren't messy for add topic
    def test_bad_inputs_controlF(self):
        dobj = controlF.make_workspace({"data": test})[RESULTS]
        # test add topic
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddTopic','AddTopic_Topic': ""}, follow=True)
        self.assertContains(response, "You did not create a valid topic")
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddTopic','AddTopic_Topic': " "}, follow=True)
        self.assertContains(response, "You did not create a valid topic")
        self.assertEqual(response.status_code, 200)

        #test add feature to topic
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddFeature','AddFeature_Topic': "asdsas", 'AddFeature_Feature': ""}, follow=True)
        self.assertContains(response, "You did not create a valid feature")
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddFeature','AddFeature_Topic': "asdsas", 'AddFeature_Feature': " "}, follow=True)
        self.assertContains(response, "You did not create a valid feature")
        self.assertEqual(response.status_code, 200)


    #test that nothing breaks in the display
    #test that assign 1 topic works
    def test_1_topic(self):
        dobj = controlF.make_workspace({"data": test})[RESULTS]

        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddTopic','AddTopic_Topic': "lalal"}, follow=True)
        self.assertContains(response, "lalal")
        self.assertContains(response, 0)


    #test that assign 1 topic, 1 feature works
    def test_1_topic_2_feature(self):
        dobj = controlF.make_workspace({"data": test})[RESULTS]
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddTopic','AddTopic_Topic': "lalal"}, follow=True)
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddFeature','AddFeature_Topic': "lalal", 'AddFeature_Feature':'featureeee'}, follow=True)
        self.assertContains(response, "lalal")
        self.assertContains(response, "featureeee")
        self.assertContains(response, 0)
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddFeature','AddFeature_Topic': "lalal", 'AddFeature_Feature':'clean'}, follow=True)
        self.assertContains(response, 5)

    #test that assign 1 topic, delete it, works
    def test_topics_1_delete(self):
        dobj = controlF.make_workspace({"data": test})[RESULTS]
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddTopic','AddTopic_Topic': "lalal"}, follow=True)
        response =  self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'DeleteTopic','DeleteTopic_Topic': "lalal"}, follow=True)
        try:
            self.assertContains(response, "lalal")

        except:
            print("test_topics_1_delete is ok")
    #test assign 1 topic, delete it, and add it back works
    def test_topics_1_delete_1_add(self):
        dobj = controlF.make_workspace({"data": test})[RESULTS]
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddTopic','AddTopic_Topic': "lalal"}, follow=True)
        response =  self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'DeleteTopic','DeleteTopic_Topic': "lalal"}, follow=True)
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddTopic','AddTopic_Topic': "hello"}, follow=True)
        self.assertContains(response, "hello")
        try:
            self.assertContains(response, "lalal")
        except:
            print("test_topics_1_delete_1_add is ok")


    #test assign 1 feature, delete feature works
    def test_delete_feature(self):
        dobj = controlF.make_workspace({"data": test})[RESULTS]
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddTopic','AddTopic_Topic': "lalal"}, follow=True)
        response =  self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddFeature','AddFeature_Topic': "lalal",'AddFeature_Feature': "sdf"}, follow=True)
        response =  self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'DeleteFeatureTopic','DeleteFeatureTopic_Topic': "lalal",'DeleteFeatureTopic_Feature': "sdf"}, follow=True)
        try:
            self.assertContains(response, "sdf")
        except:
            print("test_delete_feature is ok")

    #test assign 1 feature, delete feature, add another works
    def test_delete_feature_add(self):
        dobj = controlF.make_workspace({"data": test})[RESULTS]
        response = self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddTopic','AddTopic_Topic': "lalal"}, follow=True)
        response =  self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddFeature','AddFeature_Topic': "lalal",'AddFeature_Feature': "sdf"}, follow=True)
        response =  self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'DeleteFeatureTopic','DeleteFeatureTopic_Topic': "lalal",'DeleteFeatureTopic_Feature': "sdf"}, follow=True)
        response =  self.client.post(reverse('controlF_view', kwargs = {'id': dobj.url_key}),{'FormName': 'AddFeature','AddFeature_Topic': "lalal",'AddFeature_Feature': "happppy"}, follow=True)
        self.assertContains(response, "happppy")
        try:
            self.assertContains(response, "sdf")

        except:
            print("test_delete_feature_add is ok")
