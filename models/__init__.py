from Modul_2.WAR_2_AR.clcrypto import password_hash, generate_salt
from Modul_2.WAR_2_AR.get_connection import get_connection


class Users(object):
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password, salt):
        self.__hashed_password = password_hash(password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = f"""INSERT INTO Users(username, email, hashed_password)
            VALUES('{self.username}', '{self.email}', '{self.hashed_password}') RETURNING id"""
           # values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql)#, values)
            self.__id = cursor.fetchone()[0]  # albo cursor.fetchone()['id']
            return True
        return False


agata = Users()
agata.username = "agafija"
agata.email = "aga@onet.pl"
agata.set_password("Helenk@", generate_salt())

cnx = get_connection()
cursor = cnx.cursor()
agata.save_to_db(cursor)
cursor.close()
cnx.close()
