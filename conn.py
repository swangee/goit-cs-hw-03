import psycopg
from contextlib import contextmanager

database = './test.db'

@contextmanager
def create_connection(dsn = 'postgresql://postgres:12345@127.0.0.1/goit'):
    conn = psycopg.connect(dsn)
    yield conn
    conn.rollback()
    conn.close()
