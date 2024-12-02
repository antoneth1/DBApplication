import queries as m
import mysql.connector
import json
import geocoder
from datetime import datetime

# CLI Application Main
if __name__ == "__main__":

    username_input = None
    university_input = None
    email_input = None
    university_id = None
    
    print("Welcome to Ride-Safe")
    print("\nAllow Ride-Safe to use your current location? \n1)Yes \n2)No")
    answer = input()
    
    rose = None  
    while rose != '4':  

        g = geocoder.ip('me')  # 'me' retrieves your current IP-based location
        longitude = g.lng
        latitude = g.lat

        m.clear_console()

        print("\nRide-Safe\n\n1)Create an account \n2)Connect your Ride \n3)Find a Ride \n4)Quit")
        rose = input()  # Update rose with the user's input

        # Create an account
        if rose == '1':
            back_to_menu = False  # Flag for submenu control
            while not back_to_menu:
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

                existing_universities = m.get_universities()  # Returns list

                if university_input not in existing_universities:
                    m.add_university(university_input, latitude, longitude)

                university_id = m.get_university_id_by_name(university_input)
                m.add_user(username_input, email_input, first_name, last_name, university_id)
                m.clear_console()
                print("\nAccount successfully created!")
                print("Press 'b' to return to the main menu.")
                if input().lower() == 'b':
                    back_to_menu = True

        # Connect a Ride
        elif rose == '2':
            back_to_menu = False  # Flag for submenu control
            while not back_to_menu:
                if not username_input or not university_input or not email_input:
                    print("Please create an account first (Option 1).")
                    back_to_menu = True
                    continue

                m.clear_console()
                print("Ride-Safe\n\nSelect your ride share service\n1)Uber\n2)Lyft")
                number_input = input()
                service = 'Uber' if number_input == '1' else 'Lyft'
                m.clear_console()

                print("Ride-Safe\n")

                try:
                    current_user_id = m.get_user_id(None, email_input)
                    university_location = m.get_location_by_university(university_input)
                    m.create_ride(
                        current_user_id,
                        university_id,
                        pickup=(longitude, latitude),
                        dropoff=university_location,
                        ride_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        seats=4,
                        service_name=service,
                    )
                    print("Ride Connected Successfully.")
                except Exception as e:
                    print(f"Error: {e}. Unable to connect your ride.")

                print("Press 'b' to return to the main menu.")
                if input().lower() == 'b':
                    back_to_menu = True

        # Find a Ride
        elif rose == '3':
            back_to_menu = False  # Flag for submenu control
            while not back_to_menu:
                if not university_id:
                    print("Please create an account first (Option 1).")
                    back_to_menu = True
                    continue

                m.clear_console()
                print("Ride-Safe")
                rides = m.view_rides(university_id)
                for ride in rides:
                    print(ride)

                print("Press 'b' to return to the main menu.")
                if input().lower() == 'b':
                    back_to_menu = True

        # Quit
        elif rose == '4':
            print("Exiting Ride-Safe. Have a great day!")
            m.clear_console()

        # Invalid input
        else:
            print("Invalid option. Please choose a valid option.")
