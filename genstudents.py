import json
import random
import argparse
from faker import Faker
from utils import exam_groups


def generate_students(n, output_path, input_path='examinators.json'):
    result = dict()
    fake = Faker(['ru_RU'])
    with open(input_path, 'r') as fl:
        examinators = json.load(fl)

    groups = exam_groups(examinators)
    for i in range(n):
        group = random.sample(groups, 1)[0]
        if group not in result:
            result[group] = list()

        result[group].append(fake.name())

    with open(output_path, 'w', encoding='utf8') as fl:
        json.dump(result, fl, indent=4, sort_keys=True, ensure_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--number-of-students",
        type=int,
        default=37,
        help="Number of dummy students.",
    )
    args = parser.parse_args()
    generate_students(args.number_of_students, 'students.json')
