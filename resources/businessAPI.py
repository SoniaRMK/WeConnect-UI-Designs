from resources.lib import *

businesses = []

class Business(Resource):
    #gets a  business
    @token_required
    def get(self, bizid):
        biz = [business for business in businesses if business['businessID'] == bizid]
        if biz == []:
            message = {
            'status': "Not Found",
            'message': 'Business Not registered yet!!',
            }
            resp = jsonify(message)
            resp.status_code = 404
        else:
            message = {
            'status': "Success",
            'business': biz[0],
            }
            resp = jsonify(message)
            resp.status_code = 200

        return resp

    #deletes a business
    @token_required
    def delete(self, bizid):
        biz = [business for business in businesses if business['businessID']==bizid]
        if biz == []:
            message = {
            'status': "Not Found",
            'message': 'Business Not registered yet!!',
            }
            resp = jsonify(message)
            resp.status_code = 404
        else:
            businesses.remove(biz[0])
            message = {
                'status': "success",
                'message': 'Successfully Deleted!!',
            }
            resp = jsonify(message)
            resp.status_code = 200

        return resp
        
    #edits a  business
    @token_required
    def put(self, bizid):
        biz = [business for business in businesses if business['businessID'] == bizid]
        biz[0]['businessName'] = request.json.get('businessName', biz[0]['businessName'])
        biz[0]['businessProfile'] = request.json.get('businessProfile', biz[0]['businessProfile'])
        biz[0]['Category'] = request.json.get('Category', biz[0]['Category'])
        biz[0]['Location'] = request.json.get('Location', biz[0]['Location']) 
        business = [busi for busi in businesses if request.json['businessName'] == busi['businessName'] and request.json['Category'] == busi['Category']]
        if len(business) > 1:
            message = {
                    'status': "Failed",
                    'message': 'Business Already Exists!',
                    }
            resp = jsonify(message)
            resp.status_code = 400
        else:
            message = {
            'status': "Success",
            'message': 'Business successfully Edited!',
            }
            resp = jsonify(message)
            resp.status_code = 400

        return resp
       # message = "Business successfully Edited!"
        
        #return jsonify({'Message': message}), 200

class BusinessList(Resource):
    #creates a new business
    @token_required
    def post(self):
        biz = {
        'businessID' : len(businesses)+ 1,
        'businessName' : request.json['businessName'],
        'Location' : request.json['Location'], 
        'Category' : request.json['Category'], 
        'businessProfile': request.json['businessProfile'], 
        'createdBy': request.data['user']
        }
        business = [busi for busi in businesses if request.json['businessName'] == busi['businessName'] and request.json['Category'] == busi['Category']]
        if len(business) == 0:
            businesses.append(biz)
            message = {
            'status': "success",
            'message': 'Business Successfully Created!!',
            }
            resp = jsonify(message)
            resp.status_code = 200
      
        else:
            message = {
            'status': "Failed",
            'message': 'Business Already Created!',
            }
            resp = jsonify(message)
            resp.status_code = 400

        return resp
    
    #Get all businesses
    @token_required
    def get(self):
        return jsonify({'businesses': businesses})