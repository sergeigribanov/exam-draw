import json
import itertools
from utils import consistency_check
from ortools.sat.python import cp_model


def student_uniqueness_constraints(model, exams, examinators, students):
    elist = examinators["exam"]
    slist = list(itertools.chain(*students.values()))
    for sname in slist:
        model.Add(sum(exams[(ename, sname)] for ename in elist) == 1)

def exclusion_constraints(model, exams, examinators, students):
    elist = examinators["exam"]
    slist = list(itertools.chain(*students.values()))
    sgroups = set(map(int, itertools.chain(*students.keys())))

    for ename in elist:
        if ename not in examinators["all"]:
            print('[!] Skipping exclusion constraint: examinator {} not in "all" list.'.format(ename))
            continue

        groups = examinators["all"][ename]
        if type(groups) is int:
            groups = [groups]

        groups = set(groups)
        groups = groups.intersection(sgroups)

        eslist = list(itertools.chain(*[students[str(group)] for group in groups]))
        for sname in eslist:
            key = (ename, sname)
            model.Add(exams[key] == 0)

def uniformity_constraints(model, exams, examinators, students, penalty):
    elist = examinators["exam"]
    slist = list(itertools.chain(*students.values()))
    for ename in elist:
        model.Add(penalty[0] - sum(exams[(ename, sname)] for sname in slist) <= 0)
        model.Add(penalty[1] - sum(exams[(ename, sname)] for sname in slist) >= 0)

def create_result_dict(solver, exams, examinators, students):
    result = dict()
    elist = examinators["exam"]
    slist = list(itertools.chain(*students.values()))
    for ename in elist:
        result[ename] = list()
        for sname in slist:
            key = (ename, sname)
            if solver.Value(exams[key]) == 1:
                result[ename].append(sname)

    return result

def print_result_dict(result):
    for ename in result:
        print('\n--------')
        print('{}:\n'.format(ename))
        for sname in result[ename]:
            print(sname)

def draw(examinators, students):
    model = cp_model.CpModel()
    elist = examinators["exam"]
    slist = list(itertools.chain(*students.values()))
    exams = dict()
    # Создание переменных для описания мин / макс загруженности экзаменаторов
    lpenalty =  model.NewIntVar(0, len(slist), 'lower_penalty')
    upenalty = model.NewIntVar(0, len(slist), 'upper_penalty')
    # Создание булевых переменных (таблица соотвествия {экзаменатор : студент})
    for ename in elist:
        for sname in slist:
            key = (ename, sname)
            exams[key] = model.NewBoolVar('shift_{}_{}'.format(*key))

    # Констрейны: каждому студенту соответствует только один экзаменатор
    student_uniqueness_constraints(model, exams, examinators, students)
    # Констрейны: экзаменаторы не могут принимать экзамен у студетов из своих групп
    exclusion_constraints(model, exams, examinators, students)
    # Констрейны: наименьшее и набольшее количество студетов на экзаменатора
    uniformity_constraints(model, exams, examinators, students, [lpenalty, upenalty])
    # Требуем, чтобы разница между наибольшим и наименьши количеством студетов
    # на экзаменатора была минимаоьной
    model.Minimize(upenalty - lpenalty)
    solver = cp_model.CpSolver()
    # Лимит максимального времени в сек.
    solver.parameters.max_time_in_seconds = 10.0
    # Поиск решения
    solver.Solve(model)
    # Получение результата
    result = create_result_dict(solver, exams, examinators, students)
    # Сохранение результата в файл
    with open('result.json', 'w', encoding='utf8') as fl:
        json.dump(result, fl, indent=4, sort_keys=True, ensure_ascii=False)

    # Печать результата
    # print_result_dict(result)

if __name__ == '__main__':
    with open('examinators.json', 'r') as fl:
        examinators = json.load(fl)

    with open('students.json', 'r') as fl:
        students = json.load(fl)

    assert consistency_check(examinators, students)
    draw(examinators, students)
