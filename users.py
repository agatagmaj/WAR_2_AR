import argparse
import models
from get_connection import get_connection
from clcrypto import password_hash, generate_salt
import psycopg2

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="user's login")
parser.add_argument("-p", "--password", help="user's password")
parser.add_argument("-n", "--new-pass", help="new password")
parser.add_argument("-l", "--list", help="request to list all users")
parser.add_argument("-d", "--delete", help="login to be deleted")
parser.add_argument("-e", "--edit", help="login to be edited")

args = parser.parse_args()
login = args.username
password = args.password

if len(password) < 8:
    print('Za krótkie hasło')
else:
    if args.username and args.password and not (args.edit or args.delete):
        cnx = get_connection()
        cursor = cnx.cursor()
        a = models.Users.load_all_users(cursor)
        b = []
        for user in a:
            b.append(user.username)
        if login in b:
            print("Użytkownik o podanym loginie już istnieje")
        else:
            new_user = models.Users()
            new_user.username = login
            new_user.set_password(password, generate_salt())
            while True:
                try:
                    new_user.email = input("Podaj e-mail: ")
                    new_user.save_to_db(cursor)
                    print("Nowy użytkownik założony")
                    break
                except psycopg2.IntegrityError:
                    print("Podany e-mail już istnieje")
                    new_user.email = input("Podaj inny e-mail: ")
    else:
        print("Nie podano parametrów")

    cnx.close()
    cursor.close()

if __name__ == "__main__":
    pass
