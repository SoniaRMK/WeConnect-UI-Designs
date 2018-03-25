# app/models/review.py
"""Script for creating Review class objects"""

class Review(object):
    """Review class"""

    def __init__(self, reviewID, reviewTitle, reviewMsg, reviewBusinessID, reviewCreatedBy, reviewCreatedDate):
        self.reviewID = reviewID
        self.reviewTitle = reviewTitle
        self.reviewBusinessID = reviewBusinessID
        self.reviewMsg = reviewMsg
        self.reviewCreatedBy = reviewCreatedBy
        self.reviewCreatedDate = reviewCreatedDate

