import json
from ortools.sat.python import cp_model

def draw(examinators, students):


if __name__ == '__main__':
    with open('examinators.json', 'r') as fl:
        examinators = json.load(fl)

    with open('students.json', 'r') as fl:
        students = json.load(fl)
