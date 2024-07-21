import pyowm
from config import *

#функция что бы узнать температуру
def temperature_w(city):
	owm = pyowm.OWM(API_KEY)
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place(city)
	w = observation.weather
	temp = w.temperature('celsius')['temp']
	wind = w.wind()

	#a = "В городе " + city + " сейчас " + str(round({temp})) + "°"
	#b = "Средняя скорость верта", wind['speed'],"м/с"

	#print("В городе" + city + "сейчас" + weather.detailed_status) 
	#print("Температура воздуха",temp['temp'],"градусов")
	#print("Воздух прогреется максимум до",temp['temp_max'], "градусов")
	#print("Минимальная температура воздуха составит", temp['temp_min'], "градусов")
	#print("Ощущается как", temp['feels_like'])  
	#print("Средняя скорость верта", wind['speed'],"м/с")

	return "В городе " + city + " сейчас " + str(round(temp)) + "°"
