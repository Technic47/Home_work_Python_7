from xml.etree import ElementTree
import pandas
import csv
import datetime
import json
import UI


def create_new() -> str:
    """Create a new database"""
    now = datetime.datetime.now()
    now = now.strftime("%d%m%Y")
    name = f'/{now}.csv'
    path = data_path + name
    set_cols(path)
    with open(setup, 'w') as file:
        file.write(path)
    return path


def set_cols(path) -> None:
    """
    set names of cols in db from path
    :param path: db path
    """
    print("Enter your cols via space:")
    data = dict.fromkeys(UI.get_data().split(' '))
    print(data)
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(data)


def show_current() -> str:
    """shows current db from setup file"""
    with open(setup, 'r') as file:
        current_database = file.read()
    return current_database


def set_current(data) -> None:
    """change current db to data in setup file"""
    with open(setup, 'w') as file:
        file.write(data)


def get_info(path) -> None:
    """shows db path"""
    print(path)


def get_cols() -> []:
    """shows header of db"""
    with open(show_current(), 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        cols = reader.fieldnames
        return cols


def collect_data() -> []:
    """create line for insertion"""
    print(f"Enter new record:\n{get_cols()}")
    record = UI.get_data().replace(' ', '').replace(';', ',').replace('.', ',').replace(' ', '').split(',')
    print(record)
    return record


def save_data(data) -> {}:
    """adds line to current db"""
    cols = get_cols()
    with open(show_current(), 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=cols)
        writer.writerow({cols[0]: data[0], cols[1]: data[1], cols[2]: data[2]})
    return data


def show_base() -> None:
    """shows all records in current db"""
    rows = get_cols()
    print(rows)
    with open(show_current(), encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            print(f'{row[rows[0]]}, {row[rows[1]]}, {row[rows[2]]}')


def select_base(name: str) -> None:
    """selects db and place it to current position"""
    try:
        open(data_path + '/' + name + '.csv', 'r')
    except IOError:
        print('File not found!')
    else:
        data = data_path + '/' + name + '.csv'
        set_current(data)


def search():
    """Search function in current db"""
    global indexes
    indexes = []
    request = ''
    j = 0
    print("What key you want to search?")
    cols = get_cols()
    print(cols)
    key = UI.get_data()
    if key == '':
        print('Empty input')
    elif key not in cols:
        print('No match')
    else:
        for i in range(len(cols)):
            if key == cols[i]:
                print("Enter your request: ")
                request = UI.get_data()
                if request == '':
                    print('Empty input')
                else:
                    csvfile = csv.reader(open(show_current(), 'r'), delimiter=",")
                    for row in csvfile:
                        j += 1
                        if request in row[i]:
                            indexes.append(j)
                            print(j, row)
                    del_choose()
    return key, request


def del_choose() -> None:
    """support function. Allow to del positions after search"""
    print('Would you like to delete your request from db?')
    print('Y/N')
    answer = UI.get_data()
    if answer == 'Y' or answer == "y":
        print('All of them?')
        print('Y/N')
        answer2 = UI.get_data()
        if answer2 == 'Y' or answer2 == "y":
            delete(indexes)
        else:
            print('What positions would you like to delete?')
            show_indexed(indexes)
            numbers = list(map(int, UI.get_data().replace(' ', ',').replace(';', ',')
                               .replace('.', ',').split(',')))
            delete(numbers)
        print('Positions were deleted!')


def custom_delete():
    """user guide for removal choice"""
    print('Do you know positions for removal?')
    print('Y/N')
    answer = UI.get_data()
    if answer == 'Y' or answer == "y":
        print('What positions would you like to delete?')
        show_indexed(indexes)
        numbers = list(map(int, UI.get_data().replace(' ', ',').replace(';', ',')
                           .replace('.', ',').split(',')))
        show_indexed(numbers)
        print('Delete these positions?')
        print('Y/N')
        answer = UI.get_data()
        if answer == 'Y' or answer == "y":
            delete(numbers)
            print('Positions deleted.')
            return numbers
    elif answer == 'N' or answer == "n":
        print('Use "search" tool. It will help you to find positions.')
        return 'Nothing'
    else:
        return 'Nothing'


def show_indexed(numbers) -> None:
    """shows positions with dedicated numbers in current db"""
    j = 1
    with open(show_current(), encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            j += 1
            if j in numbers:
                print(j, row)


def delete(numbers) -> None:
    """removal procedure. Uses cached_base for re-writing current db"""
    j = 1
    with open(show_current(), 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        with open('cache/cached_base.csv', 'w', newline='') as cache_file:
            writer = csv.writer(cache_file, delimiter=",")
            for row in reader:
                if j not in numbers:
                    writer.writerow(row)
                j += 1
    with open(show_current(), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        with open('cache/cached_base.csv', 'r', encoding='utf-8') as cache_file:
            reader = csv.reader(cache_file, delimiter=",")
            for row in reader:
                writer.writerow(row)


def merge(path: str) -> None:
    """Merge selected db to current"""
    try:
        open(path)
    except FileNotFoundError:
        print('File not found!')
    else:
        cols = get_cols()
        with open(path, newline='') as csvfile:
            data = csv.DictReader(csvfile)
            with open(show_current(), 'a', newline='') as csvfile2:
                writer = csv.DictWriter(csvfile2, delimiter=",", fieldnames=cols)
                for row in data:
                    writer.writerow({cols[0]: row[cols[0]], cols[1]: row[cols[1]], cols[2]: row[cols[2]]})
        print('File merged to current db')


def export_json() -> None:
    """export current db to .json file"""
    json_array = []
    with open(show_current(), encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            json_array.append(row)
    print("Destination path:")
    json_path = UI.get_data() + '.json'
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        jsonstr = json.dumps(json_array, indent=4)
        jsonfile.write(jsonstr)


def import_json() -> None:
    """import json file to cache and allow to merge it to current db"""
    cols = get_cols()
    print("Destination path:")
    json_path = UI.get_data() + '.json'
    try:
        open(json_path)
    except FileNotFoundError:
        print('File not found!')
    else:
        with open(json_path, encoding='utf-8') as inputfile:
            df = pandas.read_json(inputfile)
        df.to_csv('cache/testfile.csv', encoding='utf-8', index=False)
        print("Would you like to merge imported data to current db?\nY/N")
        answer = UI.get_data()
        if answer == 'Y' or answer == 'y':
            with open('cache/testfile.csv', newline='') as csvfile:
                data = csv.DictReader(csvfile)
                with open(show_current(), 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=cols)
                    for row in data:
                        writer.writerow({cols[0]: row[cols[0]], cols[1]: row[cols[1]], cols[2]: row[cols[2]]})
            print('json file merged to current db')
        else:
            print('Imported file stored in: "cache/testfile.csv"')


def convert_xml(headers, row) -> str:
    """preparation for convertion to xml"""
    s = f'<row>\n'
    for header, item in zip(headers, row):
        s += f'    <{header}>' + f'{item}' + f'</{header}>\n'
    return s + '</row>'


def export_xml() -> None:
    """export current db to .xml file"""
    with open(show_current(), 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        xml = '<data>\n'
        for row in reader:
            xml += convert_xml(headers, row) + '\n'
        xml += '</data>'
    print("Destination path:")
    xml_path = UI.get_data() + '.xml'
    with open(xml_path, 'w', encoding='utf-8') as xmlfile:
        xmlfile.write(xml)


def import_xml() -> None:
    """import .xml file and save it to selected path"""
    cols = get_cols()
    rows = []
    print("Destination path:")
    xml_path = UI.get_data() + '.xml'
    try:
        open(xml_path)
    except FileNotFoundError:
        print('File not found!')
    else:
        tree = ElementTree.parse(xml_path)
        root = tree.getroot()
        header = get_cols()
        for i in root:
            col1 = i.find(str(header[0])).text
            col2 = i.find(str(header[1])).text
            col3 = i.find(str(header[2])).text

            rows.append({str(header[0]): col1,
                         str(header[1]): col2,
                         str(header[2]): col3})

        df = pandas.DataFrame(rows, columns=cols)
        df.to_csv('test.csv')


setup = 'setup.txt'
data_path = r'database'
indexes = []
setup = 'setup.txt'
