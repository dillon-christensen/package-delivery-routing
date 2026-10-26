"""
CSV Loader Service

Module for loading data from CSV files in "data" directory into python entity objects, defined in "domain"
"""
import csv
from domain.distance_table import DistanceTable
from domain.package import Package
from domain.hash_table import HashTable
from domain.address import Address

def load_packages(hash_table:HashTable):
    """
    Loads package data in Package objects stored in the custom HashTable passed in as a param
    """
    with open("data/packages.csv") as file:
        
        reader = csv.reader(file)

        #Skip header row
        next(reader)

        for row in reader:

            package = Package(
                    int(row[0]), int(row[1]), row[2], int(row[3]) 
            )

            hash_table.insert(package.id, package)

def load_addresses(address_dict:dict[int,Address]):
    """
    Loads address data in Address objects stored in passed in dict
    """
    with open("data/addresses.csv") as file:

        reader = csv.reader(file)

        #Skip header row
        next(reader)

        for row in reader:

            address = Address(
                    int(row[0]),row[1],row[2],row[3],row[4]
            )

            address_dict[address.id] = address

def load_distance_table(table:DistanceTable):
    """
    Load distance data into DistanceTable object passed in, as multi-dimensional list object that distance data can be looked up 
    by simply inputing the address id's into the index reference values, like so:
        distance_table_obj.distance_list[address_id_x][address_id_y]
    """
    with open("data/address_distance_mapping.csv") as file:

        reader = csv.reader(file)
        rows = list(reader)

    #Pull address ID's from the first row
    column_ids = [int(value) for value in rows[0][1:]]

    num_locations = max(column_ids)

    # Create a square matrix filled w/ -1
    table.distances = [
        [-1.0 for _ in range(num_locations + 1)]
        for _ in range(num_locations + 1)
    ]

    for row in rows[1:]:

        address_id_x = int(row[0])

        for column_index, value in enumerate(row[1:]):

            # Skip entries that are blank
            if value == "":
                continue

            address_id_y = column_ids[column_index]
            distance = float(value)

            #store distance going both ways
            table.distances[address_id_x][address_id_y] = distance
            table.distances[address_id_y][address_id_x] = distance
