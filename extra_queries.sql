-- List all users who have joined rides, along with the ride details
SELECT u.first_name, u.last_name, r.service_name, r.pickup_lat, r.pickup_lon, r.dropoff_lat, r.dropoff_lon
FROM Rides_Users ru
INNER JOIN User u ON ru.user_id = u.user_id
INNER JOIN Ride r ON ru.ride_id = r.ride_id;

-- List all rides created by users, including those with no join requests
SELECT r.ride_id, r.service_name, r.pickup_lat, r.pickup_lon, r.dropoff_lat, r.dropoff_lon, ru.user_id AS joined_user_id
FROM Ride r
LEFT JOIN Rides_Users ru ON r.ride_id = ru.ride_id;

-- RIGHT JOIN: List all users who have requested to join rides, even if their join status is not approved
SELECT u.user_id, u.first_name, u.last_name, ru.ride_id, ru.join_status
FROM User u
RIGHT JOIN Rides_Users ru ON u.user_id = ru.user_id;

-- FULL OUTER JOIN: List all users and rides, including those who haven’t joined or created a ride 
SELECT u.user_id, u.first_name, u.last_name, r.ride_id, r.service_name
FROM User u
LEFT JOIN Rides_Users ru ON u.user_id = ru.user_id
LEFT JOIN Ride r ON ru.ride_id = r.ride_id
UNION
SELECT u.user_id, u.first_name, u.last_name, r.ride_id, r.service_name
FROM Ride r
LEFT JOIN Rides_Users ru ON r.ride_id = ru.ride_id
LEFT JOIN User u ON ru.user_id = u.user_id;
