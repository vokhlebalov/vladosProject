import sys
from dicts import input_list, API_HH_dict
from utils import csv_reader, csv_filer, print_table, input_params

# vacancies_medium.csv
# Опыт работы: От 3 до 6 лет
# Оклад
# Нет
# 10 20
# Название, Навыки, Опыт работы, Компания
# Навыки: Git, Linux
# Навыки: Ремонт ПК, Настройка ПК
# Название, Навыки, Опыт работы, Премиум-вакансия, Компания, Оклад, Название региона, Дата публикации вакансии
# vacancies_big.csv
# Премиум-вакансия: Да
# Название
# Нет


try:
    input_data = input_params()
except ValueError as error:
    print(error)
    sys.exit()

file = input_data["file"]
filtration_param = input_data["filtration_param"]
sort_param = input_data["sort_param"]
reverse_sort = input_data["reverse_sort"]
rows_range = input_data["rows_range"]
columns = input_data["columns"]

vacancies = []
headers = []

if rows_range != '':
    vacancies.extend(list(map(int, rows_range.split(' '))))

if columns != '':
    headers = columns.split(', ')

header_row = csv_reader(file)[0]
header_rus = []

for cell in header_row:
    if cell in API_HH_dict:
        header_rus.append(API_HH_dict[cell])

print_table(
    csv_filer(
        header_row,
        csv_reader(file),
        header_rus
    ),
    vacancies,
    headers,
    filtration_param,
    sort_param, reverse_sort
)
