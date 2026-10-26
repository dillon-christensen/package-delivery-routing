"""
Package entity definition
"""
from datetime import datetime
from enum import Enum

class Package:
    def __init__(self, id:int, address_id:int, deadline:str, weight:int):
        self.id:int = id
        self.address_id:int = address_id
        self.deadline:str = deadline
        self.weight:int = weight

        self.status:PackageStatus = PackageStatus.AT_HUB
        self.delivery_time:datetime|None = None

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"AddressId: {self.address_id}, "
            f"Deadline: {self.deadline}, "
            f"Weight: {self.weight}, "
            f"Status: {self.status}, "
            f"Delivered: {self.delivery_time}, "
        )

class PackageStatus(Enum):
    AT_HUB = "At Hub"
    IN_ROUTE = "In Route"
    DELIVERED = "Delivered"

    def __str__(self):
        return str(self.value)
