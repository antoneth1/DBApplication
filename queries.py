import mysql.connector
import initialize as db
import os

def clear_console():
    """Clears the console screen."""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/MacOS
        os.system('clear')

def add_university(name, latitude, longitude):
    """Adds a university to the database"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO University (university_name, latitude, longitude)
        VALUES (%s, %s, %s)
    """, (name, latitude, longitude))
    conn.commit()
    conn.close()


def add_user(username, email, first_name, last_name, university_id):
    """Adds a user to the database"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO User (username, email, first_name, last_name, university_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, email, first_name, last_name, university_id))
    conn.commit()
    conn.close()


def create_ride(created_by_user_id, university_id, pickup, dropoff, ride_date, seats, service_name):
    """Adds a ride to the database specifying the user, how many seats are available, and the ride-share service"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Ride (created_by_user_id, university_id, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, ride_date, seats_available, ride_status, service_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending', %s)
    """, (created_by_user_id, university_id, pickup[0], pickup[1], dropoff[0], dropoff[1], ride_date, seats, service_name))
    conn.commit()
    conn.close()


def request_to_join_ride(ride_id, user_id):
    """Join existing ride"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Rides_Users (ride_id, user_id)
        VALUES (%s, %s)
    """, (ride_id, user_id))
    conn.commit()
    conn.close()


def get_universities() -> list:

    """Returns list of existing Universities in the DB"""

    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT University_name
    FROM University     
    """)
    university_list = [row[0] for row in cursor.fetchall()]

    conn.close()
    return university_list

# Get user ID by email or username
def get_user_id(username=None, email=None) -> int:
    """Retrieves the user ID by username or email."""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    if username:
        # Fetch user ID using username
        cursor.execute("""
            SELECT user_id
            FROM User
            WHERE username = %s
        """, (username,))
    elif email:
        # Fetch user ID using email
        cursor.execute("""
            SELECT user_id
            FROM User
            WHERE email = %s
        """, (email,))
    else:
        # Neither username nor email provided
        conn.close()
        raise ValueError("You must provide either a username or email to retrieve user ID.")
    
    result = cursor.fetchone()
    conn.close()
    
    # Return the user ID if found, else None
    return result[0] if result else None

def get_user_details_by_id(user_id):
    """Fetches the first and last name of a user by their user ID."""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT first_name, last_name
        FROM User
        WHERE user_id = %s
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result  # Returns a tuple: (first_name, last_name)

# Get University id by name
def get_university_id_by_name(university_name) -> str:
    """Most important function, returns the university ID with a given university name"""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT UNIVERSITY_ID
        FROM UNIVERSITY
        WHERE university_name = %s
 """, (university_name,))
    university = cursor.fetchone()
    conn.close()
    return university[0]

def get_location_by_university(university_name) -> tuple:
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
    """
    SELECT latitude, longitude
    FROM UNIVERSITY
    WHERE university_name = %s

    """, (university_name,))
    location = cursor.fetchone()
    conn.close()
    return location
        
# Approve a join request
def approve_join_request(ride_id, user_id):
    conn = db.get_db_connection()
    cursor = conn.cursor()

    # Update join status
    cursor.execute("""
        UPDATE Rides_Users
        SET join_status = 'Approved'
        WHERE ride_id = %s AND user_id = %s
    """, (ride_id, user_id))

    # Decrease seats available
    cursor.execute("""
        UPDATE Ride
        SET seats_available = seats_available - 1
        WHERE ride_id = %s
    """, (ride_id,))
    conn.commit()
    conn.close()

# View all rides for a university
def view_rides(university_id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Ride
        WHERE university_id = %s AND ride_status = 'Pending'
    """, (university_id,))
    rides = cursor.fetchall()
    conn.close()
    return rides