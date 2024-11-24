from conn import create_connection

def create_db():
    with open('init.sql', 'r') as f:
        sql = f.read()

    with create_connection() as con:
        # Open a cursor to perform database operations
        with con.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute(sql)

        con.commit()

if __name__ == "__main__":
    create_db()