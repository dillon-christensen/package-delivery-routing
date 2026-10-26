"""
DistanceTable

Matrix that holds distance information that allows distance lookups by inputing address id's as multi-dimensional index value
"""
class DistanceTable:
    def __init__(self):
        self.distances:list[list[float]] = []

    def get_distance(self, from_address_id, to_address_id) -> float:

        distance = self.distances[from_address_id][to_address_id]

        return distance

    def __str__(self) -> str:
        rows = []

        for sublist in self.distances:
            row = ", ".join(f"{value:4}" for value in sublist)
            rows.append(f"[{row}]")

        return "[\n  " + ",\n  ".join(rows) + "\n]"
