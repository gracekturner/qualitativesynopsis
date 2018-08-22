import pandas
from codenames_cleaner import *
from textgroups import *

# start adds a status column/row to the dataset. It also modifies data columns to be {raw: data}
# to allow further updates later on
def start(data):
    # testing inputs for accuracy
    list_of_inputs = [(data, PANDAS, "data", "cleaner.start")]
    test_inputs(list_of_inputs)
    for each in data.index:
        list_of_inputs.append((each, STR, "data.index", "cleaner.start"))
    for each in data.columns:
        list_of_inputs.append((each, STR, "data.columns", "cleaner.start"))
    test_inputs(list_of_inputs)
    if len(data.columns) == 0:
        raise TypeError("This empty dataset has nothing for cleaner.start to clean...")
    # new df
    df = pandas.DataFrame({})

    # create a status data point for each column
    status_row = {}
    stat = value_to_dictionary(HIDDEN, [RAW])
    status = {STATUS: stat}
    status[STATUS][RAW] = VISIBLE

    # update x->{raw:x} for each data point
    for each in data.columns:
        #for each column, apply something that changes x-> {raw:x}
        df[each] = data[each].apply(value_to_dictionary, args = ([RAW],))
        # create a row that shows status displays
        status_row[each] = status

    # set up row/column status
    df = df.append(pandas.DataFrame(status_row))
    df[STATUS] = VISIBLE


    return df

def check_basic_inputs(data, stop = False):
    test_inputs([(data, PANDAS, "data", "cleaner.check_basic_inputs")])
    # NOTE there is a situation where a user hasn't run it and accidentally
    #has STATUS in both columns and indexes...
    if STATUS not in data.columns:
        raise TypeError("data must have a status column (have you run cleaner.start()?)")
    if STATUS not in data.index:
        raise TypeError("data must have a status row (have you run cleaner.start()?)")
    if stop:
        for each in data.columns:
            if each == STATUS:
                continue
            res = data.loc[STATUS, each]
            for r in res:
                if res[r] not in POSSIBLE_STATUS:
                    raise TypeError("a status column value is invalid for cleaner.stop")

        for each in data.index:
            res = data.loc[each, STATUS]
            if res not in POSSIBLE_STATUS:
                raise TypeError("a status row value is invalid for cleaner.stop")
# stop removes status column/row from the dataset,
# and applies any other changes based on the values in the status row/col
def stop(data):
    test_inputs([(data, PANDAS, "data", "cleaner.stop")])

    check_basic_inputs(data, True)

    df = pandas.DataFrame({})


    for each in data.columns:
        if each == STATUS:
            continue


        ## for each in the possible keys
        for m in POSSIBLE_MODIFIERS:
            ##get that key
            status = data.loc[STATUS, each]
            if m not in status:
                continue

            series = data[each].apply(dictionary_to_value, args = (m,))
            ##if it is visible, add it to the new dataset as columname_key


            if status[m] == VISIBLE:
                df[each+"_"+str(m)] = series

    # if no more columns,
    if len(df.columns) == 0:
        return df
    # drop invisible rows

    df.index = data.index
    for each in data.index:
        if data.loc[each, STATUS] == HIDDEN:
            df = df.drop([each])

    # drop status row
    df = df.drop([STATUS])


    return pandas.DataFrame(df.to_dict())

def exists_col(data, col):
    if col not in data.columns:
        raise TypeError("there is not a col by that name")



def modify_status(df, what, axis, setting, sub_column = RAW):

    check_basic_inputs(df)
    if ROW != axis and COL != axis:
        raise TypeError("data must have an appropriate ROW/COL signifier")
    if setting not in POSSIBLE_STATUS:
        raise TypeError("data must have appropriate modifier")
    if axis == ROW:
        if what not in df.index:
            raise TypeError("there is not a row by that name")
        df.loc[what, STATUS] = setting
    if axis == COL:
        exists_col(df, what)
        if sub_column not in df.loc[STATUS, what]:
            raise TypeError("there is no sub_column by that name")
        res = df.xs(STATUS)[what].copy()
        res[sub_column] = setting
        df.at[STATUS, what] =  res

    return df

def hide(data, what, axis, sub_column = RAW):
    return modify_multiple_status(data, what, axis, HIDDEN, sub_column)


def show(data, what, axis, sub_column = RAW):
    return modify_multiple_status(data, what, axis, VISIBLE, sub_column)

def modify_multiple_status(data, what, axis, setting, sub_column = RAW):
    data = data.copy()
    if isinstance(what, str):
        return modify_status(data, what, axis, setting, sub_column)
    test_inputs([(what, LIST, "what", "modify_multiple_status")])

    for each in what:
        modify_status(data, each, axis, setting, sub_column)

    return data
