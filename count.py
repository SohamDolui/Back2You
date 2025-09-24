from db import get_connection

def count_lost_items():
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Items WHERE status = 'lost'")
    count = cursor.fetchone()[0]
    cursor.close()
    return "There are currently no lost items reported." if count == 0 else "There is currently 1 lost item reported." if count == 1 else f"There are currently {count} lost items reported."

def count_reported_items(user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Items WHERE user_id = %s", (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count

def count_found_items_unclaimed(user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Items WHERE status = 'found but not claimed' AND user_id = %s", (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return "You have not reported any items." if count_reported_items(user_id) == 0 else "No items reported by you, have been found." if count == 0 else "1 item reported by you, has been found but not claimed." if count == 1 else f"{count} items reported by you, have been found but not claimed."

def count_found_items_claimed(user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Items WHERE status = 'found and claimed' AND user_id = %s", (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count


def count_unread_messages(user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Messages WHERE receiver_id = %s AND is_read = 0", (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return "You have no unread messages." if count == 0 else "You have an unread message!" if count == 1 else f"You have {count} unread messages!"