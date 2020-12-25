import json

def load_exam_groups(path):
    print(path)
    with open(path, 'r') as fl:
        data = json.load(fl)

    result = set()
    for key in data:
        lst = data[key]
        if type(lst) is int:
            lst = [lst]

        for el in lst:
            assert el not in result

        result = result.union(lst)

    return result
