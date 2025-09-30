import mysql.connector as ms
from db import get_connection
from login import logged_in_user_id
import os
import subprocess
import sys
from datetime import datetime
from count import count_unread_messages, count_found_items_unclaimed, count_lost_items, count_reported_items

def clr_line():# overwrite the input line cleanly
    sys.stdout.write("\033[F")  # move cursor up
    sys.stdout.write("\033[K")  # clear line
    sys.stdout.flush()

def menu():
    print("🏠 Home Menu")
    print("⚠️ Report Item (1): Report a lost or found item")
    print("🔎 Browse/Search Items (2): Browse or search for lost and found items")
    print(f"💬 Messages (3): {count_unread_messages(logged_in_user_id)}")
    print("🌐 Global Chat (4): Join the global chat room")
    print("🙎‍♂️ My Profile (5): View and edit your profile")
    print("📈 Leaderboard (6): See your heroes who help people find their lost items!")
    print("🚪 Logout (7):")
    print("🏃‍♂️ Exit (0):")
    print()
    inp = int(input("Enter your choice: "))
    print()
    print()
    if inp == 1:
        ReportItem()
    elif inp == 2:
        BrowseItems()
    elif inp == 3:
        Messages()
    elif inp == 4:
        GlobalChat()
    elif inp == 5:
        Profile()
    elif inp == 6:
        print("Viewing Leaderboard")
        ViewLeaderboard()
    elif inp == 7:
        print("Logging out... 🚪..🏃‍♂️..🏃‍♂️")
        logout()
    elif inp == 0:
        print("Exiting... 🚪..🏃‍♂️..🏃‍♂️")
        exit()
    else:
        print("Invalid Input")
def me():
    print()
    print("🏠 Go back to menu (1): ")
    print("🏃‍♂️ Exit (0): ")
    print()
    inp = int(input("Enter your choice: "))
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
    print("🏠 Go back to menu (2): ")
    print("🏃‍♂️ Exit (0): ")
    print()
    inp = int(input("Enter your choice: "))
    print()
    if inp == 1:
        return MessageUser()
    elif inp == 2:
        return menu()
    elif inp == 0:
        print("Exiting... 🚪..🏃‍♂️..🏃‍♂️")
        exit()
    else:
        print("Invalid Input")
        me2()

def ReportItem():
    print("⚠️ Report Item")
    print("Report Lost Item (1): Lost an item? Let others know!")
    print(f"Report Found Item (2): Found an item ? Become a hero by helping others claim it!")
    print("Go back to Home Menu (0):")
    print()
    inp = int(input("Enter your choice: "))
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
    print(f"Browse Your Lost Items (1): {count_found_items_unclaimed(logged_in_user_id)}")
    print(f"Browse All Lost Items (2): {count_lost_items()} Help users connect with their lost belongings!")
    print(f"Browse Found Items (3): ")
    print("Search Items (4): Search for specific items")
    print("See list of all items (5): ")
    print("Back to Home Menu (0):")
    print()
    inp = int(input("Enter your choice: "))
    if inp == 1:
        print("Browsing Lost Items")
        BrowseLostItems()
    elif inp == 2:
        print("Browsing Found Items")
        BrowseFoundItems()
    elif inp == 3:
        print("Searching Items")
        SearchItems()
    elif inp == 0:
        return menu()
    else:
        print("Invalid Input")

def Messages():
    print("💬 Messages")
    print("View Conversations (1):")
    print("Start New Conversation (2):")
    print("Back to Home Menu (0):")
    print()
    inp = int(input("Enter your choice: "))
    if inp == 1:
        print("Viewing Conversations...")
        ViewConversations()
    elif inp == 2:
        print("Starting New Conversation")
        StartNewConversation()
    elif inp == 0:
        return menu()
    else:
        print("Invalid Input")

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

        except Exception as e:
            db_connection.rollback()
            print("❌ Failed to send message:", e)
        
def GlobalChat():
    print("🌐 Global Chat")
    print("Enter Global Chat Room (1):")
    print("Back to Home Menu (0):")
    print()
    inp = int(input("Enter your choice: "))
    if inp == 1:
        print("Entering Global Chat Room")
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