# scrub removes punctuation, capitalizations
def scrub_column(data, col):
    df = data.copy()
    check_basic_inputs(data)
    exists_col(data, col)

    for i, row in df.iterrows():
        res = row[col][RAW].lower()
        res = remove(res, PUNCTUATION_LIST)
        r = row[col].copy()
        r[SCRUB] = res
        df.at[i, col] = r

    return df

# finds family on features across datapoints in col
def family_finder(data, col):
    df = data.copy()
    check_basic_inputs(data)
    exists_col(data, col)
    if FEATURE not in data.at[data.index[0],col]:
        df = feature_finder(data, col)
    #NOTE  reorganize using apply function (somehow skipping status col?)
    for i, row in df.iterrows():
        if i == STATUS:
            df.loc[i, col][FAMILY] = VISIBLE
            continue
        df.at[i, col] = find_family(row[col], 5)
        #NOTE do something here to build topic finder res
    return df

# finds features for each data point in col
def feature_finder(data, col):
    df = data.copy()

    check_basic_inputs(data)
    exists_col(data, col)
    if SCRUB not in data.at[data.index[0],col]:
        df = scrub_column(data, col)

    # new_col
    new_col = {}

    # for each pairs
    for i in range(len(df.index)-1):
        index = list(df.index)

        if i not in new_col:
            new_col[i] = set([])
        for j in range(i+1, len(index)):
            if index[j] == STATUS:
                continue
            if j > len(index):
                break
            if j not in new_col:
                new_col[j] = set([])


            # get features (if any) from pairs
            text1 = df.at[index[i], col][SCRUB]
            text2 = df.at[index[j], col][SCRUB]

            add = find_features(text1, text2, 5)

            # add features to appropriate cell
            new_col[i] = new_col[i].union(add)
            new_col[j] = new_col[j].union(add)
        df.at[index[i], col][FEATURE] = new_col[i]

        #return results

    return df
def feature_to_topic(data, col, feature, topic):
    check_basic_inputs(data)
    exists_col(data, col)
    test_inputs([(topic, STR, "topic", "feature_to_topic"),(feature, DICT, "feature", "feature_to_topic")])
    status = data.loc[STATUS, col]
    df = data.copy()
    if TOPIC not in status:
        df = make_topic(data, col, topic)
        status = df.loc[STATUS, col]
    if topic not in status[TOPIC]:
        df = make_topic(data,col,topic)
        status = df.loc[STATUS, col]
    status[TOPIC][topic] =  {**status[TOPIC][topic], **feature}
    df.at[STATUS, col] = status

    return data

def make_topic(data, col, topic):
    check_basic_inputs(data)
    exists_col(data, col)
    test_inputs([(topic, STR, "topic", "make_topic")])
    df=  data.copy()
    status = df.loc[STATUS, col]
    if TOPIC not in status:
        status[TOPIC] = {}
    status[TOPIC][topic] = {}
    df.at[STATUS, col] = status
    return df

def build_complete_family(data, col):

    check_basic_inputs(data)
    exists_col(data, col)
    comp = {}
    if COMPLETE in data.loc[STATUS, col]:
        return data
    df = data.copy()
    for i, row in data.iterrows():
        if i == STATUS:
            continue
        fam = row[col][FAMILY]
        for each in fam:

            if fam[each][ROOT] == each:

                if each not in comp:
                    comp[each] = {CHILDREN: {}, IDS: set()}
                comp[each][IDS].add(i)
                for e in fam[each][CHILDREN]:
                    if e not in comp[each][CHILDREN]:
                        comp[each][CHILDREN][e] = {CHILDREN: set([]), IDS: set()}
                    comp[each][CHILDREN][e][IDS].add(i)
                    comp[each][CHILDREN][e][CHILDREN] = comp[each][CHILDREN][e][CHILDREN].union(fam[e][CHILDREN])

    res = df.loc[STATUS, col]
    res[COMPLETE] = comp
    df.at[STATUS, col] = res
    return df

def topic_finder(data, col):
    check_basic_inputs(data)
    exists_col(data, col)
    df = data.copy()
    if FAMILY not in data.loc[STATUS, col]:
        df = family_finder(data, col)
    df = build_complete_family(data, col)
    status = df.loc[STATUS, col]
    # merge any last roots
    roots = status[COMPLETE].keys()
        #for each pair, check if one is the root of the other, and if so:
        for i in range(len(roots)):
            for j in range(i, len(roots)):
                # add the younger family to the older one
                if roots[i] in roots[j]:
                    status[COMPLETE][roots[i]] = {**status[COMPLETE][roots[i]], **status[COMPLETE][roots[j]]}
                if roots[j] in roots[i]:
                    status[COMPLETE][roots[j]] = {**status[COMPLETE][roots[i]], **status[COMPLETE][roots[j]]}
                # remove the younger family
                #BUG do remove (Delete?) here
    for each in status[COMPLETE]:
        df =  feature_to_topic(data, col, {each: status[COMPLETE][each]}, each)

    for each in status[TOPIC]:
        print(each)
        print(status[TOPIC][each])
        print("...")
    return df
