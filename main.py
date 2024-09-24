from datetime import datetime
from itertools import zip_longest
from services import aircanada_external, turkish_external

def main():
    add_flight()
    

def base_ui():
    enter_choice = int(input("""System Access: 
    1) Login
    2) Sign Up
    Enter Choice From (1 to 2): """))
    if enter_choice == 1:
        login_screen()
    elif enter_choice == 2:
        print("Sign up is not yet supported, please wait 3>")
    else: print("Invalid Input, try again")



def login_screen():
    username = str(input("Enter Username: "))
    password = str(input("Enter Password: "))
    customer_page(username)


def customer_page(username:str):
    choice = int(input(f"""Welcome {username} | Customer:
    1) View Profile 
    2) Make itinerary
    3) List my itineraries
    4) Logout
    Enter your choice (from 1 to 4): """))
    if choice == 1: print("view profile is not supported yet")
    elif choice == 2: add_flight()
    elif choice == 3: show_itineraries()
    elif choice == 4: exit()
    else: print("Invalid Input, try again")

def create_itinerary():
    
    choice = int(input(f"""Create Your itinerary:
    1) Add Flight
    2) Add Hotel
    3) Reseve itinerary
    4) Cancel itinerary
    Enter your choice (from 1 to 4): """))
    if choice == 1:
        add_flight()


    
def add_flight():
    try:
        from_place = str(input("Enter From: "))
        from_date = str(input("Enter From Date (dd-mm-yy): "))
        to_place = str(input("Enter To: "))
        to_date = str(input("Enter Return Date (dd-mm-yy): "))
        infants = int(input("Enter # of infants: "))
        children = int(input("Enter # of children: "))
        adults = int(input("Enter # of adults: "))

        fromDateParsed = datetime.strptime(from_date, "%d-%m-%y")
        toDateParsed = datetime.strptime(to_date, "%d-%m-%y")
        
               
        aircanada_flights = aircanada_external.AirCanadaOnlineAPI.get_flights(from_place, to_place)
        turkish_flights = turkish_external.TurkishOnlineAPI.get_available_flights(from_place, to_place)

        print("Select a flight:\n")
        count = 0

        
        for item1 in aircanada_flights:
           
            flightFromDate = datetime.strptime(item1.getFromDate(), "%d-%m-%y")
            flightToDate = datetime.strptime(item1.getToDate(), "%d-%m-%y")

           
            if fromDateParsed == flightFromDate and toDateParsed == flightToDate:
                count += 1
                print(f"{count}) ", item1, f"#infants {infants} #children {children} # adults {adults}")

       
        for item2 in turkish_flights:
            
            flightFromDate = datetime.strptime(item2.getFromDate(), "%d-%m-%y")
            flightToDate = datetime.strptime(item2.getToDate(), "%d-%m-%y")

            
            if fromDateParsed == flightFromDate and toDateParsed == flightToDate:
                count += 1
                print(f"{count}) ", item2, f"#infants {infants} #children {children} # adults {adults}")

        
        if count > 0:
            choice = int(input(f"Enter Your choice from (1 to {count}): "))
        else:
            print("No flights available for the given date range.")
    except Exception as e:
        print(e)
        add_flight()    
 
        
def show_itineraries():
    print("")

main()
