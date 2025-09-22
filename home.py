import mysql.connector as ms
from db import get_connection
from login import logged_in_user_id
import os
import subprocess
import sys

def menu():
    print("Welcome to BACK2YOU")
    print()
    print("Home Menu")
    print("Report Item (1):")
    print("Browse/Search Items (2):")
    print("Messages (3):")
    print("Global Chat (4):")
    print("My Profile (5):")
    print("Logout (6):")
    print("Exit (0):")
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
        print("Logging out...")
        logout()
    elif inp == 0:
        print("Exiting...")
        exit()
    else:
        print("Invalid Input")

def ReportItem():
    print("Report Item")
    print("Report Lost Item (1):")
    print("Report Found Item (2):")
    print("Back to Home Menu (0):")
    print()
    inp = int(input("Enter your choice: "))
    if inp == 1:
        print("Reporting a Lost Item")
        ReportLostItem(logged_in_user_id)
    elif inp == 2:
        print("Reporting Found Item")
        ReportFoundItem()
    elif inp == 0:
        return menu()
    else:
        print("Invalid Input")

def BrowseItems():
    print("Browse/Search Items")
    print("Browse Lost Items (1):")
    print("Browse Found Items (2):")
    print("Search Items (3):")
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
    print("Messages")
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

def GlobalChat():
    print("Global Chat")
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
    print("My Profile")
    print("Back to Home Menu (0):")
    inp = int(input("Enter your choice: "))
    if inp == 0:
        return menu()
    else:
        print("Invalid Input")

def ReportLostItem(logged_in_user_id):
    item_name = input("Enter the name of the lost item: ")
    item_description = input("Enter a description of the lost item: ")
    category = input("Enter category of the item: ")
    item_image_url = input("Enter an image URL (or leave blank): ")

    db_connection = get_connection()
    cursor = db_connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO Items (item_name, item_description, user_id, category, status, item_image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (item_name, item_description, logged_in_user_id, category, "lost", item_image_url))

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

    finally:
        cursor.close()

def ReportFoundItem(logged_in_user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)  # dictionary=True gives column names in result

    try:
        # Step 1: Show all lost items
        cursor.execute("SELECT item_id, item_name, item_description FROM Items WHERE status = 'lost'")
        lost_items = cursor.fetchall()

        if not lost_items:
            print("\n📭 No lost items reported yet.")
            return

        print("\n📌 Lost Items Reported:")
        for item in lost_items:
            print(f"ID: {item['item_id']} | Name: {item['item_name']} | Desc: {item['item_description']}")

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
            SELECT item_name, %s, %s, %s, %s, %s 
            FROM Items WHERE item_id = %s
        """, (item_description, logged_in_user_id, category, "found", item_image_url, chosen_id))

        # Step 4: Update status of lost item → "found"
        cursor.execute("UPDATE Items SET status = 'found' WHERE item_id = %s", (chosen_id,))

        db_connection.commit()

        print(f"\n✅ Item ID {chosen_id} marked as FOUND and recorded under your account.")

    except Exception as e:
        db_connection.rollback()
        print("\n❌ Failed to register found item.")
        print(f"Error: {e}")

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

menu()