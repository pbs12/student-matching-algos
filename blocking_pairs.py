import ttc 

def list_pairings(pairing_master_list):
    agg = []
    for pairing in pairing_master_list:
        company = pairing
        for app in pairing_master_list[pairing]:
            temp = [company, app]
            agg.append(temp)
    return agg
#list_pairings = list_pairings(ttcRes)
#print(list_pairings)

def find_blocking_pairs(pairings, prefs_app, prefs_comp):
    count = 0
    test_arr = ['nun']
    count = 0
    count_shit_data = 0

   def find_blocking_pairs3(pairings, prefs_app, prefs_comp):
    count = 0
    test_arr = []
    count = 0
    count_shit_data = 0

    for pair in pairings:
        comp_prefs = prefs_comp[pair[0]]
        app_prefs = prefs_app[pair[1]]
        comp = pair[0]
        app = pair[1]
        print(count)
        count+=1
        for other_pair in pairings:
            other_comp = other_pair[0]
            other_app = other_pair[1]
            other_comp_prefs = prefs_comp[other_pair[0]]
            other_app_prefs = prefs_app[other_pair[1]]
            
            if other_comp not in app_prefs:
   #             print("used 1")
                continue 
            if app not in other_comp_prefs:
 #               print("used 2")
                continue
            if other_app not in other_comp_prefs:
                continue
            if other_pair[0] == pair[0] and other_pair[1] == pair[1]:
 #               print("used 4")
                continue 
            if app_prefs.index(comp) > app_prefs.index(other_comp) and other_comp_prefs.index(app) > other_comp_prefs.index(other_app):
                test_arr.append(["blocking pair(", app, comp,") and (",other_app, other_comp,")"])
    print(len(test_arr))
    return test_arr

#find_blocking_pairs(list_pairings, applicant_prefs_master, employer_prefs_master)

comp_prefs = {
    'apple': [1,2,3], 
    'ibm': [4,5,6]
} 
app_prefs ={
    1:['apple','ibm'],
    2:['apple','ibm'],
    3:['apple','ibm'],
    4:['ibm','apple'],
    5:['ibm','apple'],
    6:['apple','ibm'],
    7:['apple','ibm']
}
pairs= [['apple', 1],['apple', 3],['apple', 4],['ibm', 2],['apple', 6],['apple', 5]]
find_blocking_pairs(pairs, app_prefs, comp_prefs)