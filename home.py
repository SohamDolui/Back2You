import mysql.connector as ms
from db import get_connection
from login import logged_in_user_id
import os
import subprocess
import sys
from datetime import datetime 
print("Welcome to BACK2YOU")
print()

def menu():
    print("🏠 Home Menu")
    print("⚠️ Report Item (1): Report a lost or found item")
    print("🔎 Browse/Search Items (2): Browse or search for lost and found items")
    print(f"💬 Messages (3): You have {get_unread_message_count(logged_in_user_id)}!")
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

def ReportItem():
    print("⚠️ Report Item")
    print("Report Lost Item (1): Lost an item? Let others know!")
    print("Report Found Item (2): Found an item? Become a hero by helping others claim it!")
    print("Go back to Home Menu (0):")
    print()
    inp = int(input("Enter your choice: "))
    if inp == 1:
        print("Reporting a Lost Item")
        ReportLostItem(logged_in_user_id)
    elif inp == 2:
        print("Reporting Found Item")
        ReportFoundItem(logged_in_user_id)
    elif inp == 0:
        return menu()
    else:
        print("Invalid Input")

def BrowseItems():
    print("🔎 Browse/Search Items")
    print("Browse Lost Items (1): Browse lost items reported by users and be their hero!")
    print("Browse Found Items (2): Browse to claim any found item reported by users")
    print("Search Items (3): Search for specific items")
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
        print("Viewing Conversations")
        ViewConversations()
    elif inp == 2:
        print("Starting New Conversation")
        StartNewConversation()
    elif inp == 0:
        return menu()
    else:
        print("Invalid Input")

def get_unread_message_count(user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Messages WHERE receiver_id = %s AND is_read = 0", (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return str(count)+" unread message"+("" if count == 1 else "")

def MessageUser():
    s_id = logged_in_user_id
    r_id = input("Enter the user ID of the person to message: ")
    if r_id == s_id:
        print("You cannot message yourself.")
        return MessageUser()
    elif not r_id.isdigit():
        print("Invalid user ID. Please enter a numeric user ID.")
        return MessageUser()
    r_id = int(r_id)

    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE id = %s", (r_id,))
    recipient = cursor.fetchone()
    if not recipient:
        print("User not found. Please enter a valid user ID.")
        return MessageUser()
    print(f"Messaging {recipient['username']} | ID: {recipient['id']})")
    print("Type 'exit' to end the conversation.")
    message = input("Enter your message: ")
    while message != "exit":
        try:
            cursor.execute("""
                INSERT INTO Messages (sender_id, receiver_id, message, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (s_id, r_id, message, datetime.now()))
            db_connection.commit()
            print("Message sent! Enter another message or type 'exit' to end.")
        except Exception as e:
            db_connection.rollback()
            print("Failed to send message. Please try again.")
            print(f"Error: {e}")
        message = input("Enter your message: ")
        sys.stdout.write("\033[K")
        sys.stdout.flush()
        print("You: " + message)

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

def Profile():
    print("🙎‍♂️ My Profile")
    print("Delete Account (1): Permanently delete your account and all associated data")
    print("Back to Home Menu (0):")
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE id = %s", (logged_in_user_id,))
    user = cursor.fetchone()
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Points: {user['points']}")
    print(f"Account Created At: {user['created_at']}")
    print(f"Points: {user['points']}")
    inp = int(input("Enter your choice: "))
    if inp == 0:
        return menu()
    elif inp == 1:
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

def ReportLostItem(logged_in_user_id):
    item_name = input("Enter the name of the lost item: ")
    item_description = input("Enter a description of the lost item: ")
    category = input("Enter category of the item: ")
    bounty = int(input("Enter the price of the item (This will not be displayed to others and will be only used for calculation of points): "))//10
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

    except Exception as e:
        db_connection.rollback()
        print("\n❌ Failed to report lost item. Please try again.")
        print(f"Error: {e}")
        menu()

    finally:
        cursor.close()
        me()

def ReportFoundItem(logged_in_user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)  # dictionary=True gives column names in result

    try:
        # Step 1: Show all lost items
        cursor.execute("SELECT item_id, item_name, item_description FROM Items WHERE status = 'lost'")
        lost_items = cursor.fetchall()

        if not lost_items:
            print("\n📭 No lost items reported yet.")

        print("\n📌 Lost Items Reported:")
        for item in lost_items:
            print(f"ID: {item['item_id']} | Name: {item['item_name']}\nDesc: {item['item_description']}")

        # Step 2: Ask which lost item was found
        chosen_id = int(input("\nEnter the ID of the item you found: "))

        # Check if the ID exists in the lost list
        if not any(item['item_id'] == chosen_id for item in lost_items):
            print("❌ Invalid ID. Please try again.")
            return

        # Step 3: Insert new 'found' report under current user
        item_description = input("Enter description/details for found item: ")
        category = input("Enter category of the found item: ")
        item_image_url = input("Enter image URL (or leave blank): ")

        cursor.execute("""
            INSERT INTO Items (item_name, item_description, user_id, category, status, item_image_url)
            SELECT item_name, %s, %s, %s, %s, %s, %s 
            FROM Items WHERE item_id = %s
        """, (item_description, logged_in_user_id, category,"found", item_image_url, chosen_id))

        # Step 4: Update status of lost item → "found"
        cursor.execute("""UPDATE Items SET status = 'found' WHERE item_id = %s, found_description = %s, found_by = %s, found_image_url = %s WHERE item_id = %s""", (chosen_id, item_description, logged_in_user_id, item_image_url, chosen_id))

        db_connection.commit()

        print(f"\n✅ Item ID {chosen_id} marked as FOUND and recorded under your account.")

    except Exception as e:
        db_connection.rollback()
        print("\n❌ Failed to register found item.")
        print(f"Error: {e}")

    finally:
        cursor.close()
    me()

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

    except Exception as e:
        print("\n❌ Failed to retrieve leaderboard.")
        print(f"Error: {e}")

    finally:
        cursor.close()
        me()

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
        cursor.execute("SELECT item_id, item_name, item_description, category FROM Items WHERE status = 'found'")
        found_items = cursor.fetchall()

        if not found_items:
            print("\n📭 No found items reported yet.")
            return

        print("\n📌 Found Items Reported:")
        print()
        for item in found_items:
            print(f"ID: {item['item_id']} | Name: {item['item_name']}\nDesc: {item['item_description']}\nCategory: {item['category']}")
            print()

    except Exception as e:
        print("\n❌ Failed to retrieve found items.")
        print(f"Error: {e}")

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