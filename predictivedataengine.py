import csv, random, os, math, pickle

#random.seed(1)

# FILEPATHS - change these for your own directories
table_csv = "table.csv"
gpa_csv = "data/gen-10/gpadist.csv"
capacities_csv = "data/gencapacities.csv"
students_csv = "data/students.csv"
employers_csv = "data/employers.csv"
minorities_csv = "data/minorities.csv"
minority_reserves_csv = "data/minority_reserves.csv"
# FILEPATHS - change these for your own directories

class Applicant:
    def __init__(self, number, gpa, hackerrank_score, minority, class_year, experience):
        self.number = number
        self.gpa = gpa
        self.hackerrank_score = hackerrank_score
        self.minority = minority
        self.class_year = class_year
        self.experience = experience
    def __str__(self):
        minority = ""
        if self.minority == 1:
            minority += "minority"
        else:
            minority += "non-minority"
        experience = ""
        if self.experience == 1:
            experience += "has SWE experience"
        else:
            experience += "no SWE experience"
        return str(self.number) + ": " + str(self.gpa) + " | " + str(self.hackerrank_score) + " | " + minority + " | " + str(self.class_year) + " | " + experience

companies = []
with open(table_csv) as csvfile:
    table_reader = csv.reader(csvfile, delimiter=",")
    for row in table_reader:
        if row[0] == 'rank':
            continue
        companies.append(row[1])


fortune_100 = companies[0:100]

capacitiesDict = {}
minorityReservesDict = {}
compWeightDict = {}
employerPrefsDict = {}
desirabilityDict = {}
studentPrefsDict = {}
isMinorityDict = {}

for comp in fortune_100:
    capacitiesDict[comp] = random.randint(50,100)

possibilities = [i/100 for i in range(1, 101)]
for comp in capacitiesDict.keys():
    weightDict = {}
    weight_gpa = random.choice(possibilities[39:80]) # 0.40-0.80 inclusive
    remaining = int((1-weight_gpa-0.1)*100)
    weight_score = random.choice(possibilities[9:remaining+2])
    remaining = int((1-weight_gpa-weight_score)*100)
    weight_year = random.choice(possibilities[:remaining+2])
    weight_experience = round(1-weight_gpa-weight_score-weight_year, 2)
    weightDict["gpa"] = weight_gpa
    weightDict["hackerrank_score"] = weight_score
    weightDict["class_year"] = weight_year
    weightDict["experience"] = weight_experience
    compWeightDict[comp] = weightDict
    
def pred_score_from_gpa(gpa):
    correctnessRatio = gpa/4.0
    if correctnessRatio > 0.95:
        correctnessRatio = 1.00
    else:
        correctnessRatio = round(correctnessRatio, 1)
    if random.randint(1,5) == 1:
        correctnessRatio -= 0.2
    elif random.randint(1,5) == 1 and correctnessRatio <= 0.8:
        correctnessRatio += 0.2
    if random.randint(1,20) == 1:
        correctnessRatio = 0.0
    return round(correctnessRatio, 2)
    
def applicantGoodness(app, weightDict):
    gpa = app.gpa
    hackerrank_score = app.hackerrank_score
    class_year = app.class_year
    experience = app.experience
    weight_gpa = weightDict["gpa"]
    weight_score = weightDict["hackerrank_score"]
    weight_year = weightDict["class_year"]
    weight_experience = weightDict["experience"]
    gpa_ratio = (gpa/4.0)*weight_gpa
    score_ratio = hackerrank_score * weight_score
    is_junior = 0
    if class_year == "junior":
        is_junior = 1
    year_ratio = is_junior * weight_year
    experience_ratio = experience * weight_experience
    return gpa_ratio + score_ratio + year_ratio + experience_ratio

minority = [0, 0, 0, 0, 1]
class_year_list = ["sophomore", "junior", "junior", "junior", "junior", "junior"]
applicants = []
with open(gpa_csv) as csvfile:
    table_reader = csv.reader(csvfile, delimiter=",")
    student_num = 0
    for row in table_reader:
        gpa = round(float(row[0]), 2)
        hackerrank_score = pred_score_from_gpa(gpa)
        minority_status = random.choice(minority)
        class_year = random.choice(class_year_list)
        experience = 0
        if class_year == "sophomore":
            if random.randint(1,5) == 1:
                experience = 1
        elif random.randint(1,10) != 1:
                experience = 1
        app = Applicant(student_num, gpa, hackerrank_score, minority_status, class_year, experience)
        applicants.append(app)
        student_num += 1

for comp in capacitiesDict.keys():
    goodnessDict = {}
    weightDict = compWeightDict[comp]
    desirability = random.choice([1,2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,7,7,7,8,8,8,9,9,10])
    desirabilityDict[comp] = desirability
    weight_gpa = weightDict["gpa"]
    weight_score = weightDict["hackerrank_score"]
    weight_year = weightDict["class_year"]
    weight_experience = weightDict["experience"]
    for app in applicants:
        number = app.number
        goodnessDict[number] = applicantGoodness(app, weightDict)
    apps = [app.number for app in applicants]
    apps.sort(key = lambda x : goodnessDict[x], reverse = True)
    employerPrefsDict[comp] = apps.copy()
    minorityReservesDict[comp] = int(capacitiesDict[comp] * random.randrange(5, 20)*0.01)

for app in applicants:
    applicant_prefs = []
    app_number = app.number
    is_minority = app.minority
    comps = [k for k in capacitiesDict.keys()]
    random.shuffle(comps)
    while comps != []:
        choice = None
        if random.randint(1, 4) == 1:
            choice = max(comps, key=lambda x : desirabilityDict[x])
        else:
            index = 0
            choice = comps[index]
            reachedEnd = False
            while desirabilityDict[choice] < 4:
                index += 1
                if index >= len(comps):
                    reachedEnd = True
                    break
                else:
                    choice = comps[index]
            if reachedEnd:
                choice = random.choice(comps)
        applicant_prefs.append(choice)
        comps.remove(choice)
    studentPrefsDict[app_number] = applicant_prefs.copy()
    isMinorityDict[app_number] = is_minority

with open(capacities_csv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for cap in capacitiesDict.keys():
        csvwriter.writerow([cap, capacitiesDict[cap]])

with open(students_csv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for stud in studentPrefsDict.keys():
        csvwriter.writerow([stud, studentPrefsDict[stud]])

with open(employers_csv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for comp in employerPrefsDict.keys():
        csvwriter.writerow([comp, employerPrefsDict[comp]])

with open(minorities_csv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for stud in isMinorityDict.keys():
        csvwriter.writerow([stud, isMinorityDict[stud]])

with open(minority_reserves_csv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for comp in minorityReservesDict.keys():
        csvwriter.writerow([comp, minorityReservesDict[comp]])

compWeightDictFile = open("dicts/compweightdict.pkl", "wb")
pickle.dump(compWeightDict, compWeightDictFile)
compWeightDictFile.close()

desirabilityDictFile = open("dicts/desirabilitydict.pkl", "wb")
pickle.dump(desirabilityDict, desirabilityDictFile)
desirabilityDictFile.close()