
class TurkishCustomerInfo:
    def __init__(self, passport, name, birthdate):
        pass


class TurkishFlight:
    def __init__(self, cost, datetime_from, datetime_to, from_place, to_place):
        self.cost = cost
        self.datetime_from = datetime_from
        self.datetime_to = datetime_to
        self.from_place = from_place
        self.to_place = to_place
        
    def getFromDate(self):
        return self.datetime_from   
     
    def getToDate(self):
        return self.datetime_to
    
    def __str__(self):
        return f"Turkish Flight {self.cost}: Departure on {self.datetime_from}, Arrival on {self.datetime_to}"

class TurkishOnlineAPI:
    def set_from_to_info(self, datetime_from, from_loc, datetime_to, to_loc):
        pass

    def set_passengers_info(self, infants, childern, adults):
        pass

    def get_available_flights(from_place, to_place):
        flights = []
        flights.append(TurkishFlight(400, "10-01-22", "10-03-22",from_place,to_place))
        flights.append(TurkishFlight(431, "18-01-22", "27-03-22",from_place,to_place))
        flights.append(TurkishFlight(100, "15-01-22", "27-09-22",from_place,to_place))
        return flights

    @staticmethod
    def reserve_flight(customers_info: list, flight: TurkishFlight):
        confirmation_id = '1234TTTTT'  # None for failure
        return confirmation_id
        # return None     # Try None

    @staticmethod
    def cancel_flight(confirmation_id):
        return True
