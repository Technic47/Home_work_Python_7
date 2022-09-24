import csv
import datetime
import json
import UI

data_path = r'database'
current_database = 'database/22092022.csv'
#

search_result = ''


def create_new() -> str:
    """Create a new database"""
    now = datetime.datetime.now()
    now = now.strftime("%d%m%Y")
    name = f'/{now}.csv'
    path = data_path + name
    set_cols(path)
    return path


def set_cols(path) -> None:
    """
    set names of cols in db from path
    :param path: db path
    """
    print("Enter your cols via space:")
    #cols = 'id ' + UI.get_data()
    #data = dict.fromkeys(cols.split(' '))
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
    #global id
    #print(id)
    #id += 1
    print(f"Enter new record:\n{get_cols()}")
    record = input('').replace(';', ',').replace('.', ',').replace(' ', '').split(',')
    #record.insert(0, id)
    print(record)
    return record


def save_data(data) -> {}:
    """adds line to db"""
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
    global current_database
    current_database = data_path + '/' + name + '.csv'


def search():
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


def export_json():
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
