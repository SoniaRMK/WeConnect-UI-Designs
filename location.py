# app/models/location.py
"""Script for creating Location class objects"""

class Location(object):
    """Location class"""

    def __init__(self, locationName, locationID):
        self.locationName = locationName
        self.locationID = locationID
        self.businesses = {}
