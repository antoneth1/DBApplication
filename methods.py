import mysql.connector
import json

# Open config for hard-coded db credentials
with open('credentials.config') as file:
        credentials = json.load(file)

# Establish MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host= credentials['database']['host'],
        user= credentials['database']['user'],  # Replace with your MySQL username
        password= credentials['database']['password'],  # Replace with your MySQL password
        database= credentials['database']['database_name']
    )

# Initialize database and tables
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS rideshare_db")
    cursor.execute("USE rideshare_db")

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS University (
            university_id INT AUTO_INCREMENT PRIMARY KEY,
            university_name VARCHAR(50) UNIQUE NOT NULL,
            latitude DECIMAL(9,6),
            longitude DECIMAL(9,6)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(15) NOT NULL,
            email VARCHAR(50) NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            university_id INT NOT NULL,
            FOREIGN KEY (university_id) REFERENCES University(university_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ride (
            ride_id INT AUTO_INCREMENT PRIMARY KEY,
            created_by_user_id INT NOT NULL,
            university_id INT NOT NULL,
            pickup_lat DECIMAL(9,6) NOT NULL,
            pickup_lon DECIMAL(9,6) NOT NULL,
            dropoff_lat DECIMAL(9,6) NOT NULL,
            dropoff_lon DECIMAL(9,6) NOT NULL,
            ride_date DATETIME NOT NULL,
            seats_available INT NOT NULL,
            ride_status VARCHAR(20) NOT NULL,
            service_name VARCHAR(50) NOT NULL,
            FOREIGN KEY (created_by_user_id) REFERENCES User(user_id),
            FOREIGN KEY (university_id) REFERENCES University(university_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rides_Users (
            ride_user_id INT AUTO_INCREMENT PRIMARY KEY,
            ride_id INT NOT NULL,
            user_id INT NOT NULL,
            join_status VARCHAR(20) NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (ride_id) REFERENCES Ride(ride_id),
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )
    """)
    conn.commit()
    conn.close()

# Add a university
def add_university(name, latitude, longitude):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO University (university_name, latitude, longitude)
        VALUES (%s, %s, %s)
    """, (name, latitude, longitude))
    conn.commit()
    conn.close()

# Add a user
def add_user(username, email, first_name, last_name, university_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO User (username, email, first_name, last_name, university_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, email, first_name, last_name, university_id))
    conn.commit()
    conn.close()

# Create a ride
def create_ride(created_by_user_id, university_id, pickup, dropoff, ride_date, seats, service_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Ride (created_by_user_id, university_id, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, ride_date, seats_available, ride_status, service_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending', %s)
    """, (created_by_user_id, university_id, pickup[0], pickup[1], dropoff[0], dropoff[1], ride_date, seats, service_name))
    conn.commit()
    conn.close()

# Request to join a ride
def request_to_join_ride(ride_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Rides_Users (ride_id, user_id)
        VALUES (%s, %s)
    """, (ride_id, user_id))
    conn.commit()
    conn.close()

# Approve a join request
def approve_join_request(ride_id, user_id):
    conn = get_db_connection()
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Ride
        WHERE university_id = %s AND ride_status = 'Pending'
    """, (university_id,))
    rides = cursor.fetchall()
    conn.close()
    return rides