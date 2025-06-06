'''
Zach Aubry
zaubry@uwo.ca
251307316
Computer Science 1026A
File Created June 1st, 2025

This code performs a parse through a given csv file of flights with various information of each flight. The parse stores the flight number in a parent dictionary as the key, with the corresponding value
being a nested child dictionary of the flight info. This dictionary can be used to get supplimental information about each flight, such as the average ticket cost by airline, total passenegers by airline,
the flights that occur overnight, the aircrafts with the most recorded flights, total flight duration between specified airports, as well as retrieving the cheapest flight by airline.
'''


import pprint

import csv

# This is the parsing function that goes through a given file of flights, which stores flight number as a key and additional flight info as a nested dictionary in one parent dictionary
def parse_flight_data(data_file_name): # Need to sort the keys in parent IN ORDER ( use dict.sort()? ) - Think this is done?

    try:
        with open(data_file_name, "r") as csvfile:
            parent = {} # parent dictionary to organize data ; Key is flight number, and value is a child dictionary containing flight info
            main_list = [] # Storing all csv data here as nested lists, will retrieve for later

            for row in csvfile:
                
                lines = row.strip().split(",") # To remove whitespace and split the data into lists

                main_list.append(lines) 

                if lines[0].lower() == "flightnumber" or lines[0] == "": # Ignores the heading row and any empty rows
                    continue 
                else:
                    p_key = lines[0].lower() # Keys for the parent dictionary, flight characters are lowercased
                    
                    if p_key not in parent:
                        parent[p_key] = {} # The value is a child dictionary of flight info

                        # Variables for important line elements
                        aircraft = lines[8].lower()
                        airline = lines[5].lower()
                        arrivalAirport = lines[2].lower()
                        arrivalTime = lines[4]
                        avgTicketPrice = lines[7]
                        depAirport = lines[1].lower()
                        depTime = lines[3]
                        duration = lines[6]
                        passengerCount = lines[9]

                        # For converting flight duration to total minutes
                        duration_hours = int(duration[0])
                        duration_minutes = int(duration[2:4])

                        hours_2_mins = duration_hours * 60
                        total_mins = hours_2_mins + duration_minutes

                        # Now adding flight info to the child dictionary
                        parent[p_key]['Aircraft'] = str(aircraft)
                        parent[p_key]['Airline'] = str(airline)
                        parent[p_key]['ArrivalAirport'] = str(arrivalAirport)
                        parent[p_key]['ArrivalTime'] = str(arrivalTime)
                        parent[p_key]['AvgTicketPrice'] = int(avgTicketPrice)
                        parent[p_key]['DepartureAirport'] = str(depAirport)
                        parent[p_key]['DepartureTime'] = str(depTime)
                        parent[p_key]['FlightDuration'] = int(total_mins) 
                        parent[p_key]['PassengerCount'] = int(passengerCount)
        
        return parent 
        
    # Exception for if the file cannot be found 
    except FileNotFoundError: 
        return -1 


# Thie function calculates the average ticket prices for all flights by the same airline
def calculate_average_ticket_price(all_flights, airlines): 
    average_prices = []

    for line in airlines:
        try:
            line_sum = 0.0 # Prices go here for each airline
            line_count = 0 # Num of airlines for each flight
            
            # Child Dictionary
            for flight in all_flights:
                
                flight_info = all_flights[flight] 
                
                airline = flight_info['Airline']
                avg_cost = flight_info['AvgTicketPrice']
                
                # Checks if airline from the dictionary is the specified airline 
                if line.lower() != airline.lower(): 
                    continue
                else:
                    line_sum += avg_cost
                    line_count += 1
            
            if line_count == 0: # If airline has no flights
                average_prices.append(0)
            
            else:
                average_prices.append(round(line_sum / line_count, 2))

            # Reseting the sum / count for the next flight
            line_sum = 0.0
            line_count = 0
        
        # Exception for if there are any errors for the corresponding flight; passes on to the next flight and the loop continues
        except:
            average_prices.append(-1) 

    return average_prices
    

# This function gets the total pasengers that are flown by specified airlines
def get_total_passengers_by_airline(all_flights, airlines): 
    total_passengers_by_airline = {}

    for line in airlines:
        passCounter = 0
        for flight in all_flights:
            
            # Child Dictionary
            flight_info = all_flights[flight] 

            airline = flight_info['Airline']
            passengers = flight_info['PassengerCount']
                    
            # Checks if airline from the dictionary is the specified airline 
            if line.lower() != airline.lower(): 
                continue
            else:
                passCounter += passengers

        if passCounter == 0: # If no passengers are being flown by the specified airline
            continue
        else:
            total_passengers_by_airline[line.lower()] = passCounter # Assigns the airline as the key, and the total passengers by airline as the value

        passCounter = 0 # To reset for the following specified airline

    
    return total_passengers_by_airline


