from db import get_connection

def count_lost_items(a):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Items WHERE status = 'lost'")
    count = cursor.fetchone()[0]
    cursor.close()
    if a:
        return count
    else:
        return "There are currently no lost items reported." if count == 0 else "There is currently 1 lost item reported." if count == 1 else f"There are currently {count} lost items reported."

def count_reported_items(user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Items WHERE user_id = %s", (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count

def count_reunited_items(user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Items WHERE status = 'found and claimed' AND found_by = '%s'", (user_id,))
    reunited_items = cursor.fetchone()[0]
    cursor.close()
    return reunited_items


def count_reported_lost_items(user_id):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Items WHERE status != 'lost' and found_by = '%s'", (user_id,))
    lost = cursor.fetchone()[0]
    return lost

def get_people_helped(user_id):
    """
    Returns the number of distinct people a user has helped
    by finding and returning their lost items.
    """
    db_connection = get_connection()
    cursor = db_connection.cursor(dictionary=True)

    query = """
        SELECT COUNT(DISTINCT user_id) AS people_helped
        FROM Items
        WHERE found_by = %s
          AND status IN ('found and claimed', 'found but not claimed')
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    return result["people_helped"] if result else 0


def count_found_items_unclaimed(user_id, num=None):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Items WHERE status = 'found but not claimed' AND user_id = %s", (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return ("You have not reported any items." if count_reported_items(user_id) == 0 else "No items reported by you, have been found." if count == 0 else "1 item reported by you, has been found but not claimed." if count == 1 else f"{count} items reported by you, have been found but not claimed.") if not num else count

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