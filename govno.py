import sys
from dicts import input_list, API_HH_dict
from utils import csv_reader, csv_filer, print_table

# vacancies_medium.csv
# Опыт работы: От 3 до 6 лет
# Оклад
# Нет
# 10 20
# Название, Навыки, Опыт работы, Компания
# Навыки: Git, Linux
# Навыки: Ремонт ПК, Настройка ПК
# Название, Навыки, Опыт работы, Премиум-вакансия, Компания, Оклад, Название региона, Дата публикации вакансии

file = input('Введите название файла: ')
filtration_param = input('Введите параметр фильтрации: ')
sort_param = input('Введите параметр сортировки: ')
reverse_sort = input('Обратный порядок сортировки (Да / Нет): ')
lines = input('Введите диапазон вывода: ')
columns = input('Введите требуемые столбцы: ')

if ':' not in filtration_param and filtration_param != '':
    print('Формат ввода некорректен')
    sys.exit()
if ':' in filtration_param:
    filtration_param = filtration_param.split(': ')

if filtration_param == '':
    filtration_param = 'incorrect'
if filtration_param[0] == 'Навыки':
    filtration_param[1] = filtration_param[1].split(', ')

if filtration_param[0] not in input_list and filtration_param != 'incorrect':
    print('Параметр поиска некорректен')
    sys.exit()
if sort_param not in input_list and sort_param != '':
    print('Параметр сортировки некорректен')
    sys.exit()
if (reverse_sort != 'Да' and reverse_sort != 'Нет') and reverse_sort != '':
    print('Порядок сортировки задан некорректно')
    sys.exit()

vacancies = []
headers = []
if lines != '':
    for i in lines.split(' '):
        vacancies.append(int(i))
if columns != '':
    headers = columns.split(', ')

header = csv_reader(file)[0]
header_rus = []
for words in header:
    for keys, values in API_HH_dict.items():
        if words == keys:
            header_rus.append(values)


print_table(csv_filer(header, csv_reader(file), header_rus), vacancies, headers, filtration_param, sort_param, reverse_sort)
