from flask import Flask,jsonify,request,make_response
from flask_restful import Api,Resource
import pandas as pd
from pymongo import MongoClient     #To handle mongo db

#Read a tsv file
udf = pd.read_csv("Food Survey_75Responses.tsv",sep = '\t', lineterminator = '\r')

#Manupilating The dataset
drop_col = ["Timestamp","Food sanctum that doesn't vibes with you"]
udf.drop(drop_col,axis=1,inplace=True)
cols = ["Name","Year","Hosteller","North-South","Vegetarin","Dine-in","Breakfast","Lunch","Dinner","Cusinies","Chinese","Italain",
       "North","South","Continental","Tea/Coffee","Maggie","Juices","Rolls","Samosa/Puff","Panipuri","Shawarma","Sugar rush",
       "Spicy-Sweet","Spicy","Sweet","All-time"]
udf.columns = cols

#Create a Flask app(api)
app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users' : 0
})

class Visit(Resource):
    def get(self):
        num = UserNum.find({})[0]['num_of_users']
        num += 1
        UserNum.update({}, {"$set":{"num_of_users":num}})
        return str("Hello user " + str(num))


@app.route('/')
def hello_world():
    return("Hello World!")

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


class All_time(Resource):
    def get(self):
        all_time_restro = dict(udf['All-time'].value_counts().sort_values(ascending = False).head(5))
        a = all_time_restro.keys()
        k = 1
        for i in a:
            all_time_restro[i] = k
            k += 1
        all_time_restro = dict([(value, key) for key, value in all_time_restro.items()])
        result = {
            "All-time" : all_time_restro
        }
        return make_response(jsonify(result),200)

class Chinese(Resource):
    def get(self):
        chinese_restro = dict(udf['Chinese'].value_counts().sort_values(ascending = False).head(5))
        a = chinese_restro.keys()
        k= 1
        for i in a:
            chinese_restro[i] = k
            k += 1
        chinese_restro = dict([(value, key) for key, value in chinese_restro.items()])
        result = {
            "Chinese" :chinese_restro
        }
        return make_response(jsonify(result),200)

class Italain(Resource):
    def get(self):
        italain_restro = dict(udf['Italain'].value_counts().sort_values(ascending = False).head(5))
        a = italain_restro.keys()
        k= 1
        for i in a:
            italain_restro[i] = k
            k += 1
        italain_restro = dict([(value, key) for key, value in italain_restro.items()])
        result = {
            "Italain" :italain_restro
        }
        return make_response(jsonify(result),200)


class North(Resource):
    def get(self):
        north_restro = dict(udf['North'].value_counts().sort_values(ascending = False).head(5))
        a = north_restro.keys()
        k= 1
        for i in a:
            north_restro[i] = k
            k += 1
        north_restro = dict([(value, key) for key, value in north_restro.items()])
        result = {
            "North" :north_restro
        }
        return make_response(jsonify(result),200)

class South(Resource):
    def get(self):
        south_restro = dict(udf['South'].value_counts().sort_values(ascending = False).head(5))
        a = south_restro.keys()
        k= 1
        for i in a:
            south_restro[i] = k
            k += 1
        south_restro = dict([(value, key) for key, value in south_restro.items()])
        result = {
            "South" :south_restro
        }
        return make_response(jsonify(result),200)

class Continental(Resource):
    def get(self):
        continental_restro = dict(udf['Continental'].value_counts().sort_values(ascending = False).head(5))
        a = continental_restro.keys()
        k= 1
        for i in a:
            continental_restro[i] = k
            k += 1
        continental_restro = dict([(value, key) for key, value in continental_restro.items()])
        result = {
            "Continental" :continental_restro
        }
        return make_response(jsonify(result),200)



api.add_resource(All_time,"/all-time")
api.add_resource(Chinese,"/chinese")
api.add_resource(Italain,"/italain")
api.add_resource(North,"/north")
api.add_resource(South,"/south")
api.add_resource(Continental,"/continental")
api.add_resource(Visit,"/hello")

#for example
#Run localhost:5000/all-time to get a json result
#added local host to 0.0.0.0
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
