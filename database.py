from xml.etree import ElementTree
import pandas
import csv
import datetime
import json
import UI

setup = 'setup.txt'
data_path = r'database'
with open(setup, 'r') as file:
    current_database = file.read()
# current_database = 'database/22092022.csv'
setup = 'setup.txt'

search_result = ''


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
    # cols = 'id ' + UI.get_data()
    # data = dict.fromkeys(cols.split(' '))
    data = dict.fromkeys(UI.get_data().split(' '))
    print(data)
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(data)


def get_info(path) -> None:
    """shows db path"""
    print(path)


def get_cols() -> []:
    """shows header of db"""
    with open(current_database, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = reader.fieldnames
        return rows


def collect_data() -> []:
    """create line for insertion"""
    print(f"Enter new record:\n{get_cols()}")
    record = input('').replace(';', ',').replace('.', ',').replace(' ', '').split(',')
    print(record)
    return record


def save_data(data) -> {}:
    """adds line to current db"""
    cols = get_cols()
    with open(current_database, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=cols)
        writer.writerow({cols[0]: data[0], cols[1]: data[1], cols[2]: data[2]})
    return data


def show_base() -> None:
    """shows all records in current db"""
    rows = get_cols()
    print(rows)
    with open(current_database, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            print(f'{row[rows[0]]}, {row[rows[1]]}, {row[rows[2]]}')


def select_base(name) -> None:
    """selects db and place it to current position"""
    # global current_database
    with open(setup, 'w') as file:
        file.write(data_path + '/' + name + '.csv')
    # current_database = data_path + '/' + name + '.csv'


def search():
    """Search function in current db"""
    global search_result
    search_result = ''
    print("What key you want to search?")
    cols = get_cols()
    print(cols)
    key = UI.get_data()
    for i in range(len(cols)):
        if key == cols[i]:
            print("Enter your request: ")
            request = UI.get_data()
            # request = 'Pavel'
            csvfile = csv.reader(open(current_database, 'r'), delimiter=",")
            for row in csvfile:
                # print(row)
                if request in row[i]:
                    print(row)
    return key, request


def merge(path: str) -> None:
    """Merge selected db to current"""
    cols = get_cols()
    with open(path, newline='') as csvfile:
        data = csv.DictReader(csvfile)
        with open(current_database, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=cols)
            for row in data:
                writer.writerow({cols[0]: row[cols[0]], cols[1]: row[cols[1]], cols[2]: row[cols[2]]})
    print('File merged to current db')


def export_json() -> None:
    """export current db to .json file"""
    json_array = []
    with open(current_database, encoding='utf-8') as csvfile:
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
    with open(json_path, encoding='utf-8') as inputfile:
        df = pandas.read_json(inputfile)
    df.to_csv('cache/testfile.csv', encoding='utf-8', index=False)
    print("Would you like to merge imported data to current db?\nY/N")
    answer = UI.get_data()
    if answer == 'Y' or answer == 'y':
        with open('cache/testfile.csv', newline='') as csvfile:
            data = csv.DictReader(csvfile)
            with open(current_database, 'a', newline='') as csvfile:
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
    with open(current_database, 'r') as csvfile:
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
