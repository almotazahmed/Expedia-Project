from datetime import datetime
from APIs.turkish_external import TurkishOnlineAPI
from APIs.aircanada_external import AirCanadaOnlineAPI
from APIs.hilton_external import HiltonHotelAPI
from APIs.marriott_external import MarriottHotelAPI

###########################################################################################################

class UserAccount:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def login(self, username: str, password: str) -> bool:
        return username == self.username and password == self.password

###########################################################################################################

class Customer(UserAccount):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.itineraries = []

    def view_profile(self):
        print(f"Hello {self.username.capitalize()}, this is your profile.")

    def add_itinerary(self):
        itinerary = Itinerary()
        self.itineraries.append(itinerary)
        itinerary.add_reservations()

    def list_itineraries(self):
        for idx1, itinerary in enumerate(self.itineraries, start=1):
            for idx2, reservation in enumerate(itinerary.reservations, start=1):
                print(f"{idx1}: {idx2}: {reservation.selected_item}")


###########################################################################################################


class Itinerary:
    def __init__(self):
        self.reservations = []
        self.total_cost = 0


    def add_reservations(self):
        while True:
            try:
                choice = int(input(f"""Create you itinerary:
                        1) Add flight
                        2) Add Hotel
                        3) Reserve itinerary
                        4) Cancel itinerary
                        Enter your choice (from 1 to 4): """))
            except ValueError:
                print("Invalid input, please enter a number (1, 2, 3 or 4).")
                continue

            if choice == 1:
                reservation = FlightReservation()
                self.reservations.append(reservation)
                reservation.add_flight()
                self.total_cost += reservation.selected_item.cost
            elif choice == 2:
                print("not supported yet")
                reservation = HotelReservation()
                self.reservations.append(reservation)
                reservation.add_hotel()
                self.total_cost += reservation.selected_item.cost
            elif choice == 3:
                self.reserve_itinerary()
                break
            elif choice == 4:
                self.cancel_itinerary()
                break
            else:
                print("Invalid input, please enter a number (1, 2, 3 or 4).")

    def reserve_itinerary(self):
        if not self.reservations:
            print("No reservations in the itinerary to reserve.")
            return

        successful_reservations = []
        for reservation in self.reservations:
            if reservation.reserve():
                successful_reservations.append(reservation)

        if successful_reservations:
            print(f"Successfully reserved {len(successful_reservations)} items in your itinerary.")
            print(f"Total cost of itinerary: {self.total_cost}")
        else:
            print("No reservations were successfully made.")

    def cancel_itinerary(self):
        if not self.reservations:
            print("No reservations to cancel.")
            return

        for reservation in self.reservations:
            reservation.cancel()

        self.reservations.clear()
        self.total_cost = 0
        print("Itinerary canceled and all reservations removed.")


###########################################################################################################


class Reservation:
    def __init__(self):
        self.item_type = None
        self.selected_item = None
        self.confirmation_id = None

    def reserve(self):
        pass
    def cancel(self):
        pass


###########################################################################################################


class FlightReservation(Reservation):
    def __init__(self):
        super().__init__()
        self.item_type = "flight"

    def add_flight(self):
        from_loc = input("Enter departure location: ")
        datetime_from = input_date("Enter departure date (DD-MM-YYYY): ")
        to_loc = input("Enter destination: ")
        datetime_to = input_date("Enter return date (DD-MM-YYYY): ")

        num_infants = int(input("Enter number of infants: "))
        num_children = int(input("Enter number of children: "))
        num_adults = int(input("Enter number of adults: "))

        available_flights_objects = self.get_available_flights(
            from_loc, datetime_from, to_loc, datetime_to,num_infants, num_children, num_adults)

        if available_flights_objects:
            self.selected_item =  select_item(available_flights_objects, self.item_type)
        else:
            print("No flights available for the selected dates and locations.")


    @staticmethod
    def get_available_flights(from_loc, datetime_from, to_loc, datetime_to, infants, children, adults):
        available_flights_objects = []

        turkish_api = TurkishOnlineAPI()
        turkish_flights_data = turkish_api.get_available_flights()
        for flight_object in turkish_flights_data:
            flight = Flight(
                flight_object = flight_object,
                flight_company ="Turkish Airlines",
                from_loc=from_loc,
                datetime_from=flight_object.datetime_from,
                to_loc=to_loc,
                datetime_to=flight_object.datetime_to,
                num_infants=infants,
                num_children=children,
                num_adults=adults,
                cost = flight_object.cost
            )
            available_flights_objects.append(flight)

        aircanada_api = AirCanadaOnlineAPI()
        aircanada_flights_data = aircanada_api.get_flights(from_loc, datetime_from, to_loc, datetime_to, adults, children)
        for flight_object in aircanada_flights_data:
            flight = Flight(
                flight_object=flight_object,
                flight_company="AirCanada",
                from_loc=from_loc,
                datetime_from=flight_object.date_time_from,
                to_loc=to_loc,
                datetime_to=flight_object.date_time_to,
                num_infants=infants,
                num_children=children,
                num_adults=adults,
                cost = flight_object.price
            )
            available_flights_objects.append(flight)

        return available_flights_objects

    def reserve(self):
        if self.selected_item is not None:
            if self.selected_item.flight_company == "Turkish Airlines":
                turkish_api = TurkishOnlineAPI()
                self.confirmation_id = turkish_api.reserve_flight([], self.selected_item.flight_object)
                return True
            elif self.selected_item.flight_company == "AirCanada":
                aircanada_api = AirCanadaOnlineAPI()
                self.confirmation_id = aircanada_api.reserve_flight(self.selected_item.flight_object, [])
                return True
            else:
                print("Unknown airline.")
                return False
        else:
            print("No flights available for the selected dates and locations.")
            return False

    def cancel(self):
        if self.confirmation_id is not None:
            if self.selected_item.flight_company == "Turkish Airlines":
                turkish_api = TurkishOnlineAPI()
                return turkish_api.cancel_flight(self.confirmation_id)
            elif self.selected_item.flight_company == "AirCanada":
                aircanada_api = AirCanadaOnlineAPI()
                return aircanada_api.cancel_flight(self.confirmation_id)
            else:
                print("Unknown airline.")
                return False
        else:
            print("No reservation found to cancel.")
            return False



