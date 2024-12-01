import mysql.connector
import json
import methods as m

#CLI Application Main 

if __name__ == "__main__":

    
    m.initialize_database()
    m.add_university("Harvard University", 42.3770, -71.1167)
    m.add_user("johndoe", "johndoe@harvard.edu", "John", "Doe", 1)
    m.add_user("janedoe", "janedoe@harvard.edu", "Jane", "Doe", 1)
    m.create_ride(1, 1, (42.3601, -71.0589), (42.3770, -71.1167), "2024-12-01 08:00:00", 3, "Uber")
    rides = m.view_rides(1)
    
    
    for ride in rides:
        print("Ride:", ride)
