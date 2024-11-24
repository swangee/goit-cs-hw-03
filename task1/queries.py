from conn import create_connection


def main():
    with create_connection() as conn:
        with conn.cursor() as cur:
            # Отримати всі завдання певного користувача
            cur.execute('SELECT * FROM tasks WHERE user_id = %s', [50])
            print(cur.fetchall())

            # Вибрати завдання за певним статусом
            cur.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'open')")
            print(cur.fetchall())

            # Оновити статус конкретного завдання
            cur.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 50")

            # Отримати список користувачів, які не мають жодного завдання.
            cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")
            print(cur.fetchall())

            # Додати нове завдання для конкретного користувача.
            cur.execute("INSERT INTO users(fullname, email) VALUES(%s, %s)", ['some name', 'some@email.com'])
            conn.commit()

            # Знайти користувачів з певною електронною поштою.
            cur.execute("SELECT * FROM users WHERE email LIKE 'some%'")
            print(cur.fetchone())

            # Оновити ім'я користувача.
            cur.execute("UPDATE users SET fullname = 'some new name' WHERE email = 'some@email.com'")
            conn.commit()

            # Отримати кількість завдань для кожного статусу.
            cur.execute("SELECT COUNT(id) as count, (SELECT name FROM status WHERE id = status_id) as name FROM tasks GROUP BY status_id")
            print(cur.fetchall())

            # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
            # With subquery
            cur.execute("SELECT * FROM tasks WHERE user_id IN (SELECT DISTINCT id FROM users WHERE email LIKE '%@gmail.com')")
            print(cur.fetchall())

            # With join
            cur.execute("SELECT tasks.* FROM tasks JOIN users ON users.id = tasks.user_id WHERE users.email LIKE '%@gmail.com'")
            print(cur.fetchall())

            # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
            cur.execute("SELECT * FROM tasks WHERE description = ''")
            print(cur.fetchall())

            # Вибрати користувачів та їхні завдання, які є у статусі
            cur.execute("SELECT * FROM users JOIN tasks ON tasks.user_id = users.id AND tasks.status_id = (SELECT id FROM status WHERE name = %s)", ['in progress'])
            print(cur.fetchall())

            # Отримати користувачів та кількість їхніх завдань.
            cur.execute("SELECT users.*, COUNT(tasks.id) as tasks_count FROM users LEFT JOIN tasks ON tasks.user_id = users.id GROUP BY users.id")
            print(cur.fetchall())



if __name__ == '__main__':
    main()