class Flight:
    def __init__(self,flight_object = None, flight_company=None, from_loc=None, datetime_from=None, to_loc=None,
                 datetime_to=None, num_infants=0, num_children=0, num_adults=0, cost=0):
        self.flight_object = flight_object
        self.flight_company = flight_company
        self.from_loc = from_loc
        self.datetime_from = datetime_from
        self.to_loc = to_loc
        self.datetime_to = datetime_to
        self.num_infants = num_infants
        self.num_children = num_children
        self.num_adults = num_adults
        self.cost = cost

    def __str__(self):
        return (f"{self.flight_company}: Cost {self.cost} - From: {self.from_loc} on {self.datetime_from} "
                f"To: {self.to_loc} on {self.datetime_to} - "
                f"#Infants: {self.num_infants} - #Children: {self.num_children} - #Adults: {self.num_adults}")


###########################################################################################################


class HotelReservation(Reservation):
    def __init__(self):
        super().__init__()
        self.item_type = "hotel"

    def add_hotel(self):
        room_type = input("Enter room type: ")
        datetime_from = input_date("Enter from date (DD-MM-YYYY): ")
        datetime_to = input_date("Enter to date (DD-MM-YYYY): ")
        location = input("Enter location: ")

        num_rooms_needed = int(input("Enter number of rooms: "))
        num_children = int(input("Enter number of children: "))
        num_adults = int(input("Enter number of adults: "))

        available_rooms_objects = self.get_available_rooms(
            room_type, datetime_from, datetime_to, location, num_rooms_needed, num_children, num_adults)

        if available_rooms_objects:
            self.selected_item =  select_item(available_rooms_objects, self.item_type)
        else:
            print("No Rooms available for the selected dates and locations.")


    @staticmethod
    def get_available_rooms(room_type, datetime_from, datetime_to, location, num_rooms_needed, children, adults):
        available_rooms_objects = []

        hilton_hotel_api = HiltonHotelAPI()
        hilton_rooms_data = hilton_hotel_api.search_rooms(location, datetime_from, datetime_to, adults, children,
                                                          num_rooms_needed)
        for room_object in hilton_rooms_data:
            room = Room(
                room_object = room_object,
                hotel_name ="Hilton",
                room_type = room_object.room_type,
                rooms_available = room_object.available,
                num_rooms_needed = num_rooms_needed,
                price_per_night = room_object.price_per_night,
                date_from=datetime_from,
                date_to=datetime_to,
                location=location,
                num_children = children,
                num_adults = adults,
            )
            available_rooms_objects.append(room)

        marriott_hotel_api = MarriottHotelAPI()
        marriott_rooms_data = marriott_hotel_api.search_available_rooms(location, datetime_from, datetime_to, adults,
                                                                        children, num_rooms_needed)
        for room_object in marriott_rooms_data:
            room = Room(
                room_object=room_object,
                hotel_name="Marriott",
                room_type=room_object.room_type,
                rooms_available=room_object.available,
                num_rooms_needed=num_rooms_needed,
                price_per_night=room_object.price_per_night,
                date_from=datetime_from,
                date_to=datetime_to,
                location=location,
                num_children=children,
                num_adults=adults,
            )
            available_rooms_objects.append(room)

        return available_rooms_objects

    def reserve(self):
        if self.selected_item is not None:
            if self.selected_item.hotel_name == "Hilton":
                hilton_hotel_api = HiltonHotelAPI()
                self.confirmation_id = hilton_hotel_api.reserve_room(self.selected_item.room_object, [])
                return True
            elif self.selected_item.hotel_name == "Marriott":
                marriott_hotel_api = MarriottHotelAPI()
                self.confirmation_id = marriott_hotel_api.do_room_reservation(self.selected_item.room_object, [])
                return True
            else:
                print("Unknown Hotel.")
                return False
        else:
            print("No Rooms available for the selected dates and locations.")
            return False

    def cancel(self):
        if self.confirmation_id is not None:
            if self.selected_item.hotel_name == "Hilton":
                hilton_hotel_api = HiltonHotelAPI()
                return hilton_hotel_api.cancel_room(self.confirmation_id)
            elif self.selected_item.hotel_name == "Marriott":
                marriott_hotel_api = MarriottHotelAPI()
                return marriott_hotel_api.cancel_room(self.confirmation_id)
            else:
                print("Unknown Hotel.")
                return False
        else:
            print("No reservation found to cancel.")
            return False



