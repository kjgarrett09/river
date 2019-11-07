import matplotlib.pyplot as plt
import requests
import csv
import json
from io import StringIO
import numpy as np
from datetime import datetime


def rain(location):
    print "Getting latest weather reports from {}".format(location)
    res = requests.get("https://prodapi.metweb.ie/observations/{location}/today".format(location=location))
    data = json.loads(res.content)
    rain_measurements = []
    for point in data:
        rain_measurements.append(float(point['rainfall'].strip(" ")))
    return rain_measurements


def river(location):
    print "Getting latest river levels  from {}".format(location)

    today = datetime.now().strftime("%Y-%m-%d")
    locations = {"Ballycarroon": 34007,
                 "Richmond": 34118,
                 "Keenagh": 34114}
    river_measurements = []
    river_res = requests.get("http://waterlevel.ie/data/day/"
                             "{location}_0001.csv".format(location=locations[location]))
    river_data = csv.DictReader(StringIO(unicode(river_res.content, "utf-8")), delimiter=",")
    for row in river_data:
        if today in row['datetime'] and ":00" in row['datetime']:
            river_measurements.append(float(row['value'].strip(" ")))
    return river_measurements


belmullet_rain = rain("belmullet")
newport_rain = rain("newport-furnace")
knock_rain = rain("knock")

ballycarroon_river = river("Ballycarroon")
richmond_river = river("Richmond")
keenagh_river = river("Keenagh")

max_x = max([
    len(belmullet_rain),
    len(newport_rain),
    len(ballycarroon_river),
    len(richmond_river)
])
if max_x > len(belmullet_rain):
    belmullet_rain.append()
if max_x > len(newport_rain):
    newport_rain.append()



hours = [x for x in range(0, max_x)]

x = np.arange(max_x)
# fig = plt.figure()
# ax = plt.subplot(111)
fig, ax1 = plt.subplots()


# plt.axis([0, max_x, 0, 2.5])
# plt.plot(hours, belmullet_rain, label="Belmullet", "ro")
# plt.plot(hours, newport_rain, label="Newport", "bo")
# plt.plot(hours, knock_rain, label="Knock", "go")
# plt.plot(hours, ballycarroon_river, label="BallyCarroon", "g^")
# plt.plot(hours, richmond_river, "y^")
# plt.plot(hours, keenagh_river, "b^")
color = 'tab:red'
ax1.set_xlabel('time')
ax1.set_ylabel('Rain (mm)', color=color)

ax1.plot(hours, belmullet_rain, "ro", label="Belmullet")
ax1.legend(loc="upper right")
ax1.plot(hours, newport_rain, "bo", label="Newport-Furnace")
ax1.plot(hours, knock_rain, "go", label="Knock")

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('River (m)', color=color)

ax2.plot(hours, ballycarroon_river, label="BallyCarroon")
ax2.plot(hours, richmond_river, label="Richmond", )
ax2.plot(hours, keenagh_river, label="Kennagh")

fig.tight_layout()
plt.show()
