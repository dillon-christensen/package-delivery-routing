"""
WGUPS Routing Program - Task 2

Author: Dillon Christensen
Student ID: 001005594
Intructor: Bob Branch
Date: Aug, 17 2026
"""
from datetime import datetime

from colorama import init

from domain.address import Address
from domain.distance_table import DistanceTable
from domain.hash_table import HashTable
from services.csv_loader import load_addresses, load_distance_table, load_packages
from services.router import Route
from services.ui import start_ui


def main():
    """
    Main method for executing program. Loads packages, addresses and distance table
    from CSV files, generates routes from given package ID lists, then starts the UI
    with the generated routes.
    """
    init(autoreset=True)

    package_table = HashTable()
    load_packages(package_table)

    address_dict:dict[int, Address] = {}
    load_addresses(address_dict)

    distance_table = DistanceTable()
    load_distance_table(distance_table)

    # Routes start at 8am
    start_time_1:datetime = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    route_1:Route = Route(1, start_time_1, [1,4,40,7,29,5,37], package_table, distance_table, 1)
    route_2:Route = Route(2, start_time_1, [15,13,39,16,34,14,20,21,30,8,3,18,36,38,19,23], package_table, distance_table, 2)
    route_3:Route = Route(3, route_1.end_time, [6,25,26,31,32,17,22,24,28,27,35,11], package_table, distance_table, route_1.truck_number)
    route_4:Route = Route(4, route_2.end_time, [2,9,10,33,12], package_table, distance_table, route_2.truck_number)

    start_ui([route_1,route_2,route_3,route_4], address_dict, package_table, distance_table)

if __name__ == "__main__":
    main()
