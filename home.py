import mysql.connector as ms
from db import get_connection
import os

def menu():
    print("Back2You")
    print("Welcome to the Home Menu")
    print("Report Item (1):")
    print("Browse/Search Items (2):")
    print("Messages (3):")
    print("Global Chat (4):")
    print("My Profile (5):")
    print("Logout (6):")
    print("Exit (0):")
    inp = int(input("Enter your choice: "))
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
        return False
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
    inp = int(input("Enter your choice: "))
    if inp == 1:
        print("Reporting a Lost Item")
        ReportLostItem()
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

def ReportLostItem():
    item_name = input("Enter the name of the lost item: ")
    item_description = input("Enter a description of the lost item: ")
    chrone = input("Enter when it was lost: ")
    contact_info = input("Enter your contact information: ")
    print(f"Lost Item Reported: {item_name},\non {chrone},\nDescription: {item_description},\nContact Info: {contact_info}")