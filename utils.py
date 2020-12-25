import json

def exam_groups(examinators):
    result = set()
    for key in examinators["all"]:
        lst = examinators["all"][key]
        if type(lst) is int:
            lst = [lst]

        for el in lst:
            assert el not in result

        result = result.union(lst)

    return result

def consistency_check(examinators, students):
    sgroups = set(map(int, students.keys()))
    egroups = exam_groups(examinators)
    return sgroups.issubset(egroups)

def result_check(result):
    for ename in result:
        groups = result[ename]['groups']
        if type(groups) is int:
            groups = [groups]

        for sname, group in result[ename]['students']:
            if group in groups:
                flag = False
                print('[!!!] Warning: the examinator {} and the {} have the same groups.'.format(ename, sname))
