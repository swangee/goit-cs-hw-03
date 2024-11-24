import faker
from random import randint

from conn import create_connection

NUMBER_USERS = 200
NUMBER_STATUSES = 3
NUMBER_TASKS = 200

def generate_fake_data(number_users, number_tasks) -> tuple():
    fake_users = []
    statuses = ['open', 'in progress', 'done']
    fake_tasks = []

    fake_data = faker.Faker()

    for _ in range(number_users):
        fake_users.append(fake_data.simple_profile())

    for _ in range(number_tasks):
        fake_tasks.append({"title": fake_data.sentence(), "desc": fake_data.text()})


    return fake_users, statuses, fake_tasks

def prepare_data(users, statuses, tasks) -> tuple():
    for_users = []# для таблиці employees

    for user in users:
        '''
        Для записів у таблицю співробітників нам потрібно додати посаду та id компанії. Компаній у нас було за замовчуванням
        NUMBER_COMPANIES, при створенні таблиці companies для поля id ми вказували INTEGER AUTOINCREMENT - тому кожен
        запис отримуватиме послідовне число збільшене на 1, починаючи з 1. Тому компанію вибираємо випадково
        у цьому діапазоні
        '''
        for_users.append((user["name"], user["mail"]))

    '''
   Подібні операції виконаємо й у таблиці payments виплати зарплат. Приймемо, що виплата зарплати у всіх компаніях
    виконувалася з 10 по 20 числа кожного місяця. Діапазон зарплат генеруватимемо від 1000 до 10000 у.о.
    для кожного місяця та кожного співробітника.
    '''
    for_tasks = []

    for task in tasks:
        '''
        Для записів у таблицю співробітників нам потрібно додати посаду та id компанії. Компаній у нас було за замовчуванням
        NUMBER_COMPANIES, при створенні таблиці companies для поля id ми вказували INTEGER AUTOINCREMENT - тому кожен
        запис отримуватиме послідовне число збільшене на 1, починаючи з 1. Тому компанію вибираємо випадково
        у цьому діапазоні
        '''
        for_tasks.append((task["title"], task["desc"], randint(1, len(statuses)), randint(1, len(users))))

    for_statuses = []
    for status in statuses:
        for_statuses.append((status,))


    return for_users, for_statuses, for_tasks

def insert_data_to_db(users, statuses, tasks) -> None:
    # Створимо з'єднання з нашою БД та отримаємо об'єкт курсора для маніпуляцій з даними

    with create_connection() as con:
        with con.cursor() as cur:
            '''Заповнюємо таблицю компаній. І створюємо скрипт для вставлення, де змінні, які вставлятимемо, помітимо
            знаком заповнювача (?) '''

            sql_to_users = """INSERT INTO users(fullname, email)
                                   VALUES (%s, %s)"""

            '''Для вставлення відразу всіх даних скористаємося методом executemany курсора. Першим параметром буде текст
            скрипту, а другим - дані (список кортежів).'''

            cur.executemany(sql_to_users, users)

            # Далі вставляємо дані про співробітників. Напишемо для нього скрипт і вкажемо змінні

            sql_to_status = """INSERT INTO status(name)
                                   VALUES (%s)"""

            # Дані були підготовлені заздалегідь, тому просто передаємо їх у функцію

            cur.executemany(sql_to_status, statuses)

            con.commit()

            # Останньою заповнюємо таблицю із зарплатами

            sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id)
                                  VALUES (%s, %s, %s, %s)"""

            # Вставляємо дані про зарплати

            cur.executemany(sql_to_tasks, tasks)

            # Фіксуємо наші зміни в БД

        con.commit()

if __name__ == "__main__":
    users, statuses, tasks = prepare_data(*generate_fake_data(NUMBER_USERS, NUMBER_TASKS))
    insert_data_to_db(users, statuses, tasks)