"""
Address entity definition
"""
class Address:
    def __init__(self, id:int, street:str, city:str, state:str, zip:str):
        self.id:int = id
        self.street:str = street
        self.city:str = city
        self.state:str = state
        self.zip:str = zip

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"Street: {self.street}, "
            f"City: {self.city}, "
            f"State: {self.state}, "
            f"Zip: {self.zip}, "
        )
