
class AirCanadaCustomerInfo:
    def __init__(self, name, passport, birthdate):
        pass

class AirCanadaFlight:
    def __init__(self, price, date_time_from, date_time_to,from_place,to_place):
        self.price = price  # price for total of adults & children
        self.date_time_from = date_time_from
        self.date_time_to = date_time_to
        self.from_place = from_place
        self.to_place = to_place
        
    def __str__(self):
        return f"Air Canada Flight {self.price}: Departure on {self.date_time_from}, Arrival on {self.date_time_to}"
    
    def getFromDate(self):
        return self.date_time_from   
     
    def getToDate(self):
        return self.date_time_to
    
class AirCanadaOnlineAPI:
    @staticmethod
    def get_flights(from_place, to_place):
        flights = []
        flights.append(AirCanadaFlight(200, "25-01-22", "10-02-22",from_place, to_place))
        flights.append(AirCanadaFlight(250, "29-01-22", "10-02-22",from_place, to_place))
        return flights

    @staticmethod
    def reserve_flight(flight: AirCanadaFlight, customers_info: list):
        confirmation_id = '1234AirCanadaXXr34'  # None for failure
        return confirmation_id
        #return None     # Try None

    @staticmethod
    def cancel_flight(confirmation_id):
        return True
