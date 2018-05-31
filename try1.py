'''Flask API to do the CRUD operations'''

#importing flask pymongo jsonify and request 
from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify
from flask import request

#creating flask object
app=Flask(__name__)

#connecting to database mlab and configuring
app.config['MONGO_DBNAME']='athira'
app.config['MONGO_URI']='mongodb://athirag:athira123@ds139890.mlab.com:39890/athira'

#connecting the app to mongodb database using pymongo
mongo = PyMongo(app)

#enabling debugging
app.debug=True

'''CREATE in CRUD operation
accepts a name and distance as input and stores it in the database'''
#routing to /create
@app.route('/create', methods=['POST'])
def add_star():
  star = mongo.db.star
  #accept the data from json format
  name = request.json['name']
  distance = request.json['distance']
  #to check whether the data is present
  s = star.find_one({'name' : name})
  if s:
    output = "name already exist"
    
  else:
    star_id = star.insert({'name': name, 'distance': distance})
    new_star = star.find_one({'_id': star_id })
    output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  #convert the data in json format
  return jsonify(output)
 

'''READ in CRUD operation
 displayes the data in the database'''
@app.route('/read', methods=['GET'])
def get_all_stars():
  star = mongo.db.star
  output = []
  for s in star.find():
    output.append({'name' : s['name'], 'distance' : s['distance']})
  return jsonify(output)

'''update in CRUD operation
accepts a name and distance as input and update distance in the database'''
@app.route('/update', methods=['POST'])
def get_one_star():
  star = mongo.db.star
  name=request.json['name']
  distance=request.json['distance']
  s = star.find_one({'name' : name})
  if s:
    output = {'name' : s['name'], 'distance' : distance}
    star.update({"name" : s['name']},{'$set':{"distance" : distance}})
  else:
    output = "No such name"
  return jsonify(output)

'''DELETE in CRUD operation
accepts a name and delete it from the database'''
@app.route('/delete',methods=['DELETE'])
def delete_one_star():
  star=mongo.db.star
  name=request.json['name']
  star.remove({'name':name})
  return jsonify({'ok':True,'message':'deleted successfully'})



if __name__ == '__main__':
    app.run(debug=True)
