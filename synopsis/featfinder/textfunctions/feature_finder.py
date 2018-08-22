#feature_finder.py

#FEATURE_FINDER()
#feature finder works by taking 2 strings (text1, text2) and finding any overlap
#between the 2 of length >= N. It then returns a list of those overlaps ("features")
#while only showing unique features and removing any trailing whitespace from
#those features. This does mean it can find a feature that is less than size N,
#if the overlap had a lot of trailing whitespace. This is not a bug.

#DEPENDENCIES: textfunctions.remove(), globalconstants.PUNCTUATION_LIST,
#input_testing.test_inputs(). No outsider functions but sys.
import sys
sys.path.append('../')
from textfunctions.textfunctions import remove
from globalconstants import *
from input_tester.input_testing import test_inputs

def scrub(text, punc_list = PUNCTUATION_LIST_AND_STOP_WORDS):
    return remove(text.lower(), punc_list)



def feature_finder(text1, text2, N):
    #make sure the inputs are correct
    test_inputs([(text1, STR, "text1", "feature_finder"),
    (N, INT, "N", "feature_finder"), (text2, STR, "text2", "feature_finder")])

    # remove capitalizations, punctuation, and stop words on the approved list
    text1 = scrub(text1)
    text2 = scrub(text2)

    # list of features found
    features = []

    # indexes to skip after discovering a phrase (starting none)
    skip_indexes  = set()

    #for each index in the first text
    for x in range(len(text1)):

        # if it is impossible to find more features, break
        if x + N >= len(text1):
            break
        #if the index x has already been seen (because it was part of a
        #feature), skip
        if x in skip_indexes:
            continue

        #from the back, for each index in text1
        for y in range(len(text1), x, -1):

            # find the subphrase t, such that it is the phrase that is bookended
            # by the indexes x and y
            t = text1[x:y]

            # if t is not of length N or greater, break
            if len(t) < N:
                break

            # if t is found in text2, add all indexes belonging to t to
            # skip_indexes and append t to features (after stripping
            # it of unnecessary whitespace - whitespace adds noise to feature
            # generation but is useful to keep shorter words in play).
            if t in text2:
                for i in range(x,y):
                    skip_indexes.add(i)
                    features.append(t.strip())
                break

    #returns only the unique features found
    return list(set(features))

#Example:
#print(feature_finder("hello how are you!", "And how are you?", 5)) = ["how you"]
# because 'are' is a STOP word
