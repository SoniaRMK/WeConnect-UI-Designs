# app/models/user.py
"""Script for creating User class objects"""

class User():
    """User class"""

    def __init__(self, userID, userFName, userLName, userEmail, userPassword, userImage):
        self.userID = userID
        self.userFName = userFName
        self.userLName = userLName
        self.userEmail = userEmail
        self.password_hash = userPassword
        self.userImage = userImage
        self.businesses = {}
        self.reviews = {}
