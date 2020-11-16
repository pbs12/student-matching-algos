import csv

# FILEPATHS - change these for your own directories
capacities_csv = "capacities.csv"
students_csv = "students.csv"
employers_csv = "employers.csv"
minorities_csv = "minorities.csv"
minority_reserves_csv = "minority_reserves.csv"
# minority_reserves_csv = "mr_0s.csv"
# FILEPATHS - change these for your own directories

capacities = {}
applicant_prefs = {}
applicant_prefs_res = {}
employer_prefs = {}
minorities = {}
minority_reserves = {}

with open(capacities_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        comp = row[0]
        cap = int(row[1])
        capacities[comp] = cap
    
with open(students_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        stud = int(row[0])
        prefs = row[1].strip('][').split(', ')
        for i in range(len(prefs)):
            prefs[i] = prefs[i][1:-1]
        applicant_prefs[stud] = prefs

with open(students_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        stud = int(row[0])
        prefs = row[1].strip('][').split(', ')
        for i in range(len(prefs)):
            prefs[i] = prefs[i][1:-1]
        applicant_prefs_res[stud] = prefs
applicant_prefs_master = applicant_prefs_res

with open(employers_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        comp = row[0]
        prefs = row[1].strip('][').split(', ')
        for i in range(len(prefs)):
            prefs[i] = int(prefs[i])
        employer_prefs[comp] = prefs
employers_pref_master = employer_prefs 

with open(minorities_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        stud = int(row[0])
        minority = int(row[1])
        minorities[stud] = minority

with open(minority_reserves_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        comp = row[0]
        cap = int(row[1])
        minority_reserves[comp] = cap

def TTC_without_reserves(applicant_prefs, company_prefs, capacities):
    total_cap = 0
    placements = {}
    for c in capacities.keys():
        placements[c] = []
        total_cap += capacities[c]
    while total_cap > 0 and len(applicant_prefs.keys()) != 0:
        appsToDelete = []
        compsToDelete = []
        graph = {}
        for comp in company_prefs.keys():
            if company_prefs[comp] == []:
                compsToDelete.append(comp)
                continue
            first_choice = company_prefs[comp][0]
            while first_choice not in applicant_prefs.keys():
                del company_prefs[comp][0]
                if company_prefs[comp] == []:
                    compsToDelete.append(comp)
                    continue
                first_choice = company_prefs[comp][0]
            graph[comp] = first_choice
            # del company_prefs[comp][0]
        for app in applicant_prefs.keys():
            if applicant_prefs[app] == []:
                appsToDelete.append(app)
                continue
            first_choice = applicant_prefs[app][0]
            while capacities[first_choice] == 0:
                del applicant_prefs[app][0]
                if applicant_prefs[app] == []:
                    appsToDelete.append(app)
                    continue
                first_choice = applicant_prefs[app][0]
            graph[app] = first_choice
            # del applicant_prefs[app][0]
        cycles = set()
        for node in graph.keys():
            if node in applicant_prefs.keys():
                cycle = search_cycle(graph, node, node, True, [node])
                if cycle != False:
                    del cycle[-1]
                    new_cycle = []
                    cycle = frozenset([cycle[k] for k in range(len(cycle)) if k % 2 == 0])
                    cycles.add(cycle)
        for cycle in cycles:
            for app in cycle:
                placements[graph[app]].append(app)
                del applicant_prefs[app]
                capacities[graph[app]] -= 1
                total_cap -= 1
        for app in appsToDelete:
            del applicant_prefs[app]
        for comp in compsToDelete:
            del company_prefs[comp]
    counter = 0
    for lst in placements.values():
        counter += len(lst)
    print(counter)
    return placements

def TTC_with_reserves(applicant_prefs, company_prefs, capacities, minorities, minority_reserves):
    total_cap = 0
    round_num = 1
    placements = {}
    for c in capacities.keys():
        placements[c] = []
        total_cap += capacities[c]
    while total_cap > 0 and len(applicant_prefs.keys()) != 0:
    #while round_num < 3:
        appsToDelete = []
        compsToDelete = []
        graph = {}
        apps_via_mr = []
        for comp in company_prefs.keys():
            if company_prefs[comp] == []:
                    compsToDelete.append(comp)
                    continue
            first_choice = company_prefs[comp][0]
            if minority_reserves[comp] > 0:
                for app in company_prefs[comp]:
                    if isMinority(app, minorities) and app in applicant_prefs.keys():
                        first_choice = app
                        apps_via_mr.append([app, comp])
                        break
                if not isMinority(first_choice, minorities) or first_choice not in applicant_prefs.keys():
                    while first_choice not in applicant_prefs.keys():
                        del company_prefs[comp][0]
                        if company_prefs[comp] == []:
                            compsToDelete.append(comp)
                            continue
                        first_choice = company_prefs[comp][0]
            else:
                while first_choice not in applicant_prefs.keys():
                    del company_prefs[comp][0]
                    if company_prefs[comp] == []:
                        compsToDelete.append(comp)
                        continue
                    first_choice = company_prefs[comp][0]
            graph[comp] = first_choice
            # del company_prefs[comp][0]
        for app in applicant_prefs.keys():
            if applicant_prefs[app] == []:
                appsToDelete.append(app)
                continue
            first_choice = applicant_prefs[app][0]
            while capacities[first_choice] == 0:
                del applicant_prefs[app][0]
                if applicant_prefs[app] == []:
                    appsToDelete.append(app)
                    continue
                first_choice = applicant_prefs[app][0]
            graph[app] = first_choice
            # del applicant_prefs[app][0]
        cycles = set()
        for node in graph.keys():
            if node in applicant_prefs.keys():
                cycle = search_cycle(graph, node, node, True, [node])
                if cycle != False:
                    del cycle[-1]
                    new_cycle = []
                    cycle = frozenset([cycle[k] for k in range(len(cycle)) if k % 2 == 0])
                    cycles.add(cycle)
        for cycle in cycles:
            # print(cycle)
            for app in cycle:
                placements[graph[app]].append(app)
                del applicant_prefs[app]
                if isMinority(app, minorities) and minority_reserves[graph[app]] > 0:
                    minority_reserves[graph[app]] -= 1
                """
                for entry in apps_via_mr:
                    minority = entry[0]
                    comp = entry[1]
                    if minority == app and comp == graph[app]:
                        minority_reserves[graph[app]] -= 1
                """
                capacities[graph[app]] -= 1
                total_cap -= 1
        for app in appsToDelete:
            del applicant_prefs[app]
        for comp in compsToDelete:
            del company_prefs[comp]
        #print(apps_via_mr)
        #print(round_num)
        #print(len(applicant_prefs.keys()))
        #round_num += 1
        #print(len(applicant_prefs.keys()))
        #print(minority_reserves)
        totalMin = 0
        for val in applicant_prefs.keys():
            if isMinority(val, minorities):
                totalMin += 1
        #print(placements)
        #print(totalMin)
    counter = 0
    for lst in placements.values():
        counter += len(lst)
    print(counter)
    print(minority_reserves)
    return placements

def isMinority(applicant, minorities):
    return bool(minorities[applicant])

def search_cycle(graph, curr, begin, isFirst, path):
    if curr == begin and not isFirst:
        return path
    if curr in graph.keys():
        curr = graph[curr]
    else:
        return False
    if curr in path and curr != begin:
        return False
    return search_cycle(graph, curr, begin, False, path + [curr])

def whichPref(resident, assigned, resident_prefs):
    prefList = resident_prefs[resident]
    return prefList.index(assigned) + 1

def matchingResults(final_results, resident_prefs):
    matchList = []
    resultsDict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    for school in final_results.keys():
        for assigned in final_results[school]:
            matchList.append([assigned, school])
    for result in matchList:
        resident = result[0]
        assigned = result[1]
        currResult = whichPref(resident,assigned,resident_prefs)
        if currResult <= 10:
            resultsDict[currResult] += 1
    return resultsDict

# applicant_prefs = {1: ["2"], 2: ["1"], 3: ["3"], 4: ["2"]}
# company_prefs = {"1": [1], "2": [2], "3": [3]}
# capacities = {"1": 2, "2": 2, "3": 2}


ttcRes = TTC_with_reserves(applicant_prefs, employer_prefs, capacities, minorities, minority_reserves)
print(matchingResults(ttcRes, applicant_prefs_res))

#BLOCKING PAIRS

def list_pairings(pairing_master_list):
    agg = []
    for pairing in pairing_master_list:
        company = pairing
        for app in pairing_master_list[pairing]:
            temp = [company, app]
            agg.append(temp)
    return agg
list_pairings = list_pairings(ttcRes)

def find_blocking_pairs3(pairings, prefs_app, prefs_comp):
    count = 0
    test_arr = ['nun']
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
                test_arr.append(["blocking pair", app, comp," and ",other_app, other_comp])
    print(len(test_arr))
    return test_arr
find_blocking_pairs3(list_pairings, applicant_prefs_master, employer_prefs_master)
