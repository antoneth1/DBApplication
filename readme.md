### Intro to Database Systems Final Project

## University Ride-Share Application LVM

This application aims to facilitate communication between college students in similar vicinities looking for rides via ride-share services. The goal is to reduce the cost of utilizing these services, amplify safety, and foster a sense of community between students. 

This repo was created as a least viable model (LVM) of the application idea, and is intended to demonstrate its functionality via a command-line-interface (CLI) version of the application. 

Before advancing any further, please familiarize yourself with the database schema in "final_project_schema.sql" to better understand the context of querying operations within the app.

On use, the user--having the necessary dependencies installed (noted in dependencies.txt)--should be able to run app.py, where they will be prompted the following: 

# Welcome to Ride Safe

Allow Ride Safe you use your current location?
1. yes
2. no 

The CLI application is reliant on user terminal input, and will display which numbers to enter for various options. Here is the rest of the output after running app.py:

Ride-Safe

1. Create an account 
2. Connect your Ride 
3. Find a Ride 
4. Quit

The various options require further input from the user, which then is used to add data records to the data base via query methods in queries.py. 

**All users must create an account before they are able to use the other functionalities of the CLI application, as they are dependent on the inputs from the create an account option**

It is important to note the "Connect your Ride" option does not have the functionality to actually connect rides from various ride-share services, but is intended to create a hypothetical ride via the create_ride function. 

Similarly, the "Find a Ride" option will display pre-created rides in the database initialized by running the application via an arbitrary data insertion method. This means only a select few universities will display rides, 

*for this reason users should enter 'Harvard University' as their university input when creating an account.*

This CLI application is intended to show the functionality of the relational database required for the B2E mobile app. 




