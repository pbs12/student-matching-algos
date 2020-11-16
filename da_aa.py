import csv
import pandas as pd

def fetch_csv_data(capacities_csv, applicants_csv, employers_csv, minorities_csv, minority_reserves_csv):

    # Dictionaries to Store CSV Data
    reference_dict = {} # (Company Number: Company Name)
    capacities = {} # (employers : # slots available)
    applicant_prefs = {} # (applicant (int) : list of applicant prefrences)
    employer_prefs = {} # (employer (string) : list of employer prefrences )
    minorities = {} # (applicant (int) : 1 or 0)
    minority_reserves = {} # (employers : minimum number of minorities)

    with open(capacities_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            comp = row[0]
            cap = int(row[1])
            capacities[comp] = cap

    with open(applicants_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            stud = int(row[0])
            prefs = row[1].strip('][').split(', ')
            for i in range(len(prefs)):
                prefs[i] = prefs[i][1:-1]
            applicant_prefs[stud] = prefs

    with open(employers_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        index = 0
        for row in csvreader:
            comp = row[0]

            #Construct Reference Dict
            reference_dict[comp] = index
            index += 1
            #Construct employer_pref Dict
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
    return (reference_dict, capacities, applicant_prefs, employer_prefs, minorities, minority_reserves)

#Preprocessing to fit generated data with our DA Alogorithim Implementation
def preprocessing(reference_dict, capacities, applicant_prefs, employer_prefs, minorities, minority_reserves):
    companies = []
    applicants_reg = []
    applicants_diversity = set([])
    capacities_list = []
    minority_reserves_list = []

    #Intialize Arrays
    for _ in range(len(employer_prefs.keys())):
        companies.append(0)
        capacities_list.append([])
        minority_reserves_list.append(0)
    for _ in range(len(applicant_prefs.keys())):
        applicants_reg.append(0)

    #Create List of Employer Preferences
    for key in employer_prefs:
        company_index = reference_dict[key]
        companies[company_index] = employer_prefs[key]

    #Create list of applicant preferences
    for key in applicant_prefs:
        employers_by_number = []
        #Convert array of companies by String to comapnies by Id
        for company in applicant_prefs[key]:
            employers_by_number.append(reference_dict[company])
        applicants_reg[key] = employers_by_number

    #Create diveristy set
    for minority in minorities:
        if(minorities[minority] == 1):
            applicants_diversity.add(minority)

    #Create Capacities
    for employer in capacities:
        employer_id = reference_dict[employer]
        capacities_list[employer_id].append(capacities[employer])

    #Create Minority reserves
    for employer in minority_reserves:
        employer_id = reference_dict[employer]
        minority_reserves_list[employer_id] = minority_reserves[employer]

    return (companies, applicants_reg, capacities_list, applicants_diversity, minority_reserves_list, reference_dict)


def da_classic(companies, applicants_all, capacitiesAlt, applicants_diversity):

    tentativelyMatched = set([]) #running array to keep track of applicants tentatively matched
    company_matches = [] #running track of what applicants are tentatively matched, updated each round
    possibleAppliers = []
    for _ in range(len(companies)):
        company_matches.append([])
        possibleAppliers.append(set([]))

    for app_round in range(len(companies)):

        for applicant in range(len(applicants_all)):
            if applicant not in tentativelyMatched:
                #groups unmatched applicant by hospital preference of that round
                possibleAppliers[applicants_all[applicant][app_round]].add(applicant)
        for company in range(len(companies)):
            currentWaitlist = set(company_matches[company]) #retrieves applicants currently matched at hospital
            newWaitlist = set([])
            for applicant in range(len(applicants_all)): #goes through each hospital's applicant pref lists in order
                applicantID = companies[company][applicant] #retrieves the actual ID of the applicant
                if ((applicantID in possibleAppliers[company]) or (applicantID in currentWaitlist)) and (len(newWaitlist) < capacitiesAlt[company][0]):
                    #if applicant is either already matched to hospital or have it as their relevant preference, and hospital below capacity, then matched
                    newWaitlist.add(applicantID) #add to list of applicants matched at hospital
                    if applicantID not in tentativelyMatched:
                        tentativelyMatched.add(applicantID) #adds to list of all matched applicants
                elif (applicantID in currentWaitlist) and (len(newWaitlist) >= capacitiesAlt[company][0]):
                    #if applicant who is currently matched is being kicked off because hospital is above capacity, unmatched
                    tentativelyMatched.remove(applicantID)
            company_matches[company] = list(newWaitlist) #replace old list of matched applicants at hospital with updated one
    return company_matches

'''
DA algo adjusted for affirmative action via minority reserves
For more info visit: https://onlinelibrary.wiley.com/doi/epdf/10.3982/TE1135
'''

def da_aa(companies, applicants_all, capacitiesAlt, applicants_diversity, minority_reserve_quantity):
    tentativelyMatched = set([]) #running array to keep track of applicants tentatively matched
    company_matches = [] #running track of what applicants are tentatively matched, updated each round
    possibleAppliers = []
    for _ in range(len(companies)):
        company_matches.append([])
        possibleAppliers.append(set([]))

    for app_round in range(len(companies)):
        for applicant in range(len(applicants_all)):
            if applicant not in tentativelyMatched:
                possibleAppliers[applicants_all[applicant][app_round]].add(applicant)
        for company in range(len(companies)):
            currentWaitlist = set(company_matches[company]) #retrieves applicants currently matched at hospital
            newWaitlist = set([])
            for applicant in range((len(applicants_all))):
                applicantID = companies[company][applicant]
                if(applicantID in applicants_diversity):
                    if ((applicantID in possibleAppliers[company]) or (applicantID in currentWaitlist)) and (len(newWaitlist) < capacitiesAlt[company][0]) and (len(newWaitlist) < minority_reserve_quantity[company]):
                        #if applicant is either already matched to hospital or have it as their relevant preference, and hospital below capacity, then matched
                        newWaitlist.add(applicantID) #add to list of applicants matched at hospital
                        if applicantID not in tentativelyMatched:
                            tentativelyMatched.add(applicantID) #adds to list of all matched applicants
                    elif (applicantID in currentWaitlist) and (len(newWaitlist) >= minority_reserve_quantity[company]):
                       #if applicant who is currently matched is being kicked off because hospital is above capacity, unmatched
                       tentativelyMatched.remove(applicantID)
            #Now grab regular applicants
            for applicant in range(len(applicants_all)): #goes through each hospital's applicant pref lists in order
                applicantID = companies[company][applicant] #retrieves the actual ID of the applicant
                if (applicantID not in newWaitlist):
                    if ((applicantID in possibleAppliers[company]) or (applicantID in currentWaitlist)) and (len(newWaitlist) < capacitiesAlt[company][0]):
                        #if applicant is either already matched to hospital or have it as their relevant preference, and hospital below capacity, then matched
                        newWaitlist.add(applicantID) #add to list of applicants matched at hospital
                        if applicantID not in tentativelyMatched:
                            tentativelyMatched.add(applicantID) #adds to list of all matched applicants
                    elif (applicantID in currentWaitlist) and (applicantID in tentativelyMatched) and (len(newWaitlist) >= capacitiesAlt[company][0]):
                        #if applicant who is currently matched is being kicked off because hospital is above capacity, unmatched
                        tentativelyMatched.remove(applicantID)
            company_matches[company] = list(newWaitlist) #replace old list of matched applicants at hospital with updated one
    return company_matches

def printDAResultsPerapplicant(company_matches):
    print(company_matches)
    for company in company_matches:
        for applicant in company:
            print("applicant " + str(applicant) + " is in company: " + str(company_matches.index(company)))

'''
finds the number of applicants who got Nth preference and prints it
returns two arrays: (for all applicants, for minorities)
'''
def getTopChoiceOptimality(company_matches, applicants, diversity_set):
    choiceCount = [0]*len(company_matches)
    diversity_choice_count = [0] * len(company_matches)
    for applicant in range(len(applicants)): #for each applicant,
        for company in range(len(company_matches)):
            if applicant in company_matches[company]: #find what company they are at,
                #print("applicant #" + str(applicant) + " is in company " + str(applicants[applicant].index(company)))
                choice = applicants[applicant].index(company) #see what number preference that hospital was for them,
                choiceCount[choice] += 1 #and update the tally of applicants who got that number preference

                if(applicant in diversity_set):
                    diversity_choice_count[choice] += 1

    for printnum in range(len(company_matches)):
        print("The number of applicants who got choice #" + str(printnum+1) + " is " + str(choiceCount[printnum]))
    print('\n')

    for printnum in range(len(company_matches)):
        print("The number of minority applicants who got choice #" + str(printnum+1) + " is " + str(diversity_choice_count[printnum]))
    print('\n')

    #Return Preference Array
    return (choiceCount, diversity_choice_count)

'''takes in the list of applicants accepted at each company
and the list of minorities and returns the list and
percentage of interns at each company that are minorities '''
def getMinorityProp(company_matches,minorities):
    num_company = len(company_matches)

    minorityTracker = []
    minorityPercentages = []
    for _ in range(num_company):
        minorityTracker.append([])
        minorityPercentages.append([])

    for i in range(0,num_company):
        accepted_to_this_company = company_matches[i]
        for j in range(1,len(accepted_to_this_company)):
            if accepted_to_this_company[j] in minorities:
                minorityTracker[i].append(accepted_to_this_company[j])
        minorityPercentages[i] = (len(minorityTracker[i])/len(accepted_to_this_company))
    return minorityPercentages #,minorityTracker - can also track minorities per company

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


''' DA AA Test Cases'''

'''Test Case for 1 round of DA'''

companies2 = [[0,1,2,3],[1,0,2,3],[0,1,2,3]]
applicants_reg = [[0,1,2],[0,1,2], [1,0,2],[0,1,2]]
applicants_diversity = set([1,2])
capacities2 = [[1],[1],[2]]
minority_reserves = [1, 1, 1]

company_matches_test = da_aa(companies2, applicants_reg, capacities2, applicants_diversity, minority_reserves)
printDAResultsPerapplicant(company_matches_test)
getTopChoiceOptimality(company_matches_test, applicants_reg, applicants_diversity)

'''Test Case for 2 round of DA'''

companies2 = [[0,1,2,3],[1,0,2,3],[0,1,3,2]]
applicants_reg = [[1,0,2],[0,1,2], [0,1,2],[1,0,2]]
applicants_diversity = set([1,2])
capacities2 = [[1],[1],[2]]
minority_reserves = [1, 1, 1]

company_matches_test = da_aa(companies2, applicants_reg, capacities2, applicants_diversity, minority_reserves)
printDAResultsPerapplicant(company_matches_test)
getTopChoiceOptimality(company_matches_test, applicants_reg, applicants_diversity)

'''Test Case for smaller amount of minoirty reserves'''

companies2 = [[0,1,2,3],[1,0,2,3],[0,1,3,2]]
applicants_reg = [[0,1,2],[0,1,2], [0,1,2],[1,0,2]]
applicants_diversity = set([1,2])
capacities2 = [[2],[1],[2]]
minority_reserves = [0, 1, 1]

company_matches_test = da_aa(companies2, applicants_reg, capacities2, applicants_diversity, minority_reserves)
printDAResultsPerapplicant(company_matches_test)
getTopChoiceOptimality(company_matches_test, applicants_reg, applicants_diversity)


'''
Generate Data for analysis of algorithims:

Here we run both DA with minority reserves and DA without minority reserves on
10 intelligent generated datasets from employer and applicant prefrences. We then
export the results of each of our analysis (top choice optimality, minority percents, etc)
to csv's to produce graphs.
'''

topChoiceOptimalityData = []
minority_prop = []
totalMinorityCount = 0
totalReserveCount = 0
for generation in range(1, 11):
    print("generation" + str(generation))
    # capacities_csv_test = "csvs_from_randomdataengine/capacities.csv"
    # applicants_csv_test = "csvs_from_randomdataengine/applicants.csv"
    # employers_csv_test = "csvs_from_randomdataengine/employers.csv"
    # minorities_csv_test = "csvs_from_randomdataengine/minorities.csv"
    # minority_reserves_csv_test = "csvs_from_randomdataengine/minority_reserves.csv"

    generation = str(generation)
    capacities_csv_test = "data/gen-" + generation + "/gencapacities.csv"
    applicants_csv_test =  "data/gen-" + generation + "/students.csv"
    employers_csv_test = "data/gen-" + generation + "/employers.csv"
    minorities_csv_test = "data/gen-" + generation + "/minorities.csv"
    minority_reserves_csv_test = "data/gen-" + generation + "/minority_reserves.csv"


    #CSV Data -> Preprocessing -> DA -> Output Matches/Analysis

    raw_csv_dicts = fetch_csv_data(capacities_csv_test, applicants_csv_test, employers_csv_test, minorities_csv_test, minority_reserves_csv_test)

    reference_dict, capacities, applicant_prefs, employer_prefs, minorities, minority_reserves = raw_csv_dicts
    result = preprocessing(reference_dict, capacities, applicant_prefs, employer_prefs, minorities, minority_reserves)

    companies_list, applicant_reg, capacities_list, applicants_diversity, minority_reserves_list, reference_dict = result

    #Add minority reserves capacity when we want to increase the Reserve Ratio synthetically
    # for i in range(len(minority_reserves_list)):
    #     minority_reserves_list[i] = minority_reserves_list[i]+8


    #Perform DA and DA w/ minority reserves for each generation of data.

    company_matches_classic = da_classic(companies_list, applicant_reg, capacities_list, applicants_diversity)
    company_matches_minority_reseves = da_aa(companies_list, applicant_reg, capacities_list, applicants_diversity, minority_reserves_list)

    #Collect Statistics

    topChoiceOptimalityData.append(getTopChoiceOptimality(company_matches_classic, applicant_reg, applicants_diversity))
    topChoiceOptimalityData.append(getTopChoiceOptimality(company_matches_minority_reseves, applicant_reg, applicants_diversity))
    minority_prop.append(getMinorityProp(company_matches_classic, applicants_diversity))
    minority_prop.append(getMinorityProp(company_matches_minority_reseves, applicants_diversity))

    #Calculate the Reserve Ratio
    totalReserveCount += sum(minority_reserves_list)
    totalMinorityCount += len(applicants_diversity)

'''Display Stats'''

print("The Reserve Ratio is " + str(totalReserveCount/totalMinorityCount))
#Get Company Names
with open( "data/gen-1/employers.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    comp_string_arr = []
    for row in csvreader:
        comp_string_arr.append(row[0])

#Export Top Choice Optimatlity for all geneartions for DA w/ and w/o minority minority_reserves
exportTopChoiceOptimality(topChoiceOptimalityData, 'results/DA/topChoiceOptimality.csv')

#Export Minory Proprotions for all generations for DA w/ and w/o minority minority_reserves
exportMinortyProp(comp_string_arr, minority_prop, 'results/DA/minortyProp.csv')
