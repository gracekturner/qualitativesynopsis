#functionswitchboard.py has the master switchboard function, indirectly
#the list of valid mid-size functions for different aspects throughout the service
#e.g. updating different parts of models.Data, or processing forms, etc.
#copy over to whatever page you are creating a switchboard for :)

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
    
def run_function(function_name, args):
    #testing the type of the input arguments
    test_inputs([(function_name, STR, "function_name", "run_function"),
    (args, DICT, "function_name", "run_function")
    ])
    #NOTE MUST PUT IN FUNCTION POS HERE####
    function_pos = {}
    #NOTE NOTE NOTE##

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
