from pymysql import connect
from pymysql.cursors import DictCursor

from flaskapp import config

# Make sure you have data in your tables. You should have used auto increment for
# primary keys, so all primary keys should start with 1


def get_connection():
    return connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_DATABASE,
        cursorclass=DictCursor,
    )

def get_events():
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events order by event_date")
            return cursor.fetchall()

def get_event(event_id):
    sql = "SELECT * FROM events WHERE event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            return cursor.fetchone()
        
def add_event(name, event_date, start_time, end_time, venue, invitation, maximum_attendees, planner, host, rental_items, note, image_path):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO events (name, event_date, start_time, end_time, venue_id, invitation_text, max_attendees, planner_id, rental_items, notes, image_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, event_date, start_time, end_time, venue, invitation, maximum_attendees, planner, rental_items, note, image_path))
            conn.commit()

def update_event(event_id, name, event_date, start_time, end_time, venue, invitation, maximum_attendees, planner, host, rental_items, note, image_path):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                UPDATE events
                SET name = %s, event_date = %s, start_time = %s, end_time = %s, venue_id = %s, invitation_text = %s, max_attendees = %s, planner_id = %s, rental_items = %s, notes = %s, image_path = %s
                WHERE event_id = %s
            """
            cursor.execute(query, (name, event_date, start_time, end_time, venue, invitation, maximum_attendees, planner, rental_items, note, image_path, event_id))
            conn.commit()

def get_people():
    sql = "SELECT * FROM people order by date_of_birth"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

def add_person(name, address, email, dob, phone, role):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO people (name, home_address, email, date_of_birth, mobile_phone, role)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, address, email, dob, phone, role))
            conn.commit()

def delete_person(person_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = "DELETE FROM people WHERE person_id = %s"
            cursor.execute(query, (person_id,))
            conn.commit()

def get_attendees(event_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT p.* FROM people p JOIN event_attendees ea ON p.person_id = ea.person_id WHERE ea.event_id = %s", (event_id,))
            return cursor.fetchall()

def add_attendee_event(event_id, attendee_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = "INSERT INTO event_attendees (event_id, person_id) VALUES (%s, %s)"
            cursor.execute(query, (event_id, attendee_id))
            conn.commit()

def remove_attendee_event(event_id, attendee_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = "DELETE FROM event_attendees WHERE event_id = %s AND person_id = %s"
            cursor.execute(query, (event_id, attendee_id))
            conn.commit()

def get_host(event_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT p.* FROM people p JOIN event_hosts eh ON p.person_id = eh.host_id WHERE eh.event_id = %s", (event_id,))
            return cursor.fetchone()

def set_host(person_id, event_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = "INSERT INTO event_hosts (event_id, host_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE host_id = %s"
            cursor.execute(query, (event_id, person_id, person_id))
            conn.commit()

def get_planner(event_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT p.* FROM people p JOIN events e ON p.person_id = e.planner_id WHERE e.event_id = %s", (event_id,))
            return cursor.fetchone()

def set_planner(person_id, event_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = "UPDATE events SET planner_id = %s WHERE event_id = %s"
            cursor.execute(query, (person_id, event_id))
            conn.commit()

def get_venues():
    """Returns a list of dictionaries representing all of the venues data"""
    sql = "SELECT * FROM venues order by rental_fee DESC"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            venues=cursor.fetchall()
            return venues
        
def add_venue(name, address, phone, fee, capacity):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO venues (name, address, contact_phone, rental_fee, max_attendees)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, address, phone, fee, capacity))
            conn.commit()

def get_venue_name(event_id):
    sql = "SELECT v.name FROM venues as v JOIN events as e ON v.venue_id = e.venue_id WHERE e.event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            return cursor.fetchone()

def get_host_details(event_id):
    sql = """
        SELECT p.name, p.email, p.mobile_phone 
        FROM people as p JOIN events as e ON p.person_id = e.host_id 
        WHERE e.event_id = %s
    """
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            return cursor.fetchone()

def get_planner_details(event_id):
    sql = """
        SELECT p.name, p.mobile_phone, p.email 
        FROM people as p JOIN events as e ON p.person_id = e.planner_id 
        WHERE e.event_id = %s
    """
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            return cursor.fetchone()
        
if __name__ == "__main__":

    print(f"All events: {get_events()}")
    print(f"Event info for event_id 1: {get_event(1)}")
    print(f"All people: {get_people()}")
    print(f"All attendees attending the event with event_id 1: {get_attendees(1)}")
