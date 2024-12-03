import mysql.connector
import json

# Open config for hard-coded db credentials
with open('credentials.config') as file:
        credentials = json.load(file)

def get_db_connection():
    """Establishes DB Connection -> none"""
    return mysql.connector.connect(
        host=credentials['database']['host'], 
        user=credentials['database']['user'],  
        password=credentials['database']['password'], 
        database=credentials['database']['database_name'] 
    )

def initialize_database():
    """Creates the database and tables if they do not exist"""
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

def add_arbitrary_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Populate University table
    cursor.execute("""
        INSERT INTO University (university_name, latitude, longitude)
        VALUES
            ('Harvard University', 42.3770, -71.1167),
            ('MIT', 42.3601, -71.0942),
            ('Stanford University', 37.4275, -122.1697)
        ON DUPLICATE KEY UPDATE latitude = VALUES(latitude), longitude = VALUES(longitude)
    """)

    # Fetch university IDs
    cursor.execute("SELECT university_id, university_name FROM University")
    universities = {name: uni_id for uni_id, name in cursor.fetchall()}

    users = [
        ('johndoe', 'johndoe@harvard.edu', 'John', 'Doe', universities['Harvard University']),
        ('janedoe', 'janedoe@harvard.edu', 'Jane', 'Doe', universities['Harvard University']),
        ('acresce1', 'acresce1@harvard.edu', 'Anton', 'Crescente', universities['Harvard University']),
        ('rcrist', 'rcrist@harvard.edu', 'Rose', 'Crist', universities['Harvard University']),
        ('jchad', 'jchad@harvard.edu', 'Jack', 'Chadwick', universities['Harvard University']),
        ('Harvardstudent3', 'harvardstudent3@harvard.edu', 'Harvard', 'Student', universities['Harvard University']),
        ('mike123', 'mike123@mit.edu', 'Mike', 'Smith', universities['MIT']),
        ('alice89', 'alice89@mit.edu', 'Alice', 'Johnson', universities['MIT']),
        ('bob_s', 'bob_s@stanford.edu', 'Bob', 'Stewart', universities['Stanford University']),
    ]

    for user in users:
        cursor.execute("""
            INSERT INTO User (username, email, first_name, last_name, university_id)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE username = username
        """, user)

        rides = [
        (1, 1, 42.3770, -71.1167, 42.3732, -71.1097, '2024-12-01 08:00:00', 3, 'Uber'),
        (2, 1, 42.3770, -71.1167, 42.3650, -71.1039, '2024-12-01 09:30:00', 4, 'Lyft'),
        (3, 1, 42.3770, -71.1167, 42.3700, -71.1078, '2024-12-01 10:45:00', 2, 'Uber')
    ]

    for ride in rides:
        cursor.execute("""
            INSERT INTO Ride (created_by_user_id, university_id, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, ride_date, seats_available, service_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE ride_date = VALUES(ride_date), seats_available = VALUES(seats_available)
        """, ride)

    conn.commit()
    conn.close()