import csv, pickle
import pandas as pd

# FILEPATHS - change these for your own directories
students_csv = "data/gen-1/students.csv"
employers_csv = "data/gen-1/employers.csv"
minorities_csv = "data/gen-1/minorities.csv"
# FILEPATHS - change these for your own directories

def whichPref(applicant, assigned, resident_prefs):
    prefList = applicant_prefs[applicant]
    return prefList.index(assigned) + 1

def matchingResults(final_results, applicant_prefs):
    matchList = []
    resultsDict = {}
    for i in range(100):
        i += 1
        resultsDict[i] = 0
    for school in final_results.keys():
        for assigned in final_results[school]:
            matchList.append([assigned, school])
    for result in matchList:
        applicant = result[0]
        assigned = result[1]
        currResult = whichPref(applicant,assigned,applicant_prefs)
        resultsDict[currResult] += 1
    return sorted(resultsDict.items())

def matchingResultsMinorities(final_results, applicant_prefs):
    matchList = []
    resultsDict = {}
    for i in range(100):
        i += 1
        resultsDict[i] = 0
    for school in final_results.keys():
        for assigned in final_results[school]:
            if minorities[assigned] == 1:
                matchList.append([assigned, school])
    for result in matchList:
        applicant = result[0]
        assigned = result[1]
        currResult = whichPref(applicant,assigned,applicant_prefs)
        resultsDict[currResult] += 1
    return sorted(resultsDict.items())

def isMinority(applicant, minorities):
    return bool(minorities[applicant])

def minorityPercent(final_results, minorities):
    pairs = []
    for comp in employer_prefs.keys():
        total_apps = 0
        total_minorities = 0
        acceptedApps = final_results[comp]
        for app in acceptedApps:
            if isMinority(app, minorities):
                total_minorities += 1
            total_apps += 1
        pairs.append([comp, round(total_minorities/float(total_apps),2)])
    return pairs

def daToDict(da_results_list,employer_prefs):
    retDict = {}
    i = 0
    for comp in employer_prefs.keys():
        retDict[comp] = da_results_list[i].copy()
        i += 1
    return retDict

#Export Top Choice Optimatlity for DA w/ and w/o minority minority_reserves
def exportTopChoiceOptimality(choices, filelocation):
    colnames = ['gen1','gen1m', 'gen2','gen2m', 'gen3','gen3m', 'gen4','gen4m',\
    'gen5','gen5m', 'gen6','gen6m', 'gen7','gen7m', 'gen8','gen8m', 'gen9',\
    'gen9m', 'gen10','gen10m']

    top_choice_dict = {}
    for col in range(len(colnames)):
        top_choice_dict[colnames[col]] = choices[col]

    df_top_choice_opt = pd.DataFrame(top_choice_dict)
    print(df_top_choice_opt)
    df_top_choice_opt.to_csv(filelocation, index = False, header = True)

def exportMinortyProp(company_names, minority_prop, filelocation):
    colnames = ['gen1','gen1m', 'gen2','gen2m', 'gen3','gen3m', 'gen4','gen4m',\
    'gen5','gen5m', 'gen6','gen6m', 'gen7','gen7m', 'gen8','gen8m', 'gen9',\
    'gen9m', 'gen10','gen10m']

    minority_prop_dict = {}
    for col in range((len(colnames))):
        minority_prop_dict[colnames[col]] = minority_prop[col]

    df_minority_prop = pd.DataFrame(minority_prop_dict)
    print(df_minority_prop)
    df_minority_prop.to_csv(filelocation, index = company_names, header = True)

def compareAlgos(ttc_results, da_results, applicant_prefs, employer_prefs):
    ttcDict = {}
    daDict = {}
    total = 0
    diff = 0
    for comp in ttc_results.keys():
        for app in ttc_results[comp]:
            pref_number = whichPref(app, comp, applicant_prefs)
            ttcDict[app] = pref_number
    for comp in da_results.keys():
        for app in da_results[comp]:
            pref_number = whichPref(app, comp, applicant_prefs)
            daDict[app] = pref_number
    for app in ttcDict.keys():
        if app in daDict.keys():
            prefReceivedTTC = ttcDict[app]
            prefReceivedDA = daDict[app]
            diff = diff + (prefReceivedDA - prefReceivedTTC)
            total += 1
    return diff/total

