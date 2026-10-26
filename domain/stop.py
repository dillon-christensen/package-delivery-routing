"""
Stop entity definition
"""
from datetime import datetime


class Stop:
    def __init__(self,address_id:int, package_ids:list[int]):
        self.address_id:int = address_id
        self.package_ids:list[int] = package_ids
        self.is_priority:bool = False
        self.delivery_time:datetime = datetime.combine(datetime.today(), datetime.strptime("12:00 AM",  "%I:%M %p").time())
        self.distance_from_last:float = 0.0

    def __str__(self):
        return (
            f"ID: {self.package_ids}, "
            f"AddressId: {self.address_id}"
            f"IsPriority: {self.is_priority}"
        )