class Room:
    def __init__(self,room_object = None, hotel_name=None, room_type=None, rooms_available=0, num_rooms_needed=0,
                 price_per_night=0, date_from=None, date_to=None, location=None, num_children=0, num_adults=0):
        self.room_object = room_object
        self.hotel_name = hotel_name
        self.room_type = room_type
        self.rooms_available = rooms_available
        self.num_rooms_needed = num_rooms_needed
        self.price_per_night = price_per_night
        self.date_from = date_from
        self.date_to = date_to
        self.location = location
        self.num_children = num_children
        self.num_adults = num_adults

        if date_from and date_to and isinstance(date_from, datetime) and isinstance(date_to, datetime):
            self.num_nights = (date_to-date_from).days
        else:
            self.num_nights = 0

        self.cost = self.num_nights * self.price_per_night * self.num_rooms_needed

    def __str__(self):
        return (f"{self.hotel_name}: Per night: {self.price_per_night} - Total Cost: {self.cost} - From {self.num_rooms_needed} "
                f"on: {self.date_from} - #num_nights {self.num_nights} - "
                f"#num rooms: {self.rooms_available} - #Children: {self.num_children} - #Adults: {self.num_adults}")


###########################################################################################################


def select_item(available_items, item_type):
        while True:
            print(f"\nSelect a {item_type}:")
            for idx, item in enumerate(available_items, start=1):
                print(f"{idx}) {item}")
            try:
                choice = int(input(f"Enter your choice (from 1 to {len(available_items)}): "))
                if 1 <= choice <= len(available_items):
                    selected_item = available_items[choice - 1]
                    print(f"{item_type.capitalize()} ['{selected_item}'] added to your itinerary.")
                    return selected_item
                else:
                    print(f"Invalid choice, please enter a number between 1 and {len(available_items)}.")

            except ValueError:
                print(f"Invalid input, please enter a valid number (1 to {len(available_items)}).")


###########################################################################################################


def input_date(prompt):
    date_str = input(prompt)
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        print("Incorrect format, please use DD-MM-YYYY")
        return None


###########################################################################################################


def base_ui():
    customer = Customer('user1', '123456')

    while True:
        try:
            enter_choice = int(input("""System Access: 
                1) Login
                2) Sign Up
                Enter Choice (1 or 2): """))
        except ValueError:
            print("Invalid input, please enter a number (1 or 2).")
            continue

        if enter_choice == 1:
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            if customer.login(username, password):
                customer_page(customer)
                break
            else:
                print("Invalid Username or Password. Please try again.")
        elif enter_choice == 2:
            print("Sign up is not yet supported, please wait.")
        else:
            print("Invalid Input, please enter either 1 or 2.")


###########################################################################################################


def customer_page(customer):
    while True:
        try:
            choice = int(input(f"""Welcome {customer.username} | Customer:
                    1) View Profile 
                    2) Make itinerary
                    3) List my itineraries
                    4) Logout
                    Enter your choice (from 1 to 4): """))
        except ValueError:
            print("Invalid input, please enter a number (1, 2, 3 or 4).")
            continue

        if choice == 1:
            customer.view_profile()
        elif choice == 2:
            customer.add_itinerary()
        elif choice == 3:
            customer.list_itineraries()
        elif choice == 4:
            exit()
        else:
            print("Invalid input, please enter a number (1, 2, 3 or 4).")

if __name__ == "__main__":
    base_ui()