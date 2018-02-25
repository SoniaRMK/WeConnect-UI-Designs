from resources.lib import *


reviews = [
    {'reviewMsg' : 'Perfect phones for a low price', 'businessID' : 2},
    {'reviewMsg' : 'Bad customer Service', 'businessID' : 1},
    {'reviewMsg' : 'Worth the Price', 'businessID' : 2},
    {'reviewMsg' : 'Loved it', 'businessID' : 3},
    {'reviewMsg' : 'Not worth it', 'businessID' : 2}
]

class Review(Resource):
    def post(self, bizid):
        review = {
            'reviewMsg': request.json['reviewMsg'], 
            'businessID': bizid
            }
        reviews.append(review)
        return jsonify({'Reviews': reviews})

    def get(self, bizid):
        reviewsbiz = [rev for rev in reviews if rev['businessID'] == bizid]
        return jsonify({'Reviews': reviewsbiz})       