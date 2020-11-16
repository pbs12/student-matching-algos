import csv

#number_to_company_csv = "csvs_from_randomdataengine/table.csv"
# FILEPATHS - change these for your own directories

# with open(number_to_company_csv, 'r') as csvfile:
#     csvreader = csv.reader(csvfile, delimiter=',')
#     next(csvreader)
#     for row in csvreader:
#         number = int(row[0])
#         company_name = row[1]
#         reference_dict[company_name] = number

def fetch_csv_data(capacities_csv, students_csv, employers_csv, minorities_csv, minority_reserves_csv):

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
    students_reg = []
    students_diversity = set([])
    capacities_list = []
    minority_reserves_list = []

    #Intialize Arrays
    for _ in range(len(employer_prefs.keys())):
        companies.append(0)
        capacities_list.append([])
        minority_reserves_list.append(0)
    for _ in range(len(applicant_prefs.keys())):
        students_reg.append(0)

    #Create List of Employer Preferences
    for key in employer_prefs:
        company_index = reference_dict[key]
        companies[company_index] = employer_prefs[key]

    #Create list of student preferences
    for key in applicant_prefs:
        employers_by_number = []
        #Convert array of companies by String to comapnies by Id
        for company in applicant_prefs[key]:
            employers_by_number.append(reference_dict[company])
        students_reg[key] = employers_by_number

    #Create diveristy set
    for minority in minorities:
        if(minorities[minority] == 1):
            students_diversity.add(minority)

    #Create Capacities
    for employer in capacities:
        employer_id = reference_dict[employer]
        capacities_list[employer_id].append(capacities[employer])

    #Create Minority reserves
    for employer in minority_reserves:
        employer_id = reference_dict[employer]
        minority_reserves_list[employer_id] = minority_reserves[employer]

    return (companies, students_reg, students_diversity, capacities_list, minority_reserves_list)


def da_classic(companies, students_all, capacitiesAlt, students_diversity):

    tentativelyMatched = [] #running array to keep track of residents tentatively matched
    company_matches = [] #running track of what students are tentatively matched, updated each round
    possibleAppliers = []
    for _ in range(len(companies)):
        company_matches.append([])
        possibleAppliers.append([])

    for app_round in range(len(companies)):

        for resident in range(len(students_all)):
            if resident not in tentativelyMatched:
                #groups unmatched student by hospital preference of that round
                possibleAppliers[students_all[resident][app_round]].append(resident)
        for school in range(len(companies)):
            currentWaitlist = company_matches[school] #retrieves students currently matched at hospital
            newWaitlist = [] #new empty list
            for student in range(len(students_all)): #goes through each hospital's student pref lists in order
                studentID = companies[school][student] #retrieves the actual ID of the student
                if ((studentID in possibleAppliers[school]) or (studentID in currentWaitlist)) and (len(newWaitlist) < capacitiesAlt[school][0]):
                    #if student is either already matched to hospital or have it as their relevant preference, and hospital below capacity, then matched
                    newWaitlist.append(studentID) #add to list of students matched at hospital
                    if studentID not in tentativelyMatched:
                        tentativelyMatched.append(studentID) #adds to list of all matched students
                elif (studentID in currentWaitlist) and (len(newWaitlist) >= capacitiesAlt[school][0]):
                    #if student who is currently matched is being kicked off because hospital is above capacity, unmatched
                    tentativelyMatched.remove(studentID)
            company_matches[school] = newWaitlist #replace old list of matched students at hospital with updated one
    return company_matches

'''
DA algo adjusted for affirmative action via minority reserves
For more info visit: https://onlinelibrary.wiley.com/doi/epdf/10.3982/TE1135
'''

