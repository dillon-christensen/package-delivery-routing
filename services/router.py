"""
Route Service

Module that holds the Route class and is responsible for routing. Majority of business logic happens in this service. Each route 
takes a list of package ID's and generates a series of stops that contain all of the packages for each address. The stop order is
generated using the Nearest Neighbor algorithm.
"""
from datetime import datetime, timedelta
from domain.distance_table import DistanceTable
from domain.hash_table import HashTable
from domain.stop import Stop

class Route:
    
    def __init__(self, route_id:int, start_time:datetime, packages:list[int], package_table:HashTable,
                 distance_table:DistanceTable, truck_number:int):

        self.route_id:int = route_id
        self.stops:list[Stop] = []
        self.start_time:datetime = start_time
        self.end_time:datetime
        self.truck_number:int = truck_number
        self.total_distance:float = 0.0

        self.__packages:list[int] = packages
        self.__distance_table:DistanceTable = distance_table
        self.__package_table:HashTable = package_table

        self._generate_route()
        self._populate_stops_delivery_data()

    def update_route(self):
        """
        Function to update route after package address correction
        """
        self.stops = []
        self._generate_route()
        self._populate_stops_delivery_data()
    
    def _generate_route(self):

        # Nearest neighbor logic starts here
        # Start by generating raw unsorted dict of stops 
        unsorted_stops:dict[int,Stop] = self._package_id_list_to_stops()
        non_prio_stops:dict[int,Stop] = {}

        current_stop:Stop 

        # In case one of the deliveries is to the hub itself
        if 1 in unsorted_stops:
            current_stop = unsorted_stops[1]
            del unsorted_stops[1]
        else:
            current_stop = Stop(1,[])

        self.stops.append(current_stop)

        # The Nearest Neighbor algorithm has been modified into a 2 tier approach, first all of the priority packages (anything
        # before 10:30) will be routed, then any non-priority will be routed on the second loop
        while unsorted_stops:

            nearest:int = -1
            shortest_distance:float = float('inf')

            for stop_key in list(unsorted_stops):

                # Any non prio stops will be delivered after priority stops
                if unsorted_stops[stop_key].is_priority == False:
                    non_prio_stops[stop_key] = unsorted_stops[stop_key]
                    del unsorted_stops[stop_key]
                    continue

                stop_distance = self.__distance_table.get_distance(current_stop.address_id, stop_key)

                if stop_distance < shortest_distance:
                    nearest = stop_key
                    shortest_distance = stop_distance

            # Need this condition in the case of only non-prio stops
            if nearest != -1:
                current_stop = unsorted_stops[nearest]
                self.stops.append(current_stop)
                del unsorted_stops[nearest]

        # Second pass to route non-prio stops
        while non_prio_stops:

            nearest:int = -1
            shortest_distance:float = float('inf')

            for stop_key in non_prio_stops:

                stop_distance = self.__distance_table.get_distance(current_stop.address_id, stop_key)

                if stop_distance < shortest_distance:
                    nearest = stop_key
                    shortest_distance = stop_distance

            current_stop = non_prio_stops[nearest]
            self.stops.append(current_stop)
            del non_prio_stops[nearest]

        # Always ends at hub
        self.stops.append(Stop(1,[]))

    def _populate_stops_delivery_data(self):
        """
        Populates each stop w/ delivery timestamp and distance from last stop. This information will be utilized for the UI output
        later.
        """

        last_datetime:datetime = self.start_time
        last_stop_id:int = 1

        for stop in self.stops:

            distance:float = self.__distance_table.get_distance(last_stop_id, stop.address_id)
            deltahours:float = distance / 18
            current_datetime:datetime = last_datetime + timedelta(hours=deltahours)

            for id in stop.package_ids:

                package = self.__package_table.lookup(id)

                if package is not None:
                    package.delivery_time = current_datetime

            stop.delivery_time = current_datetime
            last_datetime = current_datetime
            last_stop_id = stop.address_id
            stop.distance_from_last = distance

        self.end_time = last_datetime

    def _package_id_list_to_stops(self) -> dict[int,Stop]:
        """
        Protected helper method to turn the list of package ID's provided at route creation to a raw, unsorted dict of stops
        """

        stop_dict:dict[int,Stop] = {}

        for id in self.__packages:

            package = self.__package_table.lookup(id)

            if package is not None:
                if package.address_id in stop_dict:
                    stop_dict[package.address_id].package_ids.append(id)
                else:
                    stop_dict[package.address_id] = Stop(package.address_id, [id])

                if package.deadline == "10:30 AM" or package.deadline == "9:00 AM":
                    stop_dict[package.address_id].is_priority = True

        return stop_dict
