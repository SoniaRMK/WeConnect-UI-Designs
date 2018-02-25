from resources.lib import *

businesses = [
    {'businessID' : 1, 'businessName' : 'MTN', 'Location' : 'Kampala', 'Category' : 'Telecommunications', 'businessProfile': 'Best telecommunication company in Uganda'}, 
    {'businessID' : 2, 'businessName' : 'Tecno', 'Location' : 'Kisoro', 'Category' : 'Telecommunications', 'businessProfile': 'Best telecommunication company in Uganda'},
    {'businessID' : 3, 'businessName' : 'KFC', 'Location' : 'Kabarole', 'Category' : 'Restaurant', 'businessProfile': 'Best telecommunication company in Uganda'},
    {'businessID' : 4, 'businessName' : 'Sheraton', 'Location' : 'Kampala', 'Category' : 'Hotel', 'businessProfile': 'Best telecommunication company in Uganda'},
    {'businessID' : 5, 'businessName' : 'Arab COntractors', 'Location' : 'Kampala', 'Category' : 'Construction', 'businessProfile': 'Best telecommunication company in Uganda'},
]

class Business(Resource):
    #creates a new business
    def post(self):
        biz = {
        'businessID' : businesses[-1]['businessID'] + 1,
        'businessName' : request.json['businessName'],
        'Location' : request.json['Location'], 
        'Category' : request.json['Category'], 
        'businessProfile': request.json['businessProfile']
        }
        businesses.append(biz)
        return jsonify({'businesses': businesses})
    #gets a  business
    def get(self, bizid):
        biz = [business for business in businesses if business['businessID'] == bizid]
        return jsonify({'business': biz[0]})
    #deletees a business
    def delete(self, bizid):
        biz = [business for business in businesses if business['businessID']==bizid]
        businesses.remove(biz[0])
    #edits a  business
    def put(self, bizid):
        biz = [biz for biz in businesses if biz['businessID'] == bizid]
        biz[0]['businessName'] = request.json.get('businessName', biz[0]['businessName'])
        biz[0]['businessProfile'] = request.json.get('businessProfile', biz[0]['businessProfile'])
        biz[0]['Category'] = request.json.get('Category', biz[0]['Category'])
        biz[0]['Location'] = request.json.get('Location', biz[0]['Location'])
        return jsonify({'business': biz[0]})

class BusinessList(Resource):
    def get(self):
        return jsonify({'businesses': businesses})