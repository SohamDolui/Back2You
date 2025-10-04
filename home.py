import mysql.connector as ms
from db import get_connection
from login import logged_in_user_id
import os
import subprocess
import sys
from datetime import datetime
import count
from count import count_found_items_claimed, count_unread_messages, count_found_items_unclaimed, count_lost_items, count_reported_items
import re
import random


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def clr_line():# overwrite the input line cleanly
    sys.stdout.write("\033[F")  # move cursor up
    sys.stdout.write("\033[K")  # clear line
    sys.stdout.flush()

def verify_email(email, otp):
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    html_template = f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Back2You Email Verification</title>
    <style>
        body {{
            font-family: 'Trebuchet MS', sans-serif;
            background-color: #ffffff;
            color: #333333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 40px auto;
            border: 1px solid #fafafa;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background-color: #fafafa;
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #ff4d4d;
        }}
        .header img {{
            max-width: 150px;
            height: auto;
        }}
        .content {{
            padding: 30px;
            text-align: center;
            background-color: #ff4d4d;
        }}
        .content h1 {{
            color: #ff4d4d;
            background-color: #fafafa;
            font-size: 24px;
            margin: 20px auto; /* centers the block */
            padding: 10px 0;
            width: 60%;          /* wider than fit-content but not full width */
            min-width: 200px;    /* ensures it doesn’t get too small on mobile */
            max-width: 400px;    /* prevents it from being too wide on large screens */
            border-radius: 5px;
            text-align: center;  /* centers the text inside the block */
        }}


        .otp {{
            display: inline-block;
            background-color: #ff4d4d;
            color: #ffffff;
            font-size: 28px;
            font-weight: bold;
            padding: 15px 30px;
            border-radius: 8px;
            margin: 20px 0;
            letter-spacing: 2px;
        }}
        .footer {{
            background-color: #f9f9f9;
            color: #777777;
            font-size: 12px;
            text-align: center;
            padding: 15px;
            border-top: 1px solid #eee;
        }}
        a.button {{
            background-color: #ff4d4d;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 6px;
            font-weight: bold;
            display: inline-block;
            margin-top: 20px;
        }}
        #emailtext {{
            font-size: 16px;
            line-height: 1.5;
            margin: 10px 0;
            background-color: #f2f2f2;
            padding: 20px 15px;
            border-radius: 15px;
            position: relative;
            overflow: hidden;
        }}

        /* Create a soft gradient border using a pseudo-element */
        #emailtext::before {{
            content: '';
            position: absolute;
            top: -3px; 
            left: -3px;
            right: -3px;
            bottom: -3px;
            border-radius: 18px; /* slightly bigger than the container */
            background: linear-gradient(to right, #ffcccc, #ffe6e6);
            z-index: -1; /* behind the content */
        }}

    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <!-- Add your logo here -->
            <img src='https://ik.imagekit.io/oy2mxy02p/back2you.jpg?updatedAt=1759601369037' alt='Back2You Logo'>
        </div>
        <div class='content'>
                <h1>Email Verification</h1>
            <div id='emailtext'>
                <p>Hello! 👋</p>
                <p>Thank you for joining <strong>Back2You</strong>.</p>
                <p>To complete your registration, please use the OTP below:</p>
                <div class='otp'>{otp}</div>
                <p>If you did not request this email, you can safely ignore it.</p>
                <a href='#' class='button'>Verify Now</a>
            </div>
        </div>
        <div class='footer'>
            &copy; 2025 Back2You. All rights reserved.<br>
            Lost something? Found something? Connect with the community at <a href='https://back2you.com'>back2you.com</a><br>
            Got any suggestions? or want to provide feedback? <br>
            Please feel free to reach out to us at <a href="mailto:back2you.bot@gmail.com">back2you.bot@gmail.com</a>
        </div>
    </div>
