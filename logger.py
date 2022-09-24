import datetime
import database

logs_path = r'logs'
current_log = ''
now = datetime.datetime.now()
now = now.strftime("%d%m%Y_%H%M%S")


def start_logger():
    global current_log
    name = f'/{now}.txt'
    path = logs_path + name
    with open(path, 'w') as text:
        text.write(
            f"Current database - {database.current_database}\n"
            f"{now} - session started;\n")
    print(f'Logger started. Current log - {name}')
    current_log = path
    return path


def log(data, action: str):
    with open(current_log, 'a') as text:
        text.write('{0} - {1} {2};'.format(now, data, action) + '\n')
    return data


def clear():
    with open(current_log, 'w') as text:
        text.write(f'{now} - session cleared')
    print('Current log cleared')


def stop_logger():
    with open(current_log, 'a') as text:
        text.write(f"{now} - session closed;")
    print('Logger stopped.')
