from flask import Flask, render_template, request, redirect
import requests
import json

app = Flask(__name__)

class WeatherData:
    def __init__(self):
        self.temperature = None
        self.pressure = None 
        self.humidity = None
        self.sea_level = None
        self.description = None

class Weather:
    def __init__(self):
        self.name = None
        self.api_key = "insert_your_openweather_api_key" 
        self.weekday_data = None 
        self.todays_data = None 

    def get_coordinates(self, city_name: str):
        api = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}".format(city_name, self.api_key)
        data = requests.get(api)
        converted_data = json.loads(data.content)
        return (converted_data[0]["lat"], converted_data[0]["lon"])


    def get_weather_data(self, city_name: str):
        coordinates = self.get_coordinates(city_name)
        api = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric".format(coordinates[0], coordinates[1], self.api_key)
        data = requests.get(api)
        data = data.json()
        return data

    def get_todays_data(self, data):
        day_data = data['list'][0]
        weather_data = WeatherData() 
        weather_data.temperature = day_data['main']['temp']
        weather_data.pressure = day_data['main']['pressure']
        weather_data.sea_level = day_data['main']['sea_level']
        weather_data.humidity = day_data['main']['humidity']

        return weather_data

    def get_day_data(self, day_number, data):
        day_data = data['list'][day_number-1]
        weather_data = WeatherData() 

        weather_data.temperature = day_data['main']['temp']
        weather_data.description = day_data['weather'][0]['main']

        return weather_data
        

    def get_weekday_data(self, data):
        weather_data = [WeatherData()] * 5
        weather_data[0] = self.get_day_data(1, data)
        weather_data[1] = self.get_day_data(2, data)
        weather_data[2] = self.get_day_data(3, data)
        weather_data[3] = self.get_day_data(4, data)
        weather_data[4] = self.get_day_data(5, data)

        return weather_data

    def get_weather_info(self, city_name):
        data = self.get_weather_data(city_name)
        self.name = city_name

        self.todays_data = self.get_todays_data(data)
        self.weekday_data = self.get_weekday_data(data)


@app.route("/", methods=["POST", "GET"])
def index():
    data = Weather()
    if request.method == "POST":
        content = request.form["searched_city"]
        data.get_weather_info(content)
        return render_template("index.html", weather=data)

    data.get_weather_info("London")
    return render_template("index.html", weather=data)

app.run(port=80, debug=True)

