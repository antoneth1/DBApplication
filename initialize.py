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
    """Fills the database with an artificial dataset for testing."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Populate University table
    cursor.execute("""
        INSERT INTO University (university_name, latitude, longitude)
        VALUES
            ('Harvard University', 42.3770, -71.1167),
            ('MIT', 42.3601, -71.0942),
            ('Stanford University', 37.4275, -122.1697)
        ON DUPLICATE KEY UPDATE university_name = university_name
    """)
    
    # Populate User table
    cursor.execute("""
        INSERT INTO User (username, email, first_name, last_name, university_id)
        VALUES
            ('johndoe', 'johndoe@harvard.edu', 'John', 'Doe', 1),
            ('janedoe', 'janedoe@harvard.edu', 'Jane', 'Doe', 1),
            ('mike123', 'mike123@mit.edu', 'Mike', 'Smith', 2),
            ('alice89', 'alice89@mit.edu', 'Alice', 'Johnson', 2),
            ('bob_s', 'bob_s@stanford.edu', 'Bob', 'Stewart', 3),
            ('clara_w', 'clara_w@stanford.edu', 'Clara', 'Wilson', 3),
            ('peter_pan', 'peter@mit.edu', 'Peter', 'Pan', 2),
            ('anna_k', 'anna@harvard.edu', 'Anna', 'Kim', 1),
            ('david_s', 'david@stanford.edu', 'David', 'Scott', 3),
            ('linda_b', 'linda@harvard.edu', 'Linda', 'Brown', 1),
            ('emma_c', 'emma@harvard.edu', 'Emma', 'Carter', 1),
            ('noah_g', 'noah@mit.edu', 'Noah', 'Green', 2),
            ('oliver_s', 'oliver@stanford.edu', 'Oliver', 'Smith', 3),
            ('mia_l', 'mia@harvard.edu', 'Mia', 'Lee', 1),
            ('sophia_t', 'sophia@stanford.edu', 'Sophia', 'Taylor', 3)
        ON DUPLICATE KEY UPDATE username = username
    """)

    # Populate Ride table
    cursor.execute("""
        INSERT INTO Ride (created_by_user_id, university_id, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, ride_date, seats_available, ride_status, service_name)
        VALUES
            (1, 1, 42.3601, -71.0589, 42.3770, -71.1167, '2024-12-01 08:00:00', 3, 'Pending', 'Uber'),
            (2, 1, 42.3624, -71.0912, 42.3770, -71.1167, '2024-12-01 09:30:00', 2, 'Pending', 'Lyft'),
            (3, 1, 42.3655, -71.1009, 42.3770, -71.1167, '2024-12-02 07:45:00', 4, 'Completed', 'Uber'),
            (4, 3, 37.4288, -122.1739, 37.4275, -122.1697, '2024-12-01 10:15:00', 2, 'Pending', 'Uber'),
            (5, 3, 37.4241, -122.1661, 37.4275, -122.1697, '2024-12-02 11:00:00', 1, 'Completed', 'Lyft'),
            (6, 2, 42.3732, -71.1074, 42.3601, -71.0942, '2024-12-01 13:30:00', 3, 'Pending', 'Uber'),
            (7, 2, 42.3624, -71.0912, 42.3601, -71.0942, '2024-12-02 15:00:00', 4, 'Completed', 'Lyft'),
            (8, 3, 37.4267, -122.1699, 37.4275, -122.1697, '2024-12-03 17:00:00', 2, 'Pending', 'Uber'),
            (9, 1, 42.3780, -71.1172, 42.3770, -71.1167, '2024-12-01 18:30:00', 1, 'Completed', 'Lyft'),
            (10, 1, 42.3692, -71.1062, 42.3770, -71.1167, '2024-12-01 20:45:00', 2, 'Pending', 'Uber'),
            (11, 1, 42.3610, -71.0950, 42.3770, -71.1167, '2024-12-02 21:00:00', 3, 'Completed', 'Lyft'),
            (12, 3, 37.4241, -122.1661, 37.4275, -122.1697, '2024-12-02 22:15:00', 1, 'Pending', 'Uber')
        ON DUPLICATE KEY UPDATE ride_id = ride_id
    """)

    conn.commit()
    conn.close()
