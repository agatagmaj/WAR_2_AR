from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def get_connection():
    cnx = connect(user="postgres", password="coderslab",
                  host="localhost", database="ar_db")
    cnx.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return cnx
