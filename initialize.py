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