import queries as m
import mysql.connector
import json
import geocoder


#CLI Application Main 

if __name__ == "__main__":

    print("Welcome to Ride-Safe")
    print("\nAllow Ride-Safe to use your current location? \n1)Yes \n2)No")
    answer = input()
    
    g = geocoder.ip('me')  # 'me' retrieves your current IP-based location
    longitude = g.lng
    latitude = g.lat

    m.clear_console()

    print("\nRide-Safe\n\n1)Create an account \n2)Connect your Ride \n3)Find a Ride \n4)Quit")
    user_input = input()
    

    # Test for inputs 

    # Create an account
    if user_input == '1':
        '''User selects option 1 in ClI'''
        m.clear_console()
        print("Enter a username")
        username_input = input()
        print("Enter your university")
        university_input = input()
        print("Enter your email")
        email_input = input()
        print("First Name:")
        first_name = input()
        print("Last Name:")
        last_name = input()

        existing_universities = m.get_universities() #returns list

        if university_input not in existing_universities:
            m.add_university(university_input, latitude, longitude)
            
        university_id = m.get_university_id_by_name(university_input)
        m.add_user(username_input, email_input, first_name, last_name, university_id)
        m.clear_console()
        print("\nAccount successfully created!")
    
    # Connect a Ride
    if user_input == '2':
        m.clear_console()
        print("Ride-Safe\n\nSelect your ride share service\n1)Uber\n2)Lift")
        number_input = input()
        service = ''
        if number_input == '1':
            service = 'Uber'
        if number_input == '2':
            service = 'Lyft'
        m.clear_console()
        
        print("Ride-Safe\n")

        current_user_id = m.get_user_id(None, email_input)
        university_location = m.get_location_by_university(university_input)
        m.create_ride(current_user_id, university_id, pickup=(longitude, latitude), dropoff=university_location, seats=4, service_name=service)

        print("Ride Connected Successfully.")
            
    
    if user_input == '3':
        m.clear_console
        print("Ride-Safe")
        print(m.view_rides())