def Profile():
    print("🙎‍♂️ My Profile")
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE id = %s", (logged_in_user_id,))
    user = cursor.fetchone()
    print()
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Points: {user['points']}")
    print(f"Account Created At: {user['created_at']}")
    print(f"Points: {user['points']}")
    print()
    print("Edit Profile (1): Update your username, email, or password")
    print("View Your reported Items (2): See items you've reported")
    print("Delete Account (3): Permanently delete your account and all associated data")
    print("Back to Home Menu (0):")
    print()
    inp = int(input("Enter your choice: "))
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
        inp = int(input("Enter your choice: "))
        if inp == 1:
            print("Verify your identity to proceed.")
            password = input("Enter your current password: ")
            if not verify_user(logged_in_user_id, password):
                print("Authentication failed. Incorrect password.")
                return Profile()
            new_username = input("Enter your new username: ")
            cursor.execute("UPDATE Users SET username = %s WHERE id = %s", (new_username, logged_in_user_id))
            db_connection.commit()
            print("Username updated successfully.")
        elif inp == 2:
            new_email = input("Enter your new email: ")
            cursor.execute("UPDATE Users SET email = %s WHERE id = %s", (new_email, logged_in_user_id))
            db_connection.commit()
            print("Email updated successfully.")
        elif inp == 3:
            new_password = input("Verify your current password: ")
            cursor.execute("UPDATE Users SET password = %s WHERE id = %s", (new_password, logged_in_user_id))
            db_connection.commit()
            print("Password updated successfully.")
        elif inp == 0:
            return Profile()
        else:
            print("Invalid Input")
        db_connection.commit()
    elif inp == 3:
        confirm = input("Are you sure you want to delete your account? This action is irreversible. (y/n): ")
        if confirm.lower() == "y":
            try:
                cursor.execute("DELETE FROM Users WHERE id = %s", (logged_in_user_id,))
                db_connection.commit()
                print("Your account and all associated data have been deleted.")
                logout()
            except Exception as e:
                db_connection.rollback()
                print("Failed to delete account. Please try again.")
                print(f"Error: {e}")
        else:
            print("Account deletion cancelled.")
            return Profile()
    else:
        print("Invalid Input")

def ValidateRepeatedItem(item_name):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    

def ReportLostItem(logged_in_user_id):
    item_name = input("Enter the name of the lost item: ")
    if not item_name:
        print("Item name cannot be empty. Please try again.")
        return ReportLostItem(logged_in_user_id)
    try:
        cursor.execute("""
        SELECT EXISTS (SELECT * FROM Items WHERE item_name = %s);
        """), (item_name, )
        exists = cursor.fetchone()
        if exists:
            print(f"ID: {exists['item_id']} | Name: {exists['item_name']}\nDesc: {exists['item_description']}\nCategory: {exists['category']}")
            print()
            confirmation = input("Is this the same item you are logging in currently? (y/n): ")
            if confirmation.lower() == "y":
                print("You cannot log in the same item twice!")
                db_connection.rollback()
            elif confirmation == "n":
                pass

    except Exception as e:
        print("\n❌ Failed to validate item.")
        print(f"Error: {e}")
        return False

    finally:
        cursor.close()
        db_connection.close()

    item_description = input("Enter a description of the lost item: ")
    if not item_description:
        print("Item description cannot be empty. Please try again.")
        return ReportLostItem(logged_in_user_id)
    category = input("Enter category of the item: ")
    if exists['item_name'] == item_name and exists['item_description'] == item_description and exists['category'] == category and exists['user_id'] == logged_in_user_id:
        print("You cannot report the same item twice!")
    else:
        bounty = int(input("Enter the price of the item (This will not be displayed to others and will be only used for calculation of points): "))//10
        if bounty < 1 or bounty == "":
            bounty = 1
            print("Minimum bounty is 1 point. Setting bounty to 1 point.")
        item_image_url = input("Enter an image URL (or leave blank): ")
    
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Items")
        item_id = cursor.fetchone()[0] + 1
    
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

        except Exception as e:
            db_connection.rollback()
            print("\n❌ Failed to report lost item. Please try again.")
            print(f"Error: {e}")
            me()

        finally:
            cursor.close()
        
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
        chosen_id = int(input("\nEnter the ID of the item you found: "))
        if chosen_id == "c1":
            BrowseLostItems()
        elif chosen_id == "c2":
            BrowseFoundItems()
        elif chosen_id.isdigit():
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
    
            # cursor.execute("""
            #     INSERT INTO Items (found_description, found_by, status, found_image_url)
            #     SELECT item_name, %s, %s, %s, %s, %s
            #     FROM Items WHERE item_id = %s
            # """, (item_description, logged_in_user_id, category,"found", item_image_url, chosen_id))
    
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
        else:
            print("❌ Invalid input. Please enter a valid item ID.")
            return me()
    except Exception as e:
        db_connection.rollback()
        print("\n❌ Failed to register found item.")
        print(f"Error: {e}")
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

    except Exception as e:
        print("\n❌ Failed to retrieve leaderboard.")
        print(f"Error: {e}")
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

    except Exception as e:
        print("\n❌ Failed to retrieve lost items.")
        print(f"Error: {e}")
        print()
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
        

    except Exception as e:
        print("\n❌ Failed to retrieve found items.")
        print(f"Error: {e}")
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

    except Exception as e:
        print("\n❌ Failed to perform search.")
        print(f"Error: {e}")

    finally:
        cursor.close()
menu()