</body>
</html>
"""
    message = Mail(
        from_email="back2you.bot@gmail.com",
        to_emails=email,
        subject=f'{otp} - Email Verification - Back2You',
        html_content=html_template
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        # sg.set_sendgrid_data_residency("eu")
        # uncomment the above line if you are sending mail using a regional EU subuser
        response = sg.send(message)
        print("Verification email sent. Please check your inbox. (If not found, check Spam/Junk folder)")
    except Exception:
        print("Failed to send verification email. Please try again later.")
        me()
        return False
    return True

# --- small helper to avoid repeated crashes when user types non-numeric input ---
def int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def menu():
    print("🏠 Home Menu")
    print("⚠️ Report Item (1): Report a lost or found item")
    print("🔎 Browse/Search Items (2): Browse or search for lost and found items")
    print(f"📃View status of your reported items (3): {'No' if count_found_items_unclaimed(logged_in_user_id,'num') == 0 else count_found_items_unclaimed(logged_in_user_id,'num')} Unclaimed Item{'s' if count_found_items_unclaimed(logged_in_user_id,'num') != 1 else ''}")
    print(f"💬 Messages (4): {count_unread_messages(logged_in_user_id)}")
    print("🌐 Global Chat (5): Join the global chat room")
    print("🙎‍♂️ My Profile (6): View and edit your profile")
    print("📈 Leaderboard (7): See your heroes who help people find their lost items!")
    print("🚪 Logout (8):")
    print("🏃‍♂️ Exit (0):")
    print()
    inp = input("Enter your choice: ")
    print()
    print()
    if inp == "1":
        ReportItem()
    elif inp == "2":
        BrowseItems()
    elif inp == "3":
        ViewMyItems()
    elif inp == "4":
        Messages()
    elif inp == "5":
        GlobalChat()
    elif inp == "6":
        Profile()
    elif inp == "7":
        print("Viewing Leaderboard")
        ViewLeaderboard()
    elif inp == "8":
        print("Logging out... 🚪..🏃‍♂️..🏃‍♂️")
        logout()
    elif inp == "0":
        print("Exiting... 🚪..🏃‍♂️..🏃‍♂️")
        exit()
    else:
        print("Invalid Input")
        me()
def me():
    print()
    print("🏠 Go back to menu (1): ")
    print("🏃‍♂️ Exit (0): ")
    print()
    inp = int_input("Enter your choice: ")
    print()
    if inp == 1:
        return menu()
    elif inp == 0:
        print("Exiting... 🚪..🏃‍♂️..🏃‍♂️")
        exit()
    else:
        print("Invalid Input")

def me2():
    print()
    print("Message Users from here (1): ")
    print("Report a Found Item (2): ")
    print("🏠 Go back to menu (3): ")
    print("🏃‍♂️ Exit (0): ")
    print()
    inp = int_input("Enter your choice: ")
    print()
    if inp == 1:
        return MessageUser()
    elif inp == 2:
        return ReportFoundItem(logged_in_user_id)
    elif inp == 3:
        return menu()
    elif inp == 0:
        print("Exiting... 🚪..🏃‍♂️..🏃‍♂️")
        exit()
    else:
        print("Invalid Input")
        me2()

def me3():
    print()
    print("Message Users from here (1): ")
    print("Mark an item as 'Claimed' (2): ")
    print("🏠 Go back to menu (3): ")
    print("🏃‍♂️ Exit (0): ")
    print()
    inp = int_input("Enter your choice: ")
    print()
    if inp == 1:
        return MessageUser()
    elif inp == 2:
        return ReportFoundItem(logged_in_user_id)
    elif inp == 3:
        return menu()
    elif inp == 0:
        print("Exiting... 🚪..🏃‍♂️..🏃‍♂️")
        exit()
    else:
        print("Invalid Input")
        me3()

def ReportItem():
    print("⚠️ Report Item")
    print("Report Lost Item (1): Lost an item? Let others know!")
    print(f"Report Found Item (2): Found an item? Become a hero by helping others claim it!")
    print("Go back to Home Menu (0):")
    print()
    inp = int_input("Enter your choice: ")
    if inp == 1:
        print("Reporting a Lost Item...")
        ReportLostItem(logged_in_user_id)
    elif inp == 2:
        print("Reporting Found Item...")
        ReportFoundItem(logged_in_user_id)
    elif inp == 0:
        return menu()
    else:
        print("Invalid Input")

def BrowseItems():
    print("🔎 Browse/Search Items")
    print(f"Check Status of Your Lost Items (1): {count_found_items_unclaimed(logged_in_user_id)}")
    print(f"Browse All Lost Items (2): {count_lost_items(None)} Help users connect with their lost belongings!")
    print(f"Browse Found Items (3): ")
    print("Search Items (4): Search for specific items")
    print("See list of all items (5): ")
    print("Back to Home Menu (0):")
    print()
    inp = int_input("Enter your choice: ")
    if inp == 1:
        print("This feature is yet to be added")
    elif inp == 2:
        print("Browsing Lost Items")
        BrowseLostItems()
    elif inp == 3:
        print("Browsing Found Items")
        BrowseFoundItems()
    elif inp == 4:
        print("Searching Items")
        SearchItems()
    elif inp == 0:
        return menu()
    else:
        print("Invalid Input")

def ViewMyItems():
    print("📋 Viewing Status of Your Lost Items...")
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Items WHERE user_id = %s", (logged_in_user_id,))
        items = cursor.fetchall()
    except Exception:
        print("Failed to fetch items! ❌")
        me()

    finally:
        cursor.close()
    if not items:
        print("You have not yet reported any items.")
        return me()
    print("\nYour Reported Items:")
    found_but_not_claimed = []
    found_and_claimed = []
    lost = []
    for item in items:
        status = item['status']
        found_info = ""
        if status == 'found but not claimed':
            found_info = f" | Found by User ID: {item['found_by']}"
            found_but_not_claimed.append((f"ID: {item['item_id']} | Name: {item['item_name']} | Status: {status}{found_info}\nDesc: {item['item_description']}\nCategory: {item['category']}\n"))
        elif status == 'found and claimed':
            found_info = f" | Found by User ID: {item['found_by']} | Claimed"
            found_and_claimed.append((f"ID: {item['item_id']} | Name: {item['item_name']} | Status: {status}{found_info}\nDesc: {item['item_description']}\nCategory: {item['category']}\n"))
        elif status == 'lost':
            found_info = " | Still Lost"
            lost.append((f"ID: {item['item_id']} | Name: {item['item_name']} | Status: {status}{found_info}\nDesc: {item['item_description']}\nCategory: {item['category']}\n"))
    print()
    print(f"{'None' if len(found_but_not_claimed) == 0 else len(found_but_not_claimed)} of your reported item{'s are' if len(found_but_not_claimed) != 1 else ' is'} found but unclaimed")
    print(f"{'None' if len(lost) == 0 else len(lost)} of your reported item{'s are' if len(lost) != 1 else ' is'} lost.")
    print(f"{'None' if len(found_and_claimed) == 0 else len(found_and_claimed)} of your reported item{'s are' if len(found_and_claimed) != 1 else ' is'} found and claimed")
    if found_but_not_claimed:
        print(f"\n{len(found_but_not_claimed)} items reported by You have been Found but not yet claimed:")
        for item in found_but_not_claimed:
            print(item)
    if lost:
        print("\nItems Still Lost:")
        for item in lost:
            print(item)
    if found_and_claimed:
        print("\nItems Found and Claimed:")
        for item in found_and_claimed:
            print(item)
    return me2()

def Messages():
    print("💬 Messages")
    print("View Conversations (1):")
    print("Start New Conversation (2):")
    print("Back to Home Menu (0):")
    print()
    inp = int_input("Enter your choice: ")
    if inp == 1:
        print("Viewing Conversations...")
        ViewConversations()
    elif inp == 2:
        print("Starting New Conversation")
        MessageUser()
    elif inp == 0:
        return menu()
    else:
        print("Invalid Input")

def ViewConversations():
    print("This feature is yet to be added")

def MessageUser2():
    s_id = logged_in_user_id
    r_id = input("Enter the user ID or the Username of the person to message: ")
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)
    if not r_id.isdigit():
        cursor.execute("SELECT * FROM Users WHERE username = %s", (r_id,))
        user = cursor.fetchone()
        r_id = user['id'] if user else None
    else:
        r_id = int(r_id)
    
    if r_id is None:
        print("User not found. Please enter a valid user ID or Username.")
        return MessageUser()
    if r_id == s_id:
        print("You cannot message yourself. Please enter a different user ID or Username.")
        return MessageUser()

    cursor.execute("SELECT * FROM Users WHERE id = %s", (r_id,))
    recipient = cursor.fetchone()
    if not recipient:
        print("User not found. Please enter a valid user ID.")
        return MessageUser()

    print(f"Messaging {recipient['username']} | ID: {recipient['id']}")
    print("Type 'exit' to end the conversation.")

    while True:
        message = input("Enter your message: ")

        if message.lower() == "exit":
            print("Exiting conversation...")
            cursor.close()
            db_connection.close()
            return me()

        try:
            cursor.execute("""
                INSERT INTO Messages (sender_id, receiver_id, content, created_at)
                VALUES (%s, %s, %s, %s)
            """, (s_id, r_id, message, datetime.now()))
            db_connection.commit()

            clr_line()
            sys.stdout.flush()

            print("You: " + message)

        except Exception:
            db_connection.rollback()
            print("❌ Failed to send message")
            me()

def MessageUser():
    s_id = logged_in_user_id
    r_id = input("Enter the user ID or the Username of the person to message: ")
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)
    if not r_id.isdigit():
        cursor.execute("SELECT * FROM Users WHERE username = %s", (r_id,))
        user = cursor.fetchone()
        r_id = user['id'] if user else None
    else:
        r_id = int(r_id)
    
    if r_id is None:
        print("User not found. Please enter a valid user ID or Username.")
        return MessageUser()
    if r_id == s_id:
        print("You cannot message yourself. Please enter a different user ID or Username.")
        return MessageUser()

    cursor.execute("SELECT * FROM Users WHERE id = %s", (r_id,))
    recipient = cursor.fetchone()
    if not recipient:
        print("User not found. Please enter a valid user ID.")
        return MessageUser()

    print(f"Messaging {recipient['username']} | ID: {recipient['id']}")
    print("Type 'exit' to end the conversation.")

    while True:
        message = input("Enter your message: ")

        if message.lower() == "exit":
            print("Exiting conversation...")
            cursor.close()
            db_connection.close()
            return me()

        try:
            cursor.execute("""
                INSERT INTO Messages (sender_id, receiver_id, content, created_at)
                VALUES (%s, %s, %s, %s)
            """, (s_id, r_id, message, datetime.now()))
            db_connection.commit()

            clr_line()
            sys.stdout.flush()

            print("You: " + message)

        except Exception:
            db_connection.rollback()
            print("❌ Failed to send message")
            me()
        
def GlobalChat():
    print("🌐 Global Chat")
    print("Enter Global Chat Room (1):")
    print("Back to Home Menu (0):")
    print()
    inp = int_input("Enter your choice: ")
    if inp == 1:
        print("Entering Global Chat Room")
        print("This feature is yet to be added.")
    elif inp == 0:
        return menu()
    else:
        print("Invalid Input")

def verify_user(user_id, password):
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user and user['password'] == password:
        return True
    return False
def GoBackToProfile():
    print()
    print("⬅️ Go back to Profile (1): ")
    print("🏃‍♂️ Exit (0): ")
    inp = input("Enter Your Choice: ")
    if inp.isdigit():
        inp = int(inp)
    if inp == 1:
        return Profile()
    elif inp == 0:
        exit()
    else:
        print("Invalid Input ❌")
        return GoBackToProfile()
    
def Profile():
    print("🙎‍♂️ My Profile")
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE id = %s", (logged_in_user_id,))
    user = cursor.fetchone()
    print()
    print(f"User ID: {logged_in_user_id}")
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Points: {user['points']}")
    print(f"💛 {count.get_people_helped(logged_in_user_id)} people helped | 🌍 {count.count_reported_lost_items(logged_in_user_id)} item{'s' if count.count_reported_lost_items(logged_in_user_id) != 1 else ''} reported | 🔑 {count.count_reunited_items(logged_in_user_id)} belonging{'s' if count.count_reunited_items(logged_in_user_id) != 1 else ''} reunited — you’re shaping a better community.")
    print(f"Account Created At: {user['created_at']}")
    print()
    print("Edit Profile (1): Update your username, email, or password")
    print("View Your reported Items (2): See Status of items you've reported")
    print("Delete Account (3): Permanently delete your account and all associated data")
    print("Back to Home Menu (0):")
    print()
    inp = int_input("Enter your choice: ")
    clr_line()
    print("Your choice:", inp)
    if inp == 0:
        return menu()
    elif inp == 1:
        print("Editing Profile")
        print("Change Username (1): ")
        print("Change Email (2): ")
        print("Change Password (3): ")
        print("Go back to Profile (0): ")
        print()
        inp = int_input("Enter your choice: ")
        if inp == 1:
            print("Verify your identity to proceed.")
            while True:
                password = input("Enter your current password: ")
                if not verify_user(logged_in_user_id, password):
                    print("Authentication failed. Incorrect password.")
                    continue
                break
            print("Password Authenticated ✅")
            while True:
                new_username = input("Enter your new username: ")
                if not new_username:
                    print("Username cannot be empty.")
                    continue
                break
            cursor.execute("UPDATE Users SET username = %s WHERE id = %s", (new_username, logged_in_user_id))
            db_connection.commit()
            print("Username updated successfully.")

        elif inp == 2:
            while True:
                new_email = input("Enter your new email: ")
                if not validate_email(new_email):
                    print("Invalid email format. Please try again.")
                    continue
                break
            print("Please verify E-mail before proceeding...")
            otp = random.randint(1000, 9999)
            while True:
                if not verify_email(new_email, otp):
                    print("Failed to send verification email. Please try again later.")
                    return Profile()
                try:
                    User_OTP = int(input(f"Enter the OTP sent to {new_email}: "))
                    if int(User_OTP) == otp:
                        print("Email verified successfully ✅")
                        break
                    else:
                        print("Incorrect OTP. Please try again.")
                        User_OTP = input(f"Enter the OTP sent to {new_email}: ")
                except ValueError:
                    print("Invalid input. Please enter the numeric OTP.")
                    User_OTP = input(f"Enter the OTP sent to {new_email}: ")
            cursor.execute("UPDATE Users SET email = %s WHERE id = %s", (new_email, logged_in_user_id))
            db_connection.commit()
            print("Email updated successfully.")

        elif inp == 3:
            print("Verify your identity to proceed.")
            while True:
                password = input("Enter your current password (Enter f if you forgot your password): ")
                if password == "f":
                    print("Verify it's you - Enter the OTP sent to your registered email.")
                    otp = random.randint(1000, 9999)
                    if not verify_email(user['email'], otp):
                        print("Failed to send verification email. Please try again later.")
                        return Profile()
                    try:
                        User_OTP = int(input(f"Enter the OTP sent to {user['email']}: "))
                        if int(User_OTP) == otp:
                            print("Email verified successfully ✅")
                            break
                        else:
                            print("Incorrect OTP. Please try again.")
                            continue
                    except ValueError:
                        print("Invalid input. Please enter the numeric OTP.")
                        continue
                if not verify_user(logged_in_user_id, password):
                    print("Authentication failed. Incorrect password.")
                    continue
                break
            new_password = input("Verify your current password: ")
            cursor.execute("UPDATE Users SET password = %s WHERE id = %s", (new_password, logged_in_user_id))
            db_connection.commit()
            print("Password updated successfully.")
        elif inp == 0:
            return Profile()
        else:
            print("Invalid Input")
        db_connection.commit()
        GoBackToProfile()
    elif inp == 2:
        ViewMyItems()
    elif inp == 3:
        confirm = input("Are you sure you want to delete your account? This action is irreversible. (y/n): ")
        if confirm.lower() == "y":
            try:
                cursor.execute("DELETE FROM Users WHERE id = %s", (logged_in_user_id,))
                db_connection.commit()
                print("Your account and all associated data have been deleted.")
                logout()
            except Exception:
                db_connection.rollback()
                print("Failed to delete account. Please try again.")
                me()
        else:
            print("Account deletion cancelled.")
            return Profile()
    elif inp == 0:
        exit()
    else:
        print("Invalid Input")

def ReportLostItem(logged_in_user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)
    item_name = input("Enter the name of the lost item: ")
    if not item_name:
        print("Item name cannot be empty. Please try again.")
        cursor.close()
        db_connection.close()
        return ReportLostItem(logged_in_user_id)
    try:
        cursor.execute("SELECT * FROM Items WHERE item_name = %s;", (item_name, ))
        exists = cursor.fetchone()
        reverify = "n"
        if exists:
            reverify = "y"
            print()
            print(f"ID: {exists['item_id']} | Name: {exists['item_name']}\nDesc: {exists['item_description']}\nCategory: {exists['category']}")
            print()
            confirmation = input("Is this the same item you are logging in currently? (y/n): ")
            if confirmation.lower() == "y":
                print()
                print("You cannot log in the same item twice!")
                db_connection.rollback()
                cursor.close()
                db_connection.close()
                return me()
            elif confirmation == "n":
                pass

    except Exception:
        print("\n❌ Failed to validate item.")
        cursor.close()
        db_connection.close()
        return me()

    # NOTE: do NOT close cursor/db_connection here — we need them for later inserts
    item_description = input("Enter a description of the lost item: ")
    if not item_description:
        print("Item description cannot be empty. Please try again.")
        cursor.close()
        db_connection.close()
        return ReportLostItem(logged_in_user_id)
    category = input("Enter category of the item\n(a for Accessories)\n(c for Clothing)\n(e for Electronics)\n(s for Stationery)\n(leave blank for others)\nCategory: ")
    for i in range(5):
        clr_line()
    if category.lower() == "a":
        category = "Accessories"
    elif category.lower() == "c":
        category = "Clothing"
    elif category.lower() == "e":
        category = "Electronics"
    elif category.lower() == "s":
        category = "Stationery"
    elif category == "":
        category = "Others"
    else:
        print("Invalid Input. Setting category to 'Others'.")
        category = "Others"
    print("Category set to:", category)
    
    if reverify == "y":
        if exists.get('item_name') == item_name and exists.get('item_description') == item_description and exists.get('category') == category and exists.get('user_id') == logged_in_user_id:
            print()
            print("You cannot report the same item twice!")
            cursor.close()
            db_connection.close()
            return me()

    # Ask bounty until valid (no jumping back to menu)
    while True:
        bounty_input = input("Enter the price of the item (This will not be displayed to others and will be only used for calculation of points): ")
        if not bounty_input.isdigit():
            print("❌ Invalid input. Please enter a number.")
            continue
        bounty = int(bounty_input) // 10
        if bounty < 1:
            bounty = 1
            print("⚠️ Minimum bounty is 1 point. Setting bounty to 1 point.")
        break

    item_image_url = input("Enter an image URL (or leave blank): ")

    cursor.execute("SELECT MAX(item_id) FROM Items")
    row = cursor.fetchone()
    item_id = (row["MAX(item_id)"] or 0) + 1

    
    try:
        cursor.execute("""
            INSERT INTO Items (item_id, item_name, item_description, user_id, category, bounty_points, status, item_image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (item_id, item_name, item_description, logged_in_user_id, category, bounty, "lost", item_image_url))
    
        db_connection.commit()
            
        print(f"\n✅ Lost Item Reported Successfully!")
        print(f"Name: {item_name}")
        print(f"Description: {item_description}")
        print(f"Category: {category}")
        if item_image_url:
            print(f"Image URL: {item_image_url}")
        me()

    except Exception:
        db_connection.rollback()
        print("\n❌ Failed to report lost item. Please try again.")
        me()

    finally:
        cursor.close()
        db_connection.close()
        