# This function checks the dictionary of dictionaries for flights that take place over night (i.e, departs one day and arrives on a following day)
def get_overnight_flights(all_flights): 
    overnight_flights = []

    for flight in all_flights:

        # Child Dictionary
        flight_info = all_flights[flight] 

        depTime = flight_info['DepartureTime'] 
        arrivTime = flight_info['ArrivalTime']

        # Days to check for each flight
        depDay = depTime[8:10]
        arrivDay = arrivTime[8:10]

        # Adds the flight number if the dates are different, indicating an overnight flight
        if depDay != arrivDay: 
            overnight_flights.append(flight)

    return overnight_flights


# This function goes through each aircraft and ranks them based on number of flights made by each one
# What is returned is a specified list of the top 'n' aircrafts, where n is a specified integer with default parameter of n=3
def get_top_n_aircraft(all_flights, n=3): 
    top_n_aircraft = [] 
    aircraft_count = {} # to keep track of flights made by aircraft 

    try:
        for flight in all_flights:

            # Child Dictionary
            flight_info = all_flights[flight] 

            aircraft = flight_info['Aircraft']

            if aircraft not in aircraft_count.keys(): # Counter becomes 1
                
                aircraft_count[aircraft] = 1
            
            elif aircraft in aircraft_count.keys(): 

                aircraft_count[aircraft] += 1


        # Next need to sort the dictionary so the most flights are the first element

        sorted_aircrafts = sorted(aircraft_count.items(), key=lambda x:x[1], reverse=True) # sorts the dictionary values in descending order as tuples of aircraft and number of flights

        # If n is inputted as a string, an exception is raised
        if type(n) == str:
            raise ValueError("Invalid n value!")

        # Want n as an integer for a proper ranking
        else:
            n = int(n)
        
        # If n is an invalid value, an exception is raised
        if n > len(sorted_aircrafts) or n < 0:
            raise ValueError("Invalid n value!")
        
        for i in range(n):
            top_n_aircraft.append(sorted_aircrafts[i][0]) # List gets the aircraft with the most flights
        
        return top_n_aircraft

    # Exception for if the inputed value of n exceeds the available number of unique aircraft or if n is negative
    except ValueError as excpt: 
        return excpt
    
# This function gets the total duration of any airline that flies between the specified departure and arrival airports
def get_total_duration(all_flights, airports): 
    airline_durations = {}  # Dictionary to store total durations for each airline

    # Converting the airport codes to uppercase, so they can be checked as matching codes for given flight
    for i in range(len(airports)):
            airports[i] = airports[i].upper()

    for flight in all_flights:

        # Child Dictionary
        flight_info = all_flights[flight]

        airline = flight_info['Airline'].lower()
        duration = flight_info['FlightDuration'] 

        # The airports between flights to check
        dep_port = flight_info['DepartureAirport'].upper()
        arriv_port = flight_info['ArrivalAirport'].upper()


        # Conditions that determine which flight duration is counted: including flights with specified airlines and airports only
        if dep_port in airports and arriv_port in airports and airline not in airline_durations.keys():
            
            airline_durations[airline] = duration

        elif dep_port in airports and arriv_port in airports and airline in airline_durations.keys():
            
            airline_durations[airline] += duration
        
        # For airlines that do not fly between the specified airports for any flight in the parent dictionary
        elif airline not in airline_durations.keys() and (dep_port not in airports or arriv_port not in airports):

            airline_durations[airline] = 0


    return airline_durations


# This function finds the cheapest ticket price per airline in the parent dictionary
def get_cheapest_flight_by_airline(all_flights) : 
    cheapest_flights = {} # Will return this as the cheapest flight by airline
    cheapest_tickets = {} # To keep track of ticket costs by airline

    for flight in all_flights:

        # Child Dictionary
        flight_info = all_flights[flight]

        airline = flight_info['Airline']
        avg_ticket_cost = flight_info['AvgTicketPrice']

        # Checks if the airline has been added to the dictionary as a key     
        if airline not in cheapest_flights.keys():
            cheapest_flights[airline] = flight
            cheapest_tickets[airline] = avg_ticket_cost

        else:
            if avg_ticket_cost < cheapest_tickets[airline]: # To check if the next airline's flight has a lower average ticket price than the airline's preceeding flight
                cheapest_flights[airline] = flight
                cheapest_tickets[airline] = avg_ticket_cost


    return cheapest_flights 
