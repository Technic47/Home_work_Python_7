import database
import os


def start():
    while True:
        match input('Enter command: '):
            case 'exit':
                quit()
            case 'new':
                database1 = database.create_new()
                print(f'New database created: {database1}')
                print("Switch to current database?")
                answer = input('Y/N: ')
                if answer == 'Y' or answer == 'y' or answer == 'yes':
                    database.current_database = database1
            case 'show dir':
                dirname = 'database'
                for filename in os.listdir(dirname):
                    print(filename)
            case 'show current':
                print(database.current_database)
            case 'add':
                database.save_data(database.collect_data())
            case 'show base':
                database.show_base()
            case 'select':
                name = input("Enter name of database: ")
                database.select_base(name)
            case 'export':
                database.export_json()
            case 'search':
                database.search()
