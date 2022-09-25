import logger
import database
import os


def start():
    print('System started')
    logger.start_logger()
    while True:
        match input('Enter command: '):
            case 'exit':
                logger.stop_logger()
                quit()
            case 'help':
                print('READ_ME file may help you.')
            case 'new':
                database1 = logger.log(database.create_new(), 'create')
                print(f'New database created: {database1}')
                print("Switch to current database?")
                answer = input('Y/N: ')
                if answer == 'Y' or answer == 'y' or answer == 'yes':
                    database.current_database = database1
                    logger.log(database.current_database, 'set as current')
            case 'show dir':
                dirname = 'database'
                for filename in os.listdir(dirname):
                    print(filename)
                logger.log('databases', 'shown')
            case 'show current':
                print(database.current_database)
                logger.log('current_database', 'shown')
            case 'add':
                logger.log(database.save_data(database.collect_data()), 'added')
            case 'show base':
                database.show_base()
                logger.log('current database', 'shown')
            case 'select':
                name = input("Enter name of database: ")
                database.select_base(name)
                logger.log(name, 'selected')
                logger.log(database.current_database, ' set as current')
            case 'export json':
                database.export_json()
                logger.log('current database', 'exported as .json')
            case 'export xml':
                database.export_xml()
                logger.log('current database', 'exported as .xml')
            case 'import xml':
                database.import_xml()
                logger.log('xmlfile', 'imported')
            case 'import json':
                database.import_json()
                logger.log('jsonfile', 'imported')
            case 'search':
                logger.log(database.search(), 'searched')
            case 'clear log':
                logger.clear()
