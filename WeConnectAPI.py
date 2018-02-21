from flask import Flask, jsonify, request

app = Flask(__name__)


businesses = [
    {'businessID' : 1, 'businessName' : 'MTN', 'Location' : 'Kampala', 'Category' : 'Telecommunications', 'businessProfile': 'Best telecommunication company in Uganda'}, 
    {'businessID' : 2, 'businessName' : 'Tecno', 'Location' : 'Kisoro', 'Category' : 'Telecommunications', 'businessProfile': 'Best telecommunication company in Uganda'},
    {'businessID' : 3, 'businessName' : 'KFC', 'Location' : 'Kabarole', 'Category' : 'Restaurant', 'businessProfile': 'Best telecommunication company in Uganda'},
    {'businessID' : 4, 'businessName' : 'Sheraton', 'Location' : 'Kampala', 'Category' : 'Hotel', 'businessProfile': 'Best telecommunication company in Uganda'},
    {'businessID' : 5, 'businessName' : 'Arab COntractors', 'Location' : 'Kampala', 'Category' : 'Construction', 'businessProfile': 'Best telecommunication company in Uganda'},
]

users = [
    {'userID' : 1, 'userEmail' : 'aws@xxx.com', 'userPassword' : 'qwer123' },
    {'userID' : 2, 'userEmail' : 'hjk@yyy.com', 'userPassword' : 'jh123' }
]

reviews = [
    {'reviewMsg' : 'Perfect phones for a low price', 'businessID' : 2},
    {'reviewMsg' : 'Bad customer Service', 'businessID' : 1},
    {'reviewMsg' : 'Worth the Price', 'businessID' : 2},
    {'reviewMsg' : 'Loved it', 'businessID' : 3},
    {'reviewMsg' : 'Not worth it', 'businessID' : 2}
]

# endpoint to create new user
@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    user = {
        'userID' : users[-1]['userID'] + 1,
        'userEmail' : request.json['userEmail'],
        'userPassword' : request.json['userPassword']
        }
    users.append(user)
    return jsonify({'Users': users})
# endpoint to login user
@app.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    return {'hello': 'world'}

# endpoint to logout user
@app.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    return {'hello': 'world'}

# endpoint to reset user's Password
@app.route('/api/v1/auth/reset-password', methods=['POST'])
def password_reset():
    return {'hello': 'world'}

# endpoint to create new business
@app.route('/api/v1/businesses', methods=['POST'])
def business_register():
    biz = {
        'businessID' : businesses[-1]['businessID'] + 1,
        'businessName' : request.json['businessName'],
        'Location' : request.json['Location'], 
        'Category' : request.json['Category'], 
        'businessProfile': request.json['businessProfile']
        }
    businesses.append(biz)
    return jsonify({'businesses': businesses})

# endpoint to edit a business
@app.route('/api/v1/businesses/<int:bizId>', methods=['PUT'])
def business_update(bizId):
    biz = [biz for biz in businesses if biz['businessID'] == bizId]
    biz[0]['businessName'] = request.json.get('businessName', biz[0]['businessName'])
    biz[0]['businessProfile'] = request.json.get('businessProfile', biz[0]['businessProfile'])
    biz[0]['Category'] = request.json.get('Category', biz[0]['Category'])
    biz[0]['Location'] = request.json.get('Location', biz[0]['Location'])
    return jsonify({'business': biz[0]})

# endpoint to view all businesses
@app.route('/api/v1/businesses', methods=['GET'])
def business_list_view():
    return jsonify({'businesses': businesses})

# endpoint to delete a business
@app.route('/api/v1/businesses/<int:bizId>', methods=['DELETE'])
def business_delete(bizId):
    biz = [business for business in businesses if business['businessID']==bizId]
    businesses.remove(biz[0])
    return jsonify({'businesses': businesses})  

# endpoint to view a business
@app.route('/api/v1/businesses/<int:bizid>', methods=['GET'])
def business_view(bizid):
    biz = [business for business in businesses if business['businessID'] == bizid]
    return jsonify({'business': biz[0]})

# endpoint to add a review to a business
@app.route('/api/v1/businesses/<int:bizId>/reviews', methods=['POST'])
def add_review(bizId):
    review = {
        'reviewMsg': request.json['reviewMsg'], 
        'businessID': bizId
        }
    reviews.append(review)
    return jsonify({'Reviews': reviews})

# endpoint to get all reviews of a business
@app.route('/api/v1/businesses/<int:bizId>/reviews', methods=['GET'])
def get_reviews(bizId):
    reviewsbiz = [rev for rev in reviews if rev['businessID'] == bizId]
    return jsonify({'Reviews': reviewsbiz}) 

if __name__ == '__main__':
    app.run(debug=True)