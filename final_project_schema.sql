CREATE TABLE UNIVERSITY (
    university_id INT PRIMARY KEY AUTO_INCREMENT,
    university_name VARCHAR(50) UNIQUE,
    latitude DECIMAL (9,6),
    longitude DECIMAL (9,6)
);

CREATE TABLE USER (
    user_id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(15) NOT NULL, 
    email VARCHAR(50)  NOT NULL,
    first_name VARCHAR (50),
    last_name VARCHAR (50), 
    university_id INTEGER,
    current_lat DECIMAL (9,6),
    current_long DECIMAL (9,6),
    FOREIGN KEY (university_id) REFERENCES University(university_id)
    );

CREATE TABLE Ride (
    ride_id INT PRIMARY KEY AUTO_INCREMENT,
    created_by_user_id INT NOT NULL, -- User who created the ride
    university_id INT NOT NULL, -- University of all users in the ride
    pickup_lat DECIMAL(9,6) NOT NULL, -- Pickup latitude
    pickup_lon DECIMAL(9,6) NOT NULL, -- Pickup longitude
    dropoff_lat DECIMAL(9,6) NOT NULL, -- Dropoff latitude
    dropoff_lon DECIMAL(9,6) NOT NULL, -- Dropoff longitude
    ride_date DATETIME NOT NULL, -- Date and time of the ride
    seats_available INT NOT NULL, -- Number of available seats
    ride_status VARCHAR(20) NOT NULL, -- e.g., "Pending", "Completed"
    service_name VARCHAR(50) NOT NULL, -- e.g., "Uber", "Lyft"
    FOREIGN KEY (created_by_user_id) REFERENCES User(user_id),
    FOREIGN KEY (university_id) REFERENCES University(university_id)
);

CREATE TABLE Rides_Users (
    ride_user_id INT PRIMARY KEY AUTO_INCREMENT,
    ride_id INT NOT NULL, -- Links to the Ride
    user_id INT NOT NULL, -- Links to the User
    join_status VARCHAR(20) NOT NULL DEFAULT 'Pending', -- e.g., "Pending", "Approved"
    FOREIGN KEY (ride_id) REFERENCES Ride(ride_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);


