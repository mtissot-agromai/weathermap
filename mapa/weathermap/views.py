from django.http import HttpResponse, JsonResponse # type: ignore

from django.shortcuts import render # type: ignore

from .models import Lookup

from .utils import read_db
from sqlalchemy import create_engine # type: ignore
from random import randint

from datetime import datetime, timedelta, date

def index(request):
    return render(request, "weathermap/index.html")

def history(request):
    actual_history = list(Lookup.objects.order_by("-lookup_time"))
    output = "<br>".join([str(item) for item in actual_history])
    # output = "Abc"
    return HttpResponse(output)

engine = create_engine('postgresql+psycopg2:///USER/:/PASSWORD/@localhost:5434//DB NAME/')

def get_weather_data(request):
    # print("Cheguei na get weather data")
    if request.method == "POST":
        # print('entrei no if')
        try:
            lat = float(request.POST.get("latitude"))
            lon = float(request.POST.get("longitude"))
        except ValueError:
            lat = 0
            lon = 0
        start = request.POST.get("start_date")
        end = request.POST.get("end_date")
        culture = request.POST.get("culture")
        # print(f"Safra: {safra}")

        Lookup.objects.create(latitude=lat, longitude=lon,
                               start_date=start, end_date=end)

        
        data, red, orange, yellow, colors_prcp = read_db(engine, lat, lon, start, end, culture)

        # avg_temperature
        # max_temperature
        # min_temperature
        # avg_humidity
        # max_humidity
        # min_humidity
        # avg_windspeed
        # max_windspeed
        # min_windspeed
        if not data.empty:
            dates = sorted(data['date'].tolist())
            avg_temperature = data['tavg'].tolist()
            max_temperature = data['tmax'].tolist()
            min_temperature = data['tmin'].tolist()
            avg_humidity = data['rh_avg'].tolist()
            max_humidity = data['rh_max'].tolist()
            min_humidity = data['rh_min'].tolist()
            avg_windspeed = data['wspd_avg'].tolist()
            max_windspeed = data['wspd_max'].tolist()
            min_windspeed = data['wspd_min'].tolist()
            prcp = data['prcp'].tolist()
            total_prcp = int(data['prcp'].sum())
            prcp_cumulative = data['prcp'].cumsum().tolist()
            alert_red = red
            alert_orange = orange
            alert_yellow = yellow
            colors_prcp = colors_prcp
        else:
            dates = []
            avg_temperature = []
            max_temperature = []
            min_temperature = []
            avg_humidity = []
            max_humidity = []
            min_humidity = []
            avg_windspeed = []
            max_windspeed = []
            min_windspeed = []
            prcp = []
            total_prcp = 0
            alert_red = red
            alert_orange = orange
            alert_yellow = yellow
            colors_prcp = []


        # n_days = (date.fromisoformat(end)-date.fromisoformat(start)).days
        # dates = [date.fromisoformat(end) - timedelta(days=i) for i in range(n_days + 1)]
        # temp = [randint(10, 20) for _ in range(n_days)]
        # prcp = [randint(0, 50) for _ in range(n_days)]
        # humidity = [randint(60, 100) for _ in range(n_days)]
        

        return JsonResponse({
            'dates': dates,
            'avg_temp': avg_temperature,
            'max_temp': max_temperature,
            'min_temp': min_temperature,
            'avg_rhum': avg_humidity,
            'max_rhum': max_humidity,
            'min_rhum': min_humidity,
            'avg_wspd': avg_windspeed,
            'max_wspd': max_windspeed,
            'min_wspd': min_windspeed,
            'prcp': prcp,
            'prcp_total': total_prcp,
            'prcp_cumulative': prcp_cumulative,
            'alert_red': alert_red,
            'alert_orange': alert_orange,
            'alert_yellow': alert_yellow,
            'colors_prcp': colors_prcp
        })