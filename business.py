# app/models/business.py
"""Script for creating Business class objects"""

class Business(object):
    """Business class"""

    def __init__(self, businessID, businessName, businessProfile, businessCategory, businessLocation, businessLogo, businessCreatedBy, businessCreatedDate):
        self.businessID = businessID
        self.businessName = businessName
        self.businessProfile = businessProfile
        self.businessCategory = businessCategory
        self.businessLocation = businessLocation
        self.businessLogo = businessLogo
        self.businessCreatedBy =  businessCreatedBy
        self.businessCreatedDate = businessCreatedDate
        self.reviews = {}
