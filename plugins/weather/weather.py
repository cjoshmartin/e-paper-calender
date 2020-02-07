
def kelvin_2_fah(value):
    output = (float(value) - 273.15) * (9/5) + 32
    return str(int(output)) + 'F'

def query_weather():
    weather_response = { }
    forecast_response = {}
    print('-= Ping Weather API =-')
    while True:
        try:
            weather_response = requests.get("http://api.openweathermap.org/data/2.5/weather", params={"appid":WEATHER_API, "zip":'46208,us'}).json()
            forecast_response = requests.get("http://api.openweathermap.org/data/2.5/forecast", params={"appid":WEATHER_API, "zip":'46208,us'}).json()
            break
        except:
            print('-= Weather API JSON Failed - Will Try Again =-')
            time.sleep(refresh_time)

    current_weather = weather_response['weather'][0]['main']
    current_icon = weather_response['weather'][0]['icon']

    current_temp = kelvin_2_fah(weather_response['main']['temp'])
    forecast_weather = forecast_response['list'][0]['weather'][0]['main']
    forecast_icon = forecast_response['list'][0]['weather'][0]['icon']
    forecast_temp_min_max = kelvin_2_fah(forecast_response['list'][0]['main']['temp_min']) + ' , ' + kelvin_2_fah(forecast_response['list'][0]['main']['temp_max'])

    if (len(current_weather) >= 9):
        current_weather = current_weather[0:7] + '.'
    if (len(forecast_weather) >= 9):
        forecast_weather = forecast_weather[0:7] + '.'
    
    # The placement for weather icon
    w_weather_icon,h_weather_icon = font_weather_icons.getsize(icons_list[str(current_icon)])
    y_weather_icon = 320 + ((384 - 320) / 2) - (h_weather_icon / 2)

    # The placement for current weather string & temperature
    w_current_weather,h_current_weather = font_weather.getsize(current_weather)
    w_current_temp,h_current_temp = font_weather.getsize(current_temp)

    # The placement for forecast temperature string & temperatures
    w_forecast_temp_min_max,h_forecast_temp_min_max = font_weather.getsize(forecast_temp_min_max)
    w_forecast_weather,h_forecast_weather = font_weather.getsize(forecast_weather)

    draw_black.text((250,y_weather_icon),icons_list[str(current_icon)], font = font_weather_icons, fill = 0) # Diplay weather icon

    draw_black.text((250 + w_weather_icon + 10,327), current_weather, font = font_weather, fill = 0) # Display the current weather text
    draw_black.line((250 + w_weather_icon + 10,352,250 + w_weather_icon + 10 + w_current_weather,352), fill = 0) # Line below the current weather text
    x_current_temp = (w_current_weather - w_current_temp) / 2 + 250 + 10 + w_weather_icon # Location for the current temperature to be displayed
    draw_black.text((x_current_temp, 356), current_temp, font = font_weather, fill = 0) # The text of the current temperature

    x_arrow_symbol = 250 + w_weather_icon + 20 + w_current_weather # Location of the arrow to be displayed
    draw_black.rectangle((x_arrow_symbol, 350, x_arrow_symbol + 10,354), fill = 0) # Rectangle of the arrow
    draw_black.polygon([x_arrow_symbol + 10, 346, x_arrow_symbol + 16,352, x_arrow_symbol + 10,358], fill = 0) # Triangle of the arrow

    x_forecast_start = x_arrow_symbol + 16 + 10 # All forcasts to be displayed start at this position
    draw_black.text((x_forecast_start, 356), forecast_temp_min_max, font = font_weather, fill = 0) # The text of the forecast temperature
    draw_black.line((x_forecast_start, 352, x_forecast_start + w_forecast_temp_min_max, 352), fill = 0) # Line above the forecast weather temperature text
    x_forecast_weather = x_forecast_start + (w_forecast_temp_min_max - w_forecast_weather) / 2
    draw_black.text((x_forecast_weather, 327), forecast_weather, font = font_weather, fill = 0) # Display the forecast weather text

    draw_black.text((x_forecast_start + w_forecast_temp_min_max + 10,y_weather_icon),icons_list[str(forecast_icon)], font = font_weather_icons, fill = 0) # Diplay forecast weather icon
