from dicts import input_list, experience_of_work, currency, currency_to_rub, print_columns, width_settings
import sys
import re


def input_params():
    input_dict = {
        "file": input('Введите название файла: '),
        "filtration_param": input('Введите параметр фильтрации: '),
        "sort_param": input('Введите параметр сортировки: '),
        "reverse_sort": input('Обратный порядок сортировки (Да / Нет): '),
        "rows_range": input('Введите диапазон вывода: '),
        "columns": input('Введите требуемые столбцы: ')
    }

    if len(input_dict["filtration_param"]) > 0 and ': ' not in input_dict["filtration_param"]:
        raise ValueError('Формат ввода некорректен')

    if input_dict["sort_param"] not in input_list and input_dict["sort_param"] != '':
        raise ValueError('Параметр сортировки некорректен')

    if input_dict["reverse_sort"] not in ['Да', 'Нет'] and input_dict["reverse_sort"] != '':
        raise ValueError('Порядок сортировки задан некорректно')

    filers_set = list(filter(None, input_dict["filtration_param"].split(': ')))

    if len(filers_set) == 0:
        return input_dict

    if filers_set[0] == 'Навыки':
        filers_set[1] = filers_set[1].split(', ')

    if filers_set[0] not in input_list:
        raise ValueError('Параметр поиска некорректен')

    input_dict["filtration_param"] = filers_set

    return input_dict


def filtration(param, f_row):
    if len(param) > 0:
        if param[0] == 'Навыки':
            form_value = f_row[param[0]].replace('ECALPER', ', ').split(', ')
            if all(item in form_value for item in param[1]):
                return f_row

        elif param[0] == 'Оклад':
            if int(f_row['Нижняя граница вилки оклада']) <= int(param[1]) <= int(
                    f_row['Верхняя граница вилки оклада']):
                return f_row

        elif param[0] in input_list:
            if f_row[param[0]] == param[1]:
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
    low_salary = math.trunc(float(formatted_row["Нижняя граница вилки оклада"]))
    high_salary = math.trunc(float(formatted_row["Верхняя граница вилки оклада"]))

    for keys, values in currency_to_rub.items():
        if keys in salary:
            salary_in_rub = (int(low_salary) + int(high_salary)) / 2 * values

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

    formatted_data = format_raw_data(remove_empty_data(reader, len(header)))
    result_data = []

    for row in formatted_data:
        vacancy_dict = dict(zip(list_naming, row))
        result_data.append(vacancy_dict)

    return result_data


def format_raw_data(data):
    formatted_data = []

    for row in data:
        vacancy_row = []

        for line in row:
            line = re.sub(r'<[^>]*>', '', line)
            line = line.replace('\n', 'ECALPER')
            line = str.strip(re.sub(r'\s+', ' ', line))
            vacancy_row.append(line)

        formatted_data.append(vacancy_row)

    return formatted_data


def remove_empty_data(data, table_length):
    cleared_data = []

    for row in data:
        flag = True

        for cell in row:
            if len(row) != table_length or cell == '':
                flag = False

        if flag is True:
            cleared_data.append(row)

    return cleared_data


def print_table(data_vacancies, data_lines, data_columns, f_param, s_param, rev_sort):
    from prettytable import PrettyTable, ALL

    vacancies_table = PrettyTable()
    vacancies_table.field_names = print_columns
    list_of_tablelists = []
    list_of_dicts = []
    number = 1

    for vacancy in data_vacancies[1:]:
        table_list = []
        result_row = {}
        row = formatter(vacancy)

        if len(f_param) > 0:
            if filtration(f_param, row) is None:
                continue
            result_row = filtration(f_param, row)
        elif len(f_param) == 0:
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
    vacancies_table._max_width = width_settings

    vacancies_table.del_column('Нижняя граница вилки оклада')
    vacancies_table.del_column('Верхняя граница вилки оклада')
    vacancies_table.del_column('Идентификатор валюты оклада')
    vacancies_table.del_column('Оклад указан до вычета налогов')
    vacancies_table.del_column('Зарплата в рублях')
    vacancies_table.del_column('Количество навыков')
    vacancies_table.del_column('Индекс опыта работы')
    vacancies_table.del_column('Дата и время')
    vacancies_table.hrules = ALL

    if len(list_of_tablelists) == 0 and len(f_param) == 0:
        print('Нет данных')
    elif len(list_of_tablelists) == 0 and len(f_param) > 0:
        print('Ничего не найдено')
    else:
        if len(data_lines) == 0 and data_columns != ['№']:
            print(vacancies_table.get_string(fields=data_columns))
        elif data_columns == ['№'] and len(data_lines) > 0:
            if len(data_lines) > 1:
                print(vacancies_table.get_string(start=data_lines[0] - 1, end=(data_lines[1] - 1)))
            else:
                print(vacancies_table.get_string(start=data_lines[0] - 1))
        elif data_columns != ['№'] and len(data_lines) > 0:
            if len(data_lines) > 1:
                print(vacancies_table.get_string(start=data_lines[0] - 1, end=(data_lines[1] - 1), fields=data_columns))
            else:
                print(vacancies_table.get_string(start=data_lines[0] - 1, fields=data_columns))
        elif len(data_lines) == 0 and data_columns == ['№']:
            print(vacancies_table)
