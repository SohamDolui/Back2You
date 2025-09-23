from dotenv import load_dotenv
import mysql.connector as ms
import os

load_dotenv()

conn = None

def get_connection():
    global conn
    if conn is not None:
        return conn
    else:
        conn = ms.connect(host='localhost', user='root', password=os.getenv("ROOT_PASSWORD"), use_pure = True)
        cursor = conn.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS Back2You')
        cursor.execute('USE Back2You')
        cursor.execute('CREATE TABLE IF NOT EXISTS ' \
        'Users '
        '(id INT AUTO_INCREMENT PRIMARY KEY, ' \
        'username VARCHAR(50), ' \
        'password VARCHAR(50), ' \
        'email VARCHAR(100), ' \
        'points INT DEFAULT 0, ' \
        'points_history TEXT, ' \
        'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);')

        cursor.execute('CREATE TABLE IF NOT EXISTS ' \
        'Items ' \
        '(item_id INT PRIMARY KEY, ' \
        'item_name VARCHAR(100), ' \
        'item_description TEXT,' \
        'user_id INT, ' \
        'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ' \
        'category VARCHAR(50), ' \
        'bounty_points INT DEFAULT(10), status ENUM("lost", "found but not claimed", "found and claimed"), ' \
        'item_image_url VARCHAR(2000), ' \
        'found_description TEXT, ' \
        'found_by INT, ' \
        'found_image_url VARCHAR(2000), ' \
        'FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE);')

        cursor.execute('CREATE TABLE IF NOT EXISTS '
        'Messages ' \
        '(message_id INT PRIMARY KEY, ' \
        'sender_id INT, ' \
        'receiver_id INT, ' \
        'content TEXT, ' \
        'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ' \
        'FOREIGN KEY (sender_id) REFERENCES Users(id) ON DELETE CASCADE, ' \
        'FOREIGN KEY (receiver_id) REFERENCES Users(id) ON DELETE CASCADE);')

        cursor.execute('CREATE TABLE IF NOT EXISTS '
        'GlobalChat ' \
        '(chat_id INT PRIMARY KEY, ' \
        'user_id INT, ' \
        'message TEXT, ' \
        'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ' \
        'FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE);')
        conn.commit()
        cursor.close()
        return conn