def ReportFoundItem(logged_in_user_id):
    
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)  # dictionary=True gives column names in result

    try:
        # Step 1: Show all lost items
        cursor.execute("SELECT item_id, item_name, category, item_description FROM Items WHERE status = 'lost'")
        lost_items = cursor.fetchall()

        if not lost_items:
            print("\n📭 No lost items reported yet.")
            me()

        print("\n📌 Lost Items Reported:")
        for item in lost_items:
            print(f"ID: {item['item_id']} | Name: {item['item_name']}\nDesc: {item['item_description']}")

        # Step 2: Ask which lost item was found
        print("Don't see the item you found? It might have already been claimed or reported as found.")
        print("Check Lost Items (c1) or Found Items (c2).")

        # Keep asking until valid choice (digit or c1/c2)
        while True:
            chosen = input("\nEnter the ID of the item you found (or type c1 to check Lost Items, c2 to check Found Items): ").strip()
            if chosen == "c1":
                BrowseLostItems()
                cursor.close()
                db_connection.close()
                return
            elif chosen == "c2":
                BrowseFoundItems()
                cursor.close()
                db_connection.close()
                return
            elif chosen.isdigit():
                chosen_id = int(chosen)
                break
            else:
                print("❌ Invalid input. Please enter a valid item ID or c1/c2.")

        clr_line()
        sys.stdout.flush()
        print(f"Chosen Item ID: {chosen_id}")
        # Check if the ID exists in the lost list
        if not any(item['item_id'] == chosen_id for item in lost_items):
            print("❌ Invalid ID. Please try again.")
            return
    
        # Step 3: Insert new 'found' report under current user
        item_description = input("Enter description/details for found item (or leave blank): ")
        # category = lost_items[[item['item_id'] for item in lost_items].index(chosen_id)]['category']
        item_image_url = input("Enter image URL (or leave blank): ")
    
        # Step 4: Update status of lost item → "found"
    
        cursor.execute("SELECT bounty_points FROM Items WHERE item_id = %s", (chosen_id,))
        bounty = cursor.fetchone()['bounty_points']
        cursor.execute("SELECT points FROM Users WHERE id = %s", (logged_in_user_id,))
        bounty_user = bounty + cursor.fetchone()['points']
        cursor.execute("""UPDATE Items SET status = 'found but not claimed', found_description = %s, found_by = %s, found_image_url = %s WHERE item_id = %s""", (item_description, logged_in_user_id, item_image_url, chosen_id))
        cursor.execute("UPDATE Users SET points = %s WHERE id = %s", (bounty_user, logged_in_user_id))
        cursor.execute("SELECT bounty_points FROM Items WHERE item_id = %s", (chosen_id,))
        bounty = cursor.fetchone()['bounty_points']
    
        db_connection.commit()
    
        print(f"\n✅ Item ID {chosen_id} marked as FOUND and recorded under your account.")
        print("Thank you for helping reunite lost items with their owners!")
        print(f"You have been rewarded {bounty} points for your good deed!")
        me()
    except Exception:
        db_connection.rollback()
        print("\n❌ Failed to register found item.")
        me()

    finally:
        cursor.close()

def ViewLeaderboard():
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT username, points FROM Users ORDER BY points DESC LIMIT 10")
        leaders = cursor.fetchall()

        if not leaders:
            print("\n📭 No users found.")
            return

        print("\n🏆 Leaderboard - Top 10 Users by Points:")
        for idx, user in enumerate(leaders, start=1):
            print(f"{idx}. {user['username']} - {user['points']} points")
        me()

    except Exception:
        print("\n❌ Failed to retrieve leaderboard.")
        me()

    finally:
        cursor.close()

def logout():
    print("🔒 Logging out...")

    # Path to your main.py
    script_path = os.path.join(os.path.dirname(__file__), "main.py")

    if os.name == "nt":  # Windows
        subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:  # Linux / Mac
        subprocess.Popen(["python3", script_path])

    sys.exit(0)  # Kill current session

def BrowseLostItems():
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT item_id, item_name, item_description, category FROM Items WHERE status = 'lost'")
        lost_items = cursor.fetchall()

        if not lost_items:
            print("\n📭 No lost items reported yet.")
            return me()

        print("\n📌 Lost Items Reported:")
        print()
        for item in lost_items:
            print(f"ID: {item['item_id']} | Name: {item['item_name']}\nDesc: {item['item_description']}\nCategory: {item['category']}")
            print()
        me()

    except Exception:
        print("\n❌ Failed to retrieve lost items.")
        me()

    finally:
        cursor.close()

