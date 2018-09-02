# from Modul_2.WAR_2_AR.clcrypto import password_hash, generate_salt
# from  Modul_2.WAR_2_AR.get_connection import get_connection
from clcrypto import password_hash, generate_salt
from  get_connection import get_connection


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
            cursor.execute(sql)
            self.__id = cursor.fetchone()[0]  # albo cursor.fetchone()['id']
            return True
        else:
            sql = f"""UPDATE Users SET username='{self.username}', email='{self.email}', hashed_password='{self.hashed_password}'
            WHERE id='{self.id}'"""
            cursor.execute(sql)
            return True

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = f"SELECT id, username, email, hashed_password FROM users WHERE id='{user_id}'"

        cursor.execute(sql)  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = Users()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, email, hashed_password FROM Users"

        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = Users()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.email = row[2]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
        return ret

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"

        cursor.execute(sql, (self.__id,))
        self.__id = -1
        return True


if __name__ == "__main__":
    hela = Users()
    hela.username = "Helka"
    hela.email = "HelaD@gmail.com"
    hela.set_password("Helenk@2018", generate_salt())

    cnx = get_connection()
    cursor = cnx.cursor()
    # stworzyc kursor, który tworzy słownik i wyświetla alternatywa dla wyświetlania jednego atrybutu poniżej
    a = Users.load_all_users(cursor)
    b = []
    for user in a:
        b.append(user.username)
    print(b)

    ### delete object
    # a = Users.load_user_by_id(cursor, 2)
    # a.delete(cursor)

    cursor.close()
    cnx.close()

### save_to_db
# hela.save_to_db(cursor)

### load_user_by_id


### load_all_users
# stworzyc kursor, który tworzy słownik i wyświetla alternatywa dla wyświetlania jednego atrybutu poniżej
# a = Users.load_all_users(cursor)
# b = []
# for user in a:
#     b.append(user.username)
# print(b)

### update object
# a = Users.load_user_by_id(cursor, 2)
# a.username = "Paw"
# a.email = "dab.pwl@net.pl"
# a.save_to_db(cursor)

### delete object
# a = Users.load_user_by_id(cursor, 2)
# a.delete(cursor)