def da_aa(companies, students_all, capacitiesAlt, students_diversity, minority_reserve_quantity):
    print(capacitiesAlt)
    print(capacities_list)
    print(students_diversity)

    tentativelyMatched = [] #running array to keep track of residents tentatively matched
    minority_reserve_admits = 0
    company_matches = [] #running track of what students are tentatively matched, updated each round
    possibleAppliers = []
    for _ in range(len(companies)):
        company_matches.append([])
        possibleAppliers.append([])

    for app_round in range(len(companies)):

        for resident in range(len(students_all)):
            if resident not in tentativelyMatched:
                #groups unmatched student by hospital preference of that round
                possibleAppliers[students_all[resident][app_round]].append(resident)
        for school in range(len(companies)):
            currentWaitlist = company_matches[school] #retrieves students currently matched at hospital
            newWaitlist = [] #new empty list

            #First grab diversity students - how do i do this with teantively matched???
            for student in range((len(students_all))):
                studentID = companies[school][student]
                if(studentID in students_diversity):
                    if ((studentID in possibleAppliers[school]) or (studentID in currentWaitlist)) and (len(newWaitlist) < capacitiesAlt[school][0]) and (len(newWaitlist) < minority_reserve_quantity[school]):
                        #if student is either already matched to hospital or have it as their relevant preference, and hospital below capacity, then matched
                        newWaitlist.append(studentID) #add to list of students matched at hospital
                        #print(str(studentID) + "minority" + str(school))
                        if studentID not in tentativelyMatched:
                            tentativelyMatched.append(studentID) #adds to list of all matched students
                    elif (studentID in currentWaitlist) and (len(newWaitlist) >= capacitiesAlt[school][0]):
                        #if student who is currently matched is being kicked off because hospital is above capacity, unmatched
                        tentativelyMatched.remove(studentID)

            #Now grab regular students
            for student in range(len(students_all)): #goes through each hospital's student pref lists in order
                studentID = companies[school][student] #retrieves the actual ID of the student
                if (studentID not in newWaitlist):
                    if ((studentID in possibleAppliers[school]) or (studentID in currentWaitlist)) and (len(newWaitlist) < capacitiesAlt[school][0]):
                        #if student is either already matched to hospital or have it as their relevant preference, and hospital below capacity, then matched
                        newWaitlist.append(studentID) #add to list of students matched at hospital
                        #print(str(studentID) + "non-minority" + str(school))
                        if studentID not in tentativelyMatched:
                            tentativelyMatched.append(studentID) #adds to list of all matched students
                    elif (studentID in currentWaitlist) and (len(newWaitlist) >= capacitiesAlt[school][0]):
                        #if student who is currently matched is being kicked off because hospital is above capacity, unmatched
                        tentativelyMatched.remove(studentID)
            company_matches[school] = newWaitlist #replace old list of matched students at hospital with updated one
    return company_matches

def printDAResultsPerStudent(company_matches):
    print(company_matches)
    for school in company_matches:
        for student in school:
            print("Student " + str(student) + " is in School: " + str(company_matches.index(school)))

'''
finds the number of students who got Nth preference and prints it
'''
def printTopChoiceOptimality(company_matches, students):
    choiceCount = [0]*len(company_matches)
    for resident in range(len(students)): #for each resident,
        for school in range(len(company_matches)):
            if resident in company_matches[school]: #find what school they are at,
                #print("Student #" + str(resident) + " is in school " + str(students[resident].index(school)))
                choice = students[resident].index(school) #see what number preference that hospital was for them,
                choiceCount[choice] += 1 #and update the tally of students who got that number preference

    for printnum in range(len(company_matches)):
        print("The number of students who got choice #" + str(printnum+1) + " is " + str(choiceCount[printnum]))
    print('\n')



''' DA AA Test Cases'''

# companies2 = [[0,1,2,3],[1,0,2,3],[0,1,2,3]]
# students_reg = [[0,1,2],[0,1,2], [1,0,2],[0,1,2]]
# students_diversity = set([1,2])
# capacities2 = [[1],[1],[2]]
# minority_reserves = [1, 1, 1]
#
# company_matches_test = da_aa(companies2, students_reg, capacities2, students_diversity, minority_reserves)
# printDAResultsPerStudent(company_matches_test)
# printTopChoiceOptimality(company_matches_test, students_reg)

''' DA AA on generated data '''

# FILEPATHS - change these for your own directories
capacities_csv_test = "csvs_from_randomdataengine/capacities.csv"
students_csv_test = "csvs_from_randomdataengine/students.csv"
employers_csv_test = "csvs_from_randomdataengine/employers.csv"
minorities_csv_test = "csvs_from_randomdataengine/minorities.csv"
minority_reserves_csv_test = "csvs_from_randomdataengine/minority_reserves.csv"

raw_csv_dicts = fetch_csv_data(capacities_csv_test, students_csv_test, employers_csv_test, minorities_csv_test, minority_reserves_csv_test)

reference_dict, capacities, applicant_prefs, employer_prefs, minorities, minority_reserves = raw_csv_dicts

result = preprocessing(reference_dict, capacities, applicant_prefs, employer_prefs, minorities, minority_reserves)
companies_list = result[0]
student_reg = result[1]
students_diversity = result[2]
capacities_list = result[3]
minority_reserves_list = result[4]

company_matches_test = da_aa(companies_list, student_reg, capacities_list, students_diversity, minority_reserves_list)
#printDAResultsPerStudent(company_matches_test)
printTopChoiceOptimality(company_matches_test, student_reg)

company_matches_test_classic = da_classic(companies_list, student_reg, capacities_list, students_diversity)
# #printDAResultsPerStudent(company_matches_test_classic)
printTopChoiceOptimality(company_matches_test_classic, student_reg)
