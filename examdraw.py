import json
import itertools
from utils import consistency_check
from ortools.sat.python import cp_model

def draw(examinators, students):
    model = cp_model.CpModel()
    elist = list(examinators.keys())
    slist = list(itertools.chain(*students.values()))
    exams = dict()
    lpenalty =  model.NewIntVar(0, len(slist), 'lower_penalty')
    upenalty = model.NewIntVar(0, len(slist), 'upper_penalty')
    # Создание булевых переменных (таблица соотвествия {экзаменатор : студент})
    for ename in elist:
        for sname in slist:
            key = (ename, sname)
            exams[key] = model.NewBoolVar('shift_{}_{}'.format(*key))

    # Констрейны: каждому студенту соответствует только один экзаменатор
    for sname in slist:
        model.Add(sum(exams[(ename, sname)] for ename in elist) == 1)

    # Констрейны: экзаменаторы не могут принимать экзамен у студетов из своих групп
    sgroups = set(map(int, itertools.chain(*students.keys())))
    for ename in elist:
        groups = examinators[ename]
        if type(groups) is int:
            groups = [groups]

        groups = set(groups)
        groups = groups.intersection(sgroups)

        eslist = list(itertools.chain(*[students[str(group)] for group in groups]))
        for sname in eslist:
            key = (ename, sname)
            model.Add(exams[key] == 0)

    # Констрейны: наименьшее и набольшее количество студетов на экзаменатора
    for ename in elist:
        model.Add(lpenalty - sum(exams[(ename, sname)] for sname in slist) <= 0)
        model.Add(upenalty - sum(exams[(ename, sname)] for sname in slist) >= 0)


    # Требуем, чтобы разница между наибольшим и наименьши количеством студетов
    # на экзаменатора была минимаоьной
    model.Minimize(upenalty - lpenalty)

    solver = cp_model.CpSolver()
    solver.Solve(model)

    for ename in elist:
        print('-----')
        print(ename + ":")
        for sname in slist:
            key = (ename, sname)
            if solver.Value(exams[key]) == 1:
                print(sname)

if __name__ == '__main__':
    with open('examinators.json', 'r') as fl:
        examinators = json.load(fl)

    with open('students.json', 'r') as fl:
        students = json.load(fl)

    assert consistency_check(examinators, students)
    draw(examinators, students)
