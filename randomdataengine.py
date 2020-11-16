import csv, random

# FILEPATHS - change these for your own directories
table_csv = "table.csv"
capacities_csv = "capacities.csv"
students_csv = "students.csv"
employers_csv = "employers.csv"
minorities_csv = "minorities.csv"
minority_reserves_csv = "minority_reserves.csv"
# FILEPATHS - change these for your own directories

def sumDict(dict1):
    sum = 0
    for val in dict1.values():
        sum += val
    return sum

companies = []
with open(table_csv) as csvfile:
    table_reader = csv.reader(csvfile, delimiter=",")
    for row in table_reader:
        if row[0] == 'rank':
            continue
        companies.append(row[1])


fortune_50 = companies[0:50]

capacitiesDict = {}

for comp in fortune_50:
    capacitiesDict[comp] = random.randrange(50,100)

sum = sumDict(capacitiesDict)

students = [i for i in range(sum)]

studentPrefsDict = {}
employerPrefsDict = {}
isMinorityDict = {}
minorityReservesDict = {}

for comp in capacitiesDict.keys():
    minorityReservesDict[comp] = int(capacitiesDict[comp] * random.randrange(5, 20)*0.01)

minority = [0, 0, 0, 0, 1]

for stud in students:
    fort5 = [c for c in fortune_50]
    random.shuffle(fort5)
    studentPrefsDict[stud] = fort5

for comp in fortune_50:
    studs = [n for n in students]
    random.shuffle(studs)
    employerPrefsDict[comp] = studs

for stud in students:
    isMinorityDict[stud] = random.choice(minority)

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

print("DONE!!!")