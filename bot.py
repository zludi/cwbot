import telebot
import json
import urllib.request as ul

TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(TOKEN)
country = None
@bot.message_handler(commands=['start'])
def start(start):
    sent = bot.send_message(start.chat.id, 'Your country or state')
    bot.register_next_step_handler(sent, town)

def town(countryRequest):
    global country
    sent = bot.send_message(countryRequest.chat.id, 'Your city')
    country = countryRequest
    bot.register_next_step_handler(sent, weather)

def weather(townRequest):
    url = 'http://api.wunderground.com/api/YOUR_API_ID/geolookup/conditions/q/'+ country.text + '/' + str(townRequest.text) + '.json'
    try:
        f = ul.urlopen(url)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        location = parsed_json['location']['city']
        temp_c = parsed_json['current_observation']['temp_c']
        date = parsed_json['current_observation']['observation_time']
        wind =  parsed_json['current_observation']['wind_dir']
        windSpeed  =  parsed_json['current_observation']['wind_kph']
        pressure = float( parsed_json['current_observation']['pressure_mb']) / 1000 * 750 
        UV =  parsed_json['current_observation']['UV']
        cloudness =  parsed_json['current_observation']['weather']
        humidity = parsed_json['current_observation']['relative_humidity']
    except Exception:
        sent = bot.send_message(townRequest.chat.id, 'Wrong country/state or town. Try again. Send "OK".')
        bot.register_next_step_handler(sent, start)
    else:   
        bot.send_message(townRequest.chat.id, '\n'.join(f'Temperature in {location}: {temp_c} °C; Cloudness: {cloudness}; Humidity: {humidity}; Wind {wind}, {windSpeed} kph; Pressure: {pressure} mm Hg; UV: {UV}; {date}'.split('; ')))
    f.close()	
bot.polling() 