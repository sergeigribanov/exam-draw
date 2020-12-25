import json
import random
from faker import Faker
from utils import load_exam_groups


def generate_students(n, output_path, input_path='examinators.json'):
    result = dict()
    fake = Faker('ru_RU')
    groups = load_exam_groups(input_path)
    for i in range(n):
        group = random.sample(groups, 1)[0]
        if group not in result:
            result[group] = list()

        result[group].append(fake.name())

    with open(output_path, 'w', encoding='utf8') as fl:
        json.dump(result, fl, indent=4, sort_keys=True, ensure_ascii=False)

if __name__ == '__main__':
    generate_students(100, 'students.json')
