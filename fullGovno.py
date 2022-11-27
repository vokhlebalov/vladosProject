import sys

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

input_list = [
    'Название',
    'Описание',
    'Навыки',
    'Опыт работы',
    'Премиум-вакансия',
    'Компания',
    'Оклад',
    'Название региона',
    'Дата публикации вакансии',
    'Нижняя граница вилки оклада',
    'Верхняя граница вилки оклада',
    'Идентификатор валюты оклада',
    'Оклад указан до вычета налогов'
]

API_HH_dict = {
    'name': 'Название',
    'description': 'Описание',
    'key_skills': 'Навыки',
    'experience_id': 'Опыт работы',
    'premium': 'Премиум-вакансия',
    'employer_name': 'Компания',
    'salary_from': 'Нижняя граница вилки оклада',
    'salary_to': 'Верхняя граница вилки оклада',
    'salary_gross': 'Оклад указан до вычета налогов',
    'salary_currency': 'Идентификатор валюты оклада',
    'salary': 'Оклад',
    'area_name': 'Название региона',
    'published_at': 'Дата публикации вакансии'
}

experience_of_work = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"
}

currency = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум"
}

currency_to_rub = {
    "Манаты": 35.68,
    "Белорусские рубли": 23.91,
    "Евро": 59.90,
    "Грузинский лари": 21.74,
    "Киргизский сом": 0.76,
    "Тенге": 0.13,
    "Рубли": 1,
    "Гривны": 1.64,
    "Доллары": 60.66,
    "Узбекский сум": 0.0055,
}


def filtration(param, f_row):
    if param != 'incorrect':
        if param[0] in input_list and param[0] != 'Навыки' and param[0] != 'Оклад':
            if param[0] in f_row.keys() and f_row[param[0]] == param[1]:
                return f_row

        elif param[0] == 'Навыки':
            flag = True
            if param[0] in f_row.keys():
                form_value = f_row[param[0]].replace('ECALPER', ', ').split(', ')
                flag = all(item in form_value for item in param[1])

            if flag:
                return f_row

        elif param[0] == 'Оклад':
            if int(f_row['Нижняя граница вилки оклада']) <= int(param[1]) <= int(
                    f_row['Верхняя граница вилки оклада']):
                return f_row
    else:
        return f_row


def sorter(data, param, r_s):
    from operator import itemgetter

    if r_s == 'Да':
        r_s = True
    else:
        r_s = False
    if param == 'Оклад':
        newlist = sorted(data, key=itemgetter('Зарплата в рублях'), reverse=r_s)
    elif param == 'Навыки':
        newlist = sorted(data, key=itemgetter('Количество навыков'), reverse=r_s)
    elif param == 'Опыт работы':
        newlist = sorted(data, key=itemgetter('Индекс опыта работы'), reverse=r_s)
    elif param == 'Дата публикации вакансии':
        newlist = sorted(data, key=itemgetter('Дата и время'), reverse=r_s)
    else:
        newlist = sorted(data, key=itemgetter(param), reverse=r_s)
    return newlist


def formatter(row):
    import re
    import math
    from datetime import datetime

    formatted_row = {}

    for key, value in row.items():
        formatted_value = value
        if value == 'True' or value == 'False':
            formatted_value = re.sub(r'True', 'Да', value)
            formatted_value = re.sub(r'False', 'Нет', value)
        if value in experience_of_work:
            formatted_value = experience_of_work[value]
        if value in currency:
            formatted_value = currency[value]
        if key == 'Оклад указан до вычета налогов':
            formatted_value = 'С вычетом налогов' if formatted_value == 'Нет' else 'Без вычета налогов'
        if key == 'Дата публикации вакансии':
            date = datetime.strptime(value[:10], '%Y-%m-%d')
            formatted_value = str(date.strftime('%d.%m.%Y'))
        if key == 'Премиум-вакансия':
            if value == 'True':
                formatted_value = 'Да'
            elif value == 'False':
                formatted_value = 'Нет'
        formatted_row[key] = formatted_value

    salary = f'{math.trunc(float(formatted_row["Нижняя граница вилки оклада"])):,} - {math.trunc(float(formatted_row["Верхняя граница вилки оклада"])):,} ({formatted_row["Идентификатор валюты оклада"]}) ({formatted_row["Оклад указан до вычета налогов"]})'.replace(
        ',', ' ')
    lowsalary = math.trunc(float(formatted_row["Нижняя граница вилки оклада"]))
    highsalary = math.trunc(float(formatted_row["Верхняя граница вилки оклада"]))

    for keys, values in currency_to_rub.items():
        if keys in salary:
            salary_in_rub = (int(lowsalary) + int(highsalary)) / 2 * values

    splitted_row = formatted_row['Навыки'].split('ECALPER')

    exp_index = 0
    if formatted_row['Опыт работы'] == 'Нет опыта':
        exp_index = 0
    elif formatted_row['Опыт работы'] == 'От 1 года до 3 лет':
        exp_index = 1
    elif formatted_row['Опыт работы'] == 'От 3 до 6 лет':
        exp_index = 2
    elif formatted_row['Опыт работы'] == 'Более 6 лет':
        exp_index = 3

    buf_row = {
        'Название': formatted_row['Название'],
        'Описание': formatted_row['Описание'],
        'Навыки': formatted_row['Навыки'],
        'Опыт работы': formatted_row['Опыт работы'],
        'Премиум-вакансия': formatted_row['Премиум-вакансия'],
        'Компания': formatted_row['Компания'],
        'Оклад': salary,
        'Название региона': formatted_row['Название региона'],
        'Дата публикации вакансии': formatted_row['Дата публикации вакансии'],
        'Нижняя граница вилки оклада': row['Нижняя граница вилки оклада'],
        'Верхняя граница вилки оклада': row['Верхняя граница вилки оклада'],
        'Идентификатор валюты оклада': formatted_row['Идентификатор валюты оклада'],
        'Оклад указан до вычета налогов': formatted_row['Оклад указан до вычета налогов'],
        'Зарплата в рублях': salary_in_rub,
        'Количество навыков': len(splitted_row),
        'Индекс опыта работы': exp_index,
        'Дата и время': row['Дата публикации вакансии']
    }
    return buf_row


