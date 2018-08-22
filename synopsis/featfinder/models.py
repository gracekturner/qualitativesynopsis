
import sys
sys.path.append('../')
from django.db import models
import pandas
from django.utils.crypto import get_random_string
from globalconstants import *
from input_tester.input_testing import *
from textfunctions.feature_finder import feature_finder, scrub
from . import views

from django.http import HttpResponse
try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO
#import StringIO
import xlsxwriter

#Data: a class that stores the url key (the id of the specific workspace) and
#data (a pandas.Dataframe -> Dict -> str(Dict))
class Data(models.Model):
    url_key = models.CharField(max_length=200)
    data = models.TextField()
