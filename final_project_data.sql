-- Populate University Table
INSERT INTO University (university_name, latitude, longitude)
VALUES
    ('Harvard University', 42.3770, -71.1167),
    ('MIT', 42.3601, -71.0942),
    ('Stanford University', 37.4275, -122.1697);

-- Populate User Table
INSERT INTO User (username, email, first_name, last_name, university_id, current_lat, current_long)
VALUES
    ('johndoe', 'johndoe@harvard.edu', 'John', 'Doe', 1, 42.3601, -71.0589),
    ('janedoe', 'janedoe@harvard.edu', 'Jane', 'Doe', 1, 42.3732, -71.1074),
    ('mike123', 'mike123@mit.edu', 'Mike', 'Smith', 2, 42.3624, -71.0912),
    ('alice89', 'alice89@mit.edu', 'Alice', 'Johnson', 2, 42.3655, -71.1009),
    ('bob_s', 'bob_s@stanford.edu', 'Bob', 'Stewart', 3, 37.4241, -122.1661),
    ('clara_w', 'clara_w@stanford.edu', 'Clara', 'Wilson', 3, 37.4288, -122.1739),
    ('peter_pan', 'peter@mit.edu', 'Peter', 'Pan', 2, 42.3610, -71.0950),
    ('anna_k', 'anna@harvard.edu', 'Anna', 'Kim', 1, 42.3780, -71.1172),
    ('david_s', 'david@stanford.edu', 'David', 'Scott', 3, 37.4267, -122.1699),
    ('linda_b', 'linda@harvard.edu', 'Linda', 'Brown', 1, 42.3692, -71.1062);

-- Populate Ride Table
INSERT INTO Ride (service_name, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, ride_date, seats_available, ride_status, university_id)
VALUES
    ('Uber', 42.3601, -71.0589, 42.3770, -71.1167, '2024-12-01 08:00:00', 3, 'Pending', 1),
    ('Lyft', 42.3624, -71.0912, 42.3770, -71.1167, '2024-12-01 09:30:00', 2, 'Pending', 1),
    ('Uber', 42.3655, -71.1009, 42.3770, -71.1167, '2024-12-02 07:45:00', 4, 'Completed', 1),
    ('Uber', 37.4288, -122.1739, 37.4275, -122.1697, '2024-12-01 10:15:00', 2, 'Pending', 3),
    ('Lyft', 37.4241, -122.1661, 37.4275, -122.1697, '2024-12-02 11:00:00', 1, 'Completed', 3),
    ('Uber', 42.3732, -71.1074, 42.3601, -71.0942, '2024-12-01 13:30:00', 3, 'Pending', 2),
    ('Lyft', 42.3624, -71.0912, 42.3601, -71.0942, '2024-12-02 15:00:00', 4, 'Completed', 2),
    ('Uber', 37.4267, -122.1699, 37.4275, -122.1697, '2024-12-03 17:00:00', 2, 'Pending', 3),
    ('Lyft', 42.3780, -71.1172, 42.3770, -71.1167, '2024-12-01 18:30:00', 1, 'Completed', 1),
    ('Uber', 42.3692, -71.1062, 42.3770, -71.1167, '2024-12-01 20:45:00', 2, 'Pending', 1),
    ('Lyft', 42.3610, -71.0950, 42.3770, -71.1167, '2024-12-02 21:00:00', 3, 'Completed', 1),
    ('Uber', 37.4241, -122.1661, 37.4275, -122.1697, '2024-12-02 22:15:00', 1, 'Pending', 3);
