import pandas as pd
# import psycopg2

HIGH_THRESH = 10000
LOW_THRESH = -500

soy_thresholds = {
    'severe': {'mintemp': 2,
    'precipitation': {1: 100, 3: 110, 5: 150},
    'no_rain': 10,
    'maxtemp': 38,
    'windspeed': 50},

    'moderate': {'mintemp': 5,
    'precipitation': {1: 80, 3: 100, 5: 120},
    'no_rain': 7,
    'maxtemp': 35,
    'windspeed': 40},

    'weak': {'mintemp': 10,
    'precipitation': {1: 50, 3: 80, 5: 100},
    'no_rain': 4,
    'maxtemp': 32,
    'windspeed': 30}
}
maize_thresholds = {
    'severe': {'mintemp': 2,
    'precipitation': {1: 100, 3: 110, 5: 150}, # transform this into another dict: 1: 100mm, 3: 110mm, 5: 120mm
    'no_rain': 7,
    'maxtemp': 38,
    'windspeed': 50},


    'moderate': {'mintemp': 5,
    'precipitation': {1: 80, 3: 100, 5: 120},
    'no_rain': 5,
    'maxtemp': 35,
    'windspeed': 40},

    'weak': {'mintemp': 10,
    'precipitation': {1: 50, 3: 80, 5: 100},
    'no_rain': HIGH_THRESH,
    'maxtemp': 32,
    'windspeed': 30}
}
bean_thresholds = {
    'severe': {'mintemp': 2,
    'precipitation': {1: 100, 3: 110, 5: 150}, # transform this into another dict: 1: 100mm, 3: 110mm, 5: 120mm
    'no_rain': 10,
    'maxtemp': 38,
    'windspeed': 50},

    'moderate': {'mintemp': 5,
    'precipitation': {1: 80, 3: 100, 5: 120},
    'no_rain': 7,
    'maxtemp': 35,
    'windspeed': 40},

    'weak': {'mintemp': 10,
    'precipitation': {1: 50, 3: 80, 5: 100},
    'no_rain': 4,
    'maxtemp': 32,
    'windspeed': 30}
}
rice_thresholds = {
    'severe': {'mintemp': 2,
    'precipitation': {1: 100, 3: 110, 5: 150}, # transform this into another dict: 1: 100mm, 3: 110mm, 5: 120mm
    'no_rain': 10,
    'maxtemp': 38,
    'windspeed': 50},

    'moderate': {'mintemp': 5,
    'precipitation': {1: 80, 3: 100, 5: 120},
    'no_rain': 7,
    'maxtemp': 35,
    'windspeed': 40},

    'weak': {'mintemp': 10,
    'precipitation': {1: 50, 3: 80, 5: 100},
    'no_rain': 4,
    'maxtemp': 32,
    'windspeed': 30}
}
wheat_thresholds = {
    'severe': {'mintemp': 2,
    'precipitation': {1: 100, 3: 110, 5: 150}, # transform this into another dict: 1: 100mm, 3: 110mm, 5: 120mm
    'no_rain': 10,
    'maxtemp': 38,
    'windspeed': 50},

    'moderate': {'mintemp': 5,
    'precipitation': {1: 80, 3: 100, 5: 120},
    'no_rain': 7,
    'maxtemp': 35,
    'windspeed': 40},

    'weak': {'mintemp': 10,
    'precipitation': {1: 50, 3: 80, 5: 100},
    'no_rain': 4,
    'maxtemp': 32,
    'windspeed': 30}
}

thresholds = {
    'soy': soy_thresholds,
    'maize': maize_thresholds,
    'bean': bean_thresholds,
    'rice': rice_thresholds,
    'wheat': wheat_thresholds
}


