
def main():
    base_ui()
    

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
    elif choice == 2: make_itinerary()
    elif choice == 3: show_itineraries()
    elif choice == 4: exit()
    else: print("Invalid Input, try again")


def make_itinerary():
    print("")

def show_itineraries():
    print("")

main()
