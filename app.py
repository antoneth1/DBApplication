import queries as m
import initialize as i
import mysql.connector
import json
import geocoder
from datetime import datetime

# CLI Application Main
if __name__ == "__main__":

    i.initialize_database()
    i.add_arbitrary_data()
    

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

                university_coords = geocoder.osm(
                location=university_input,
                url="https://nominatim.openstreetmap.org/search",  
                headers={"User-Agent": "Ride-Safe Application"}  
)
                uni_latitude = university_coords.lat
                uni_longitude = university_coords.lng
                existing_universities = m.get_universities()  # Returns list

                if university_input not in existing_universities:
                    m.add_university(university_input, uni_latitude, uni_longitude)

                university_id = m.get_university_id_by_name(university_input)
                m.add_user(username_input, email_input, first_name, last_name, university_id)
                m.clear_console()
                print("\nAccount successfully created!")
                print("Press 'b' to return to the main menu.")
                if input().lower() == 'b':
                    back_to_menu = True

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

                try:
                    # Use cached coordinates if available, otherwise fetch them
                    if not university_id or not uni_latitude or not uni_longitude:
                        ride_to_location = geocoder.osm(
                        location=university_input,  # Location to search for
                        url="https://nominatim.openstreetmap.org/search",  # Default OSM server URL
                        headers={"User-Agent": "Ride-Safe Application"}  # Required User-Agent header
)
                        uni_latitude = ride_to_location.lat
                        uni_longitude = ride_to_location.lng

                        if uni_latitude is None or uni_longitude is None:
                            raise ValueError(f"Unable to retrieve the location for {university_input}. Please check the university name.")

                    # Retrieve the current user's ID
                    current_user_id = m.get_user_id(None, email_input)

                    # Create the ride
                    m.create_ride(
                        current_user_id,
                        university_id,
                        pickup=(latitude, longitude),
                        dropoff=(uni_latitude, uni_longitude),
                        ride_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        seats=4,
                        service_name=service,
                    )
                    print("Ride Connected Successfully.")

                except ValueError as ve:
                    print(f"Error: {ve}")
                except Exception as e:
                    print(f"Unexpected error: {e}. Unable to connect your ride.")

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
                print("Available Rides:\n")

                # Fetch available rides for the user's university
                rides = m.view_rides(university_id)
                
                if not rides:
                    print("No rides available for your university.")
                    print("Press 'b' to return to the main menu.")
                    if input().lower() == 'b':
                        back_to_menu = True
                        continue

                # Display rides in a user-friendly format
                ride_map = {}
                for index, ride in enumerate(rides, start=1):
                    # Fetch ride details
                    ride_id = ride[0]
                    created_by_user_id = ride[1]
                    pickup_lat = ride[3]
                    pickup_lon = ride[4]
                    dropoff_lat = ride[5]
                    dropoff_lon = ride[6]
                    ride_date = ride[7]
                    seats_available = ride[8]
                    service_name = ride[10]

                    # Fetch ride owner's name
                    owner_details = m.get_user_details_by_id(created_by_user_id)
                    owner_first_name = owner_details[0]
                    owner_last_name = owner_details[1]

                    # Display ride
                    print(f"{index}. {owner_first_name} {owner_last_name}'s Ride")
                    print(f"   Service: {service_name}")
                    print(f"   Pickup: ({pickup_lat}, {pickup_lon})")
                    print(f"   Dropoff: ({dropoff_lat}, {dropoff_lon})")
                    print(f"   Date: {ride_date}")
                    print(f"   Seats Available: {seats_available}")
                    print("-" * 30)

                    # Map user input to ride ID
                    ride_map[str(index)] = ride_id

                # Allow user to join a ride
                print("Enter the number of the ride you'd like to join, or press 'b' to return to the main menu.")
                user_choice = input().lower()

                if user_choice == 'b':
                    back_to_menu = True
                    continue

                if user_choice in ride_map:
                    selected_ride_id = ride_map[user_choice]

                    # Request to join the ride
                    try:
                        current_user_id = m.get_user_id(None, email_input)
                        m.request_to_join_ride(selected_ride_id, current_user_id)
                        print("Successfully requested to join the ride.")
                        m.approve_join_request(selected_ride_id, current_user_id)
                        print("Ride join request approved!")
                        
                    except Exception as e:
                        print(f"Error: {e}. Unable to join the ride.")

                    print("Press 'b' to return to the main menu.")
                    if input().lower() == 'b':
                        back_to_menu = True

        # Quit
        elif rose == '4':
            print("Exiting Ride-Safe. Have a great day!")

        # Invalid input
        else:
            print("Invalid option. Please choose a valid option.")