def analyze_data(data, culture, thresholds):
    alerts = {
        'severe': [],
        'moderate': [],
        'weak': []
    }
    if data.empty:
        print(f"I think this should be unreachable")
        return None  

    # =======================================
    # Test precipitation
    # =======================================
    colors_prcp = ["#0073c3"] * len(data)  # if no alerts, graph is blue
    last = 0
    severity_colors = {'severe': "#aa0000", 'moderate': "#ffa600", 'weak': "#ffd000"}

    for severity in ['severe', 'moderate', 'weak']:
        for day in thresholds[culture][severity]['precipitation'].keys():
            rolling_sum = data['prcp'].rolling(day).sum()
            exceeded = rolling_sum > thresholds[culture][severity]['precipitation'][day]
            num = len(rolling_sum[exceeded].dropna())
            
            if num-last > 0:
                alerts[severity].append(f"🌧️ {num-last} period" + 's'*(num-last>1) + 
                                    f" that rained more than {thresholds[culture][severity]['precipitation'][day]} mm in {day} day" + 
                                    's'*(day>1) + ".")
                
                # change color based on severity
                for i in range(len(data)-day+1):
                    if exceeded.iloc[i+day-1]:
                        for j in range(day):
                            idx = i+j
                            if colors_prcp[idx] == '#0073c3': # color only if it has no color
                                # the order bein severe -> mod -> weak enforces that the most severe color
                                # applicable is the one that will be used
                                colors_prcp[idx] = severity_colors[severity]
                        
        last += num

    # print(colors_prcp)

    # Test days without rain:
    last = 0
    dry_spells = data['prcp'].eq(0).astype(int).groupby(data['prcp'].ne(0).cumsum()).sum()
    for severity in ['severe', 'moderate', 'weak']:
        num = len(dry_spells[dry_spells >= thresholds[culture][severity]['no_rain']])
        if num-last>0:               #•
            alerts[severity].append(f"🏜️ {num-last} period{'s' * (num-last>1)} of {thresholds[culture][severity]['no_rain']} or more consecutive days without rain.")
        last+=num


    # ===========================================================
    # Test maximum temperature
    # ===========================================================
    last = 0
    for severity in ['severe', 'moderate', 'weak']:
        num = len(data[data['tmax']>thresholds[culture][severity]['maxtemp']])
        if num-last>0:               #• 
            alerts[severity].append(f"🥵 {num-last} day" + 's'*(num-last>1) +  f" had maximum temperatures higher than {thresholds[culture][severity]['maxtemp']} °C.")
        last+= num

    # ===========================================================
    # Test minimum temperature
    # ===========================================================
    last = 0
    for severity in ['severe', 'moderate', 'weak']:
        num = len(data[data['tmin']<thresholds[culture][severity]['mintemp']])
        if num-last>0:               #•
            alerts[severity].append(f"🥶 {num-last} day" + 's'*(num-last>1) +  f" had minimum temperatures lower than {thresholds[culture][severity]['mintemp']} °C.")
        last+= num

    # ===========================================================
    # Test windspeed
    # ===========================================================
    last = 0
    for severity in ['severe', 'moderate', 'weak']:
        num = len(data[data['wspd_max']>thresholds[culture][severity]['windspeed']])
        if num-last>0:               #•
            alerts[severity].append(f"🍃 {num-last} day" + 's'*(num-last>1) +  f" had maximum windspeeds higher than {thresholds[culture][severity]['windspeed']} km/h.")
        last+= num

    red, orange, yellow = "\n".join(alerts['severe']), "\n".join(alerts['moderate']), "\n".join(alerts['weak'])

    return red, orange, yellow, colors_prcp



def read_db(engine, latitude, longitude, start_date, end_date, culture):
    engine = engine
    data = pd.read_sql_query(f"""SELECT point_id, date, tmax, tmin, tavg, prcp, rh_max, rh_min, rh_avg, wspd_max, wspd_min, wspd_avg FROM get_weather_data_nearby(
    {float(latitude)}, {float(longitude)}, '{start_date}', '{end_date}', 7.8) ORDER BY distance;
    """, engine)
    data = data[data['point_id']==data['point_id'].values[0]]
    red_alert, orange_alert, yellow_alert, colors_prcp = analyze_data(data, culture, thresholds)
    if data.empty:
        return (data, red_alert, orange_alert, yellow_alert, colors_prcp)
    return (data, red_alert, orange_alert, yellow_alert, colors_prcp)





