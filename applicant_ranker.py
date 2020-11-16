import csv
import os
import json
import statistics 



class Applicant:
    def __init__(self, name, gpa):
        self.gpa = gpa
        self.name = name
        self.
    
joe = Applicant('Joe', 3.6)
jim = Applicant('Jim', 3.4)
john = Applicant('John', 3.1)
jing = Applicant('Jing', 4.0)
applicants = [joe, jim, john, jing]


def rank_by_gpa(applicant_list, gpa_cutoff):
    ranked_applicants = []
    filtered_applicants = []
    gpa_list = []
    for app in applicant_list:
        if app.gpa >= gpa_cutoff:
            filtered_applicants.append(app)
            gpa_list.append(app.gpa)

    gpa_list.sort()
    for gpa in gpa_list:
        for applicant in filtered_applicants:
            if applicant.gpa == gpa:
                ranked_applicants.append(applicant)
    return ranked_applicants
            
    
ranked = rank_by_gpa(applicants, 3.2)
            


def bubble_sort(applicant_list):
    n = len(applicant_list) 
    for i in range(n): 
        swapped = False
        for applicant in range(0, n-i-1): 
            print(applicant_list[applicant].gpa)
            if applicant_list[applicant].gpa > applicant_list[applicant+1].gpa:
                applicant_list[applicant] = applicant_list[applicant+1]
                applicant_list[applicant+1] = applicant_list[applicant]
                swapped = True
  
        # IF no two elements were swapped 
        # by inner loop, then break 
        if swapped == False: 
            break
    return applicant_list