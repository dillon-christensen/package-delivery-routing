"""
HashTable Implementation

Custom hash table. Built on a list of lists, implementation uses a hash function to append to or look up an indexed list. It uses
chaining in buckets to avoid collisions.
"""
from colorama import Fore

from domain.package import Package

class HashTable:

    def __init__(self, size:int=20):
        self.table = []

        for _ in range(size):
            self.table.append([])

    def _hash_function(self, key:int):
        # Simple hash function, simply returns the key modulo the 
        # size of the table
        return key % len(self.table)

    def insert(self, key:int, package:Package):
        bucketId = self._hash_function(key)
        bucket = self.table[bucketId]

        for pair in bucket:

            # If package already exists skip insertion, id's should be unique
            if pair[0] == key:
                print(Fore.RED +
                      'Error: HashTable key already exists; Skipping...')
                return

        bucket.append([key, package])

    def lookup(self, key:int) -> Package | None:
        bucketId = self._hash_function(key)
        bucket = self.table[bucketId]

        for pair in bucket:
            if pair[0] == key:
                return pair[1]

        return None