def BrowseFoundItems():
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT item_id, item_name, item_description, category FROM Items WHERE status = 'found but not claimed'")
        found_items = cursor.fetchall()

        if not found_items:
            print("\n📭 No found items reported yet.")
            return me()

        print("\n📌 Found Items Reported:")
        print()
        for item in found_items:
            print(f"ID: {item['item_id']} | Name: {item['item_name']}\nDesc: {item['item_description']}\nCategory: {item['category']}")
            print()
        me2()
        

    except Exception:
        print("\n❌ Failed to retrieve found items.")
        me()

    finally:
        cursor.close()

def SearchItems():
    search_term = input("Enter item name or keyword to search: ")
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT item_id, item_name, item_description, category, status 
            FROM Items 
            WHERE item_name LIKE %s OR item_description LIKE %s
        """, (f"%{search_term}%", f"%{search_term}%"))
        results = cursor.fetchall()

        if not results:
            print("\n📭 No items matched your search.")
            return

        print("\n🔍 Search Results:")
        for item in results:
            print(f"ID: {item['item_id']} | Name: {item['item_name']}\nDesc: {item['item_description']}\nCategory: {item['category']}\nStatus: {item['status']}")
            print()

    except Exception:
        print("\n❌ Failed to perform search.")
        me()

    finally:
        cursor.close()
menu()