def csv_reader(file_name):
    import csv
    text = []
    with open(file_name, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            text.append(row)
        if len(text) == 0:
            print('Пустой файл')
            sys.exit()
        else:
            return text


def csv_filer(header, reader, list_naming):
    import re

    list_of_lists = []
    vacancy_list = []
    list_of_dicts = []

    for i in reader:
        flag = True
        for j in i:
            if len(i) != len(header) or j == '':
                flag = False
        if flag is True:
            list_of_lists.append(i)

    for row in list_of_lists:
        vacancy_row = []
        for line in row:
            line = re.sub(r'<[^>]*>', '', line)
            line = line.replace('\n', 'ECALPER')
            line = str.strip(re.sub(r'\s+', ' ', line))
            vacancy_row.append(line)
        vacancy_list.append(vacancy_row)

    for i in vacancy_list:
        vacancy_dict = dict(zip(list_naming, i))
        list_of_dicts.append(vacancy_dict)

    return list_of_dicts


def print_table(data_vacancies, data_lines, data_columns, f_param, s_param, rev_sort):
    from prettytable import PrettyTable, ALL

    vacancies_table = PrettyTable()
    vacancies_table.field_names = [
        '№',
        'Название',
        'Описание',
        'Навыки',
        'Опыт работы',
        'Премиум-вакансия',
        'Компания',
        'Оклад',
        'Название региона',
        'Дата публикации вакансии',
        'Нижняя граница вилки оклада',
        'Верхняя граница вилки оклада',
        'Идентификатор валюты оклада',
        'Оклад указан до вычета налогов',
        'Зарплата в рублях',
        'Количество навыков',
        'Индекс опыта работы',
        'Дата и время'
    ]

    list_of_tablelists = []
    list_of_dicts = []
    number = 1

    for vacancy in data_vacancies[1:]:
        table_list = []
        result_row = {}
        row = formatter(vacancy)
        if f_param != 'incorrect':
            if filtration(f_param, row) is None:
                continue
            result_row = filtration(f_param, row)
        elif f_param == 'incorrect':
            result_row = row
        for key, value in result_row.items():
            formatted_value = ''
            if key == 'Навыки':
                splitted_value = value.replace('ECALPER', '\n')
                for i in splitted_value:
                    formatted_value += i
                result_row['Навыки'] = formatted_value
        if s_param == '':
            for i in result_row.values():
                if isinstance(i, str):
                    if len(i) > 100:
                        string = i[0:100] + '...'
                        table_list.append(string.strip())
                    else:
                        table_list.append(i.strip())
                else:
                    table_list.append(i)
            table_list.insert(0, number)
            list_of_tablelists.append(table_list)
            number += 1
        else:
            list_of_dicts.append(result_row)
    list_of_dicts = sorter(list_of_dicts, s_param, rev_sort)
    for i in list_of_dicts:
        table_list1 = []
        for j in i.values():
            if isinstance(j, str):
                if len(j) > 100:
                    string = j[0:100] + '...'
                    table_list1.append(string.strip())
                else:
                    table_list1.append(j.strip())
            else:
                table_list1.append(j)
        table_list1.insert(0, number)
        list_of_tablelists.append(table_list1)
        number += 1
    data_columns.insert(0, '№')
    vacancies_table.add_rows(list_of_tablelists)
    vacancies_table.align = 'l'
    vacancies_table._max_width = {'№': 20, 'Название': 20, 'Описание': 20, 'Навыки': 20, 'Опыт работы': 20,
                                  'Премиум-вакансия': 20, 'Компания': 20, 'Оклад': 20, 'Название региона': 20,
                                  'Дата публикации вакансии': 20}
    vacancies_table.del_column('Нижняя граница вилки оклада')
    vacancies_table.del_column('Верхняя граница вилки оклада')
    vacancies_table.del_column('Идентификатор валюты оклада')
    vacancies_table.del_column('Оклад указан до вычета налогов')
    vacancies_table.del_column('Зарплата в рублях')
    vacancies_table.del_column('Количество навыков')
    vacancies_table.del_column('Индекс опыта работы')
    vacancies_table.del_column('Дата и время')
    vacancies_table.hrules = ALL
    if list_of_tablelists == [] and f_param == 'incorrect':
        print('Нет данных')
    elif list_of_tablelists == [] and f_param != 'incorrect':
        print('Ничего не найдено')
    else:
        if data_lines == [] and data_columns != ['№']:
            print(vacancies_table.get_string(fields=data_columns))
        elif data_columns == ['№'] and data_lines != []:
            if len(data_lines) != 1:
                print(vacancies_table.get_string(start=data_lines[0] - 1, end=(data_lines[1] - 1)))
            else:
                print(vacancies_table.get_string(start=data_lines[0] - 1))
        elif data_columns != ['№'] and data_lines != []:
            if len(data_lines) != 1:
                print(vacancies_table.get_string(start=data_lines[0] - 1, end=(data_lines[1] - 1), fields=data_columns))
            else:
                print(vacancies_table.get_string(start=data_lines[0] - 1, fields=data_columns))
        elif data_lines == [] and data_columns == ['№']:
            print(vacancies_table)


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

print_table(csv_filer(header, csv_reader(file), header_rus), vacancies, headers, filtration_param, sort_param,
            reverse_sort)
