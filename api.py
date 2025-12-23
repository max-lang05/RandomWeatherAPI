import datetime, random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

#Database of all http requests
class WeatherModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    time = db.Column(db.String)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    temprature = db.Column(db.Integer, nullable=False)
    windSpeed = db.Column(db.Integer, nullable=False)
    windDirection = db.Column(db.Integer, nullable=False)

#gets arguments passed in from request
user_args = reqparse.RequestParser()
user_args.add_argument('longitude', type=float, required=True, help="Longitude cannot be blank")
user_args.add_argument('latitude', type=float, required=True, help="Latitude cannot be blank")

#format for responses
# Full weather fields
userFields = {
    'id': fields.Integer,
    'date': fields.String,
    'time': fields.String,
    'longitude': fields.Float,
    'latitude': fields.Float,
    'temprature': fields.Integer,
    'windSpeed': fields.Integer,
    'windDirection': fields.Integer
}

# Temperature-only fields
temperatureFields = {
    'id': fields.Integer,
    'date': fields.String,
    'time': fields.String,
    'temprature': fields.Integer
}

# Wind-only fields
windFields = {
    'id': fields.Integer,
    'date': fields.String,
    'time': fields.String,
    'windSpeed': fields.Integer,
    'windDirection': fields.Integer
}

class Weather(Resource):
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        now = datetime.datetime.now()
        localWeather = WeatherModel(
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            longitude=args['longitude'],
            latitude=args['latitude'],
            temprature=random.randint(-5, 40),
            windSpeed=random.randint(1, 64),
            windDirection=random.randint(0, 360)
        )
        db.session.add(localWeather)
        db.session.commit()
        return localWeather, 200

class Temperature(Resource):
    @marshal_with(temperatureFields)
    def post(self):
        args = user_args.parse_args()
        now = datetime.datetime.now()
        tempRecord = WeatherModel(
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            longitude=args['longitude'],
            latitude=args['latitude'],
            temprature=random.randint(-5, 40),
            windSpeed=0,  # placeholder
            windDirection=0  # placeholder
        )
        db.session.add(tempRecord)
        db.session.commit()
        return tempRecord, 200

class Wind(Resource):
    @marshal_with(windFields)
    def post(self):
        args = user_args.parse_args()
        now = datetime.datetime.now()
        windRecord = WeatherModel(
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            longitude=args['longitude'],
            latitude=args['latitude'],
            temprature=0,  # placeholder
            windSpeed=random.randint(1, 64),
            windDirection=random.randint(0, 360)
        )
        db.session.add(windRecord)
        db.session.commit()
        return windRecord, 200

# endpoints
api.add_resource(Weather, '/api/weather')          # full weather
api.add_resource(Temperature, '/api/weather/temp') # temperature only
api.add_resource(Wind, '/api/weather/wind')        # wind only

@app.route('/')
def home():
    
    return '<h1>Weather API</h1>'

if __name__ == '__main__':
    app.run(debug=True)