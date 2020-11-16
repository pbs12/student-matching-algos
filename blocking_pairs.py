comp_prefs = {
    'apple': [1,2,3,4,5,6,7,8], 
    'ibm': [4,5,6,2,7]
} 
app_prefs ={
    1:['apple','ibm'],
    2:['apple','ibm'],
    3:['ibm','apple'],
    4:['apple','ibm'],
    5:['ibm','apple'],
    6:['ibm','apple'],
    7:['apple','ibm']
}
pairs= [['apple', 1],['apple', 3],['apple', 4],['ibm', 2],['apple', 6],['apple', 5]]
pair_dict =[{
    'comp': 'apple',
    'app': 15,
    'app_pref_index': 13,
    'comp_app_pref_index': 15
}]
comp_prefs_indexed = {}
app_prefs_indexed = {}

def create_indexes():
    for comp in comp_prefs:
        index = 0
        comp_prefs_indexed[comp] = {}
        for app in comp_prefs[comp]:
            comp_prefs_indexed[comp][app] = index
            index+=1
    for app in app_prefs:
        index = 0
        app_prefs_indexed[app] = {}
        for comp in app_prefs[app]:
            app_prefs_indexed[app][comp] = index
            index+=1
create_indexes()           
        

def blocking_pairs(pairings, prefs_app, prefs_comp):
    test_arr = ['nun']
    for pair in pairings:
        comp = pair[0]
        app = pair[1]
        for other_pair in pairings:
            other_comp = other_pair[0]
            other_app = other_pair[1]
            if app not in comp_prefs_indexed[other_comp].keys():
                continue
            if other_comp not in app_prefs_indexed[app].keys():
                continue
            if app_prefs_indexed[app][comp] > app_prefs_indexed[app][other_comp] and comp_prefs_indexed[other_comp][app] > comp_prefs_indexed[other_comp][other_app]:
                test_arr.append(["blocking pair", app, comp," and ",other_app, other_comp])
    print(len(test_arr))
    return test_arr

blocking_pairs(pairs, app_prefs, comp_prefs)