vik_optimality_ttc = []
vik_minority_analysis_ttc = []
for generation in range(1, 11):
    print("generation" + str(generation))
    # capacities_csv_test = "csvs_from_randomdataengine/capacities.csv"
    # students_csv_test = "csvs_from_randomdataengine/students.csv"
    # employers_csv_test = "csvs_from_randomdataengine/employers.csv"
    # minorities_csv_test = "csvs_from_randomdataengine/minorities.csv"
    # minority_reserves_csv_test = "csvs_from_randomdataengine/minority_reserves.csv"

    generation = str(generation)
    students_csv =  "data/gen-" + generation + "/students.csv"
    employers_csv = "data/gen-" + generation + "/employers.csv"
    minorities_csv = "data/gen-" + generation + "/minorities.csv"

    applicant_prefs = {}
    employer_prefs = {}
    minorities = {}


    with open(students_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            stud = int(row[0])
            prefs = row[1].strip('][').split(', ')
            for i in range(len(prefs)):
                prefs[i] = prefs[i][1:-1]
            applicant_prefs[stud] = prefs

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

    file_path = "results/TTC/mr-gen-" + generation
    ttcMRDict = open(file_path, "rb")
    ttcMR = pickle.load(ttcMRDict)

    file_path = "results/TTC/no-mr-gen-" + generation
    ttcNoMRDict = open(file_path, "rb")
    ttcNoMR = pickle.load(ttcNoMRDict)

    file_path = "results/DA/mr-gen-" + generation
    daMRDict = open(file_path, "rb")
    daMR = pickle.load(daMRDict)

    file_path = "results/DA/no-mr-gen-" + generation
    daNoMRDict = open(file_path, "rb")
    daNoMR = pickle.load(daNoMRDict)

    ##BLOCKING PAIR
    pairings = []
    for comp in ttcNoMR:
        for app in ttcNoMR[comp]:
            pair = [comp,app]
            pairings.append(pair)
    pairings

    comp_prefs_indexed = {}
    app_prefs_indexed = {}
    def create_indexes():
        for comp in employer_prefs:
            index = 0
            comp_prefs_indexed[comp] = {}
            for app in employer_prefs[comp]:
                comp_prefs_indexed[comp][app] = index
                index+=1
        for app in applicant_prefs:
            index = 0
            app_prefs_indexed[app] = {}
            for comp in applicant_prefs[app]:
                app_prefs_indexed[app][comp] = index
                index+=1
    create_indexes()      
    
    def blocking_pairs(pairings, prefs_app, prefs_comp):
        test_arr = []
        count = 0
        for pair in pairings:
            comp = pair[0]
            app = pair[1]
            for other_pair in pairings:
                other_comp = other_pair[0]
                other_app = other_pair[1]
                try:
                    if app not in comp_prefs_indexed[other_comp].keys():
                        print('reached 1')
                        continue
                except KeyError:
                        pass
                try:
                    if other_comp not in app_prefs_indexed[app].keys():
                        print('reached 2')
                        continue
                except KeyError:
                        pass
                try:
                    if comp == other_comp and app == other_app:
                        print('reached 3')
                        continue
                except KeyError:
                        pass
                try:
                    if app_prefs_indexed[app][comp] > app_prefs_indexed[app][other_comp] and comp_prefs_indexed[other_comp][app] > comp_prefs_indexed[other_comp][other_app]:
                        test_arr.append(["blocking pair", app, comp," and ",other_app, other_comp])
                        count+=1
                except KeyError:
                        pass
        print(len(test_arr))
        print(count)
        return test_arr

    blocking_pairs(pairings, applicant_prefs, employer_prefs)

    # print("=====NO RESERVES=====")
    ttcNoMRMatchings = matchingResults(ttcNoMR, applicant_prefs)
    ttcNoMRMinorityOnlyMatchings = matchingResultsMinorities(ttcNoMR, applicant_prefs)
    # print(ttcNoMRMatchings)
    ttcNoMRResults = []
    ttcNoMRAllResults = []
    ttcNoMRMinorityOnlyResults = []
    ttcNoMRPropResults = []
    for pair in ttcNoMRMatchings:
        ttcNoMRAllResults.append(pair[1])
    for pair in ttcNoMRMinorityOnlyMatchings:
        ttcNoMRMinorityOnlyResults.append(pair[1])
    minorityPropsNoMR = minorityPercent(ttcNoMR, minorities)
    for pair in minorityPropsNoMR:
        ttcNoMRPropResults.append(pair[1])
    ttcNoMRAllResults = (ttcNoMRAllResults.copy(), ttcNoMRMinorityOnlyResults.copy())
    # print(minorityPropsNoMR)
    # print("\n")
    # print("=====RESERVES=====")
    ttcMRMatchings = matchingResults(ttcMR, applicant_prefs)
    ttcMRMinorityOnlyMatchings = matchingResultsMinorities(ttcMR, applicant_prefs)
    # print(ttcMRMatchings)
    ttcMRPropResults = []
    ttcMRResults = []
    ttcMRAllResults = []
    ttcMRMinorityOnlyResults = []
    ttcMRPropResults = []
    for pair in ttcMRMatchings:
        ttcMRAllResults.append(pair[1])
    for pair in ttcMRMinorityOnlyMatchings:
        ttcMRMinorityOnlyResults.append(pair[1])
    minorityPropsMR = minorityPercent(ttcMR, minorities)
    for pair in minorityPropsMR:
        ttcMRPropResults.append(pair[1])
    ttcMRAllResults = (ttcMRAllResults.copy(), ttcMRMinorityOnlyResults.copy())
    # print(minorityPercent(ttcMR, minorities))
    # print("\n")
    # print("=====COMPARISON=====")
    daDict = daToDict(daMR, employer_prefs)
    # print(compareAlgos(ttcMR, daDict, applicant_prefs, employer_prefs))
    vik_optimality_ttc.append(ttcNoMRAllResults)
    vik_optimality_ttc.append(ttcMRAllResults)
    vik_minority_analysis_ttc.append(ttcNoMRPropResults.copy())
    vik_minority_analysis_ttc.append(ttcMRPropResults.copy())
print(vik_optimality_ttc) # this is stat 1 Vik
print(vik_minority_analysis_ttc) # this is stat 2 Vik
print(employer_prefs.keys()) # this is the list of companies Vik

#Export Top Choice Optimatlity for all geneartions of TTC w/ and w/o minority minority_reserves
exportTopChoiceOptimality(vik_optimality_ttc, 'results/TTC/topChoiceOptimality.csv')

#Export Minory Proprotions for all generations of TTC w/ and w/o minority minority_reserves
exportMinortyProp(employer_prefs.keys(), vik_minority_analysis_ttc, 'results/TTC/minortyProp.csv')
