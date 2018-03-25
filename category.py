# app/models/category.py
"""Script for creating Category class objects"""

class Category(object):
    """Category class"""

    def __init__(self, categoryName, categoryID):
        self.categoryName = categoryName
        self.categoryID = categoryID
        self.businesses = {}
