from db import get_connection
# print("This part of the code has been called!")

logged_in_user_id = None

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor = get_connection().cursor()
    cursor.execute("USE Back2You")
    cursor.execute(f"SELECT * FROM Users WHERE username = '{username}' AND password = '{password}'")
    data = cursor.fetchall()

    if len(data) == 0:
        print("The data entered is incorrect!\n")
        exit()
    else:
        global logged_in_user_id
        logged_in_user_id = data[0][0]

def sign_up():
    username = input("To Sign up\nEnter the username you want: ")
    password = input("Enter Password: ")
    email = input("Enter your email: ")

    if username is None or password is None or email is None:
        print("\nUsername/Password/email cannot be None")
        exit()

    if len(username) > 50 or len(password) > 50 or len(email) > 100:
        print("\nThe Username/Password can consist maximum of 50 letters and Email can consist maximum of 100 characters")
        exit()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("USE Back2You")
    # cursor.execute("SELECT * FROM Users WHERE username = '?'", (username,))
    cursor.execute(f"SELECT * FROM Users WHERE username = '{username}'")

    if len(cursor.fetchall()) != 0:
        print("A user already exists with this username!")
        exit()
    else:
        cursor.execute(f"INSERT INTO Users (username, password, email) VALUES('{username}', '{password}', '{email}')")
        conn.commit()

        print("The user has been created!")
        cursor.execute(f"SELECT * FROM Users WHERE username = '{username}'")
        user_data = cursor.fetchall()
        
        global logged_in_user_id
        logged_in_user_id = user_data[0][0]

choice = input("WELCOME TO Back2You\nLog in (1) or Sign up (2): ")

if choice == "1": login()
elif choice == "2": sign_up()
else:
    print("You must have entered 0 or 1!")
    exit()