"""
UI Service

Module responsible for handling console display and user input. 
"""
from datetime import datetime

from domain.address import Address
from domain.distance_table import DistanceTable
from domain.hash_table import HashTable
from services.router import Route
from colorama import Back, Fore, Style

def start_ui(routes:list[Route], address_dict:dict[int,Address], package_table:HashTable, distance_table:DistanceTable):
    """
    Central function for console UI. Prints Program title, prompts for and processes user
    input to display package status for a given time, then outputs the status for each package
    at that time.
    """

    user_input:str = ""

    print(Back.MAGENTA + "\n\n  WGUPS Package Tracker\n")

    while user_input != "q":

        # User input prompt
        user_input = input("\n\n  Please enter a time to view package status in the "
                            + "form H:MM AM/PM or q to quit: ")

        # If user enters q exit the loop
        if user_input == "q":
            continue

        print("\n\n")

        time_format:str = "%I:%M %p"
        total_distance:float = 0.0

        status_time:datetime = datetime.combine(datetime.today(), datetime.strptime(user_input, time_format).time())
        no_route_packages:list[int] = []

        # Simulate Address correction on package #9 according to time 
        # given by user
        update_time:datetime = datetime.combine(datetime.today(), datetime.strptime("10:20 AM", time_format).time())
        package_9 = package_table.lookup(9)
        if package_9 is not None:
            if status_time > update_time:
                package_9.address_id = 6
            else:
                package_9.address_id = 9

        # Update route 4 (route that contains address 9)
        route_4:Route = routes[3]
        route_4.update_route()

        # Print any routes that have started
        for route in routes:
            if route.start_time < status_time:
                _print_route(route, address_dict, status_time)
            else:
                for stop in route.stops:
                    no_route_packages.extend(stop.package_ids)
            total_distance += route.total_distance

        # Print any packages still at the Hub or that have been delayed
        if not no_route_packages:
            print(Back.WHITE + Fore.BLACK + Style.BRIGHT + f"{'Summary':^140}\n" + Style.RESET_ALL + "\n")
        else:
            _print_hub_delayed_packages(no_route_packages, package_table, address_dict, status_time)


        # Print time that all trucks finished and total distance traveled
        if status_time >= route_4.end_time:
            end_str = route_4.end_time.strftime("%-I:%M%p").lower()[0:-1]
        else:
            end_str = "-"
        distance_str = f"{total_distance:.1f}"
        print(Fore.BLUE + f"{' ':<20}{'All Trucks Finished: ':<21}" + Style.RESET_ALL + f"{end_str:<6}{' ':<34}"
              + Fore.BLUE + f"{'Total Distance Traveled: ':<25}" + Style.RESET_ALL + f"{distance_str} mi")

def _print_route(route:Route, address_dict:dict[int,Address], status_time:datetime):
    """
    Protected Method for displaying route.
    """
    
    indent = "     "
    output_str = ""

    stops_no_hub = route.stops[1:-1]
    distance_current:float = 0.0
    
    for i, stop in enumerate(stops_no_hub):

        package_str = ", ".join(map(str, stop.package_ids))
        address_str = address_dict[stop.address_id].street
        
        # Trim address if too long
        if len(address_str) > 20:
            address_str = address_str[:20] + "..."

        time_str = ""
        status_str = ""

        # Populate output strings for stop data according to
        # whether stop has been completed and only add distance to
        # running total if stop is completed
        if status_time >= stop.delivery_time:
            time_str = f"{stop.delivery_time.strftime("%-I:%M%p").lower()[0:-1]:<6}"
            status_str = Fore.GREEN + f"{'Delivered':<13}" + Style.RESET_ALL
            distance_current += stop.distance_from_last
        else:
            time_str = Style.DIM + f"{'-':^6}" + Style.RESET_ALL
            status_str = Fore.BLUE + f"{'En Route':<13}" + Style.RESET_ALL

        # If even index, stop is output on left column; odd on right column
        if i % 2 == 0:
            output_str += (
                    Style.DIM + f"{indent}{i+1:<6}" 
                    + Style.RESET_ALL + f"{package_str:<14}{address_str:<24}{status_str}{time_str}  "
                    + Fore.CYAN + Style.BRIGHT + "||  " + Style.RESET_ALL
            )
        else:
            output_str += (
                    Style.DIM + f"{i+1:<6}" + Style.RESET_ALL
                    + Fore.WHITE + f"{package_str:<14}{address_str:<24}{status_str}{time_str}  \n"
            )

    # Route summary section
    start_str = route.start_time.strftime("%-I:%M%p").lower()[0:-1]
    end_str = ""
    if status_time < route.end_time:
        end_str = "-"
    else:
        end_str = route.end_time.strftime("%-I:%M%p").lower()[0:-1]

    route.total_distance = distance_current
    distance_str = f"{distance_current:.1f}"

    print(Back.CYAN + Fore.BLACK + Style.BRIGHT + f"{f'Route {route.route_id}  -  Truck {route.truck_number}':^140}")
    print(Back.CYAN + Fore.BLACK + f"{indent}Stop  {'Package ID':<14}{'Address':<24}{'Status':<13}"
          + f"{'Time':<7}{' ':<5}Stop  {'Package ID':<14}{'Address':<24}{'Status':<13}{'Time':<9}")
    print(output_str + "\n")
    print(Fore.BLUE + f"{' ':<10}{'Start Time: ':<12}" + Style.RESET_ALL + f"{start_str:<6}{' ':<34}"
          + Fore.BLUE + f"{'End Time: ':<10}" + Style.RESET_ALL + f"{end_str:<6}{' ':<34}"
          + Fore.BLUE + f"{'Distance: ':<10}" + Style.RESET_ALL + f"{distance_str} mi\n")


def _print_hub_delayed_packages(packages:list[int], package_table:HashTable, address_dict:dict[int,Address], status_time:datetime):
    """
    Protected Method for displaying any packages that are still at the hub or have been delayed.
    """

    output_str = ""
    delayed_packages = [6,25,28,32]
    packages.sort()
    
    for i, id in enumerate(packages):

        package = package_table.lookup(id)

        # Go to next package if no package comes back from ID
        if package is None:
            continue

        time_format:str = "%I:%M %p"
        address_str = address_dict[package.address_id].street

        if len(address_str) > 20:
            address_str = address_str[:20] + "..."

        status_str = ""
        delay_arrival_time = datetime.combine(datetime.today(), datetime.strptime("9:05 AM", time_format).time())
        
        # Check if package is delayed or in the hub
        if status_time < delay_arrival_time and id in delayed_packages:
            status_str = Fore.RED + f"{'Delayed':<10}" + Style.RESET_ALL
        else:
            status_str = Fore.MAGENTA + f"{'At Hub':<10}" + Style.RESET_ALL

        # Print in 3 columns
        if i % 3 != 2:
            output_str += (f"  {id:<3} {address_str:<24}{status_str}"
                           + Fore.CYAN + Style.BRIGHT + f"{'||':<10}" + Style.RESET_ALL)
        else:
            output_str += f"  {id:<3} {address_str:<24}{status_str}\n"


    print(Back.WHITE + Fore.BLACK + Style.BRIGHT + f"{'Packages  -  At Hub | Delayed':^140}")
    print(Back.WHITE + Fore.BLACK + f"  {'ID'}  {'Address':<24}{'Status':<10}{' ':<10}"
          + f"  {'ID'}  {'Address':<24}{'Status':<10}{' ':<10}"
          + f"  {'ID'}  {'Address':<24}{'Status':<10}")
    print(output_str + "\n")
