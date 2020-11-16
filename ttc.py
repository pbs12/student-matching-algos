import csv, pickle

# FILEPATHS - change these for your own directories
capacities_csv = "data/gen-10/gencapacities.csv"
students_csv = "data/gen-10/students.csv"
employers_csv = "data/gen-10/employers.csv"
minorities_csv = "data/gen-10/minorities.csv"
minority_reserves_csv = "data/gen-10/minority_reserves.csv"
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

with open(employers_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        comp = row[0]
        prefs = row[1].strip('][').split(', ')
        for i in range(len(prefs)):
            prefs[i] = int(prefs[i])
        employer_prefs[comp] = prefs

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




# ttcMR = TTC_with_reserves(applicant_prefs, employer_prefs, capacities, minorities, minority_reserves)
#ttcNoMR = TTC_without_reserves(applicant_prefs, employer_prefs, capacities)
#print(matchingResults(ttcMR, applicant_prefs_res))

# ttcMRDict = open("results/TTC/mr-gen-1", "wb")
# pickle.dump(ttcMR, ttcMRDict)
# ttcMRDict.close()

#ttcNoMRDict = open("results/TTC/no-mr-gen-10", "wb")
#pickle.dump(ttcNoMR, ttcNoMRDict)
#ttcNoMRDict.close()


