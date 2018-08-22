#globalconstants - lists all constants that show up repeatedly in one file.
#DEPENDENCIES: pandas (external)
import pandas

# Punctuation List: English version
PUNCTUATION_LIST = [",", "!", "-", '.', "?", ":", "'", '"', '(', ')']
#Punctuation and Stop Words: English version.
#Does not remove words that appear at the beginning of the text
PUNCTUATION_LIST_AND_STOP_WORDS = [",", "!", "-", '.', "?", ":", "'", '"', '(', ')',
" is ", " and ", " or ", " was ", " by ", " this ", " the ", " are ",
 " but "," on "," that ", " those ", " to ", " our ", " a " " this ",
  " these ", " with "]

#common datatypes
STR = "str"
DICT = "dict"
INT = "int"
LIST = "list"
PANDAS = "pandas"
EXCEL = "excel"

#DATATYPE_DICT: a dict that turns global constants (see above) to types
DATATYPE_DICT = {}
DATATYPE_DICT[STR] = str
DATATYPE_DICT[INT] = int
DATATYPE_DICT[PANDAS] = pandas.DataFrame
DATATYPE_DICT[DICT] = dict

ERROR = "error"
RESULTS = "results"

#stuff for models.DATA
DATA_NAME = "data_name"
RAW = "raw"
TOPIC = "topic"
FEATURE = "feature"
FALSEPOS = "falsepos"
FEAT = "feat"
FALSE_FEATURE = "falsefeature"
PERM_FEATURE = "permfeature"
