import requests
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Some constants
URL = "http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast?lat={lat};long={long}"

DEEL_BRIDGE = {"lat": "54.0808005", "long": "-9.5116742"}

PROXIES = {
    # "http": "http://hdqproxy01",
    # "https": "https://hdqproxy01",
}

# End Constants


def loc_forecast(location):
    print "Getting forecast for location : {} :  {}".format(location["lat"], location["long"])

    address = URL.format(lat=location["lat"], long=location["long"])
    res = requests.get(address, proxies=PROXIES)
    return res.content


def draw_graph(extracts):

    times = [block['from'] for block in extracts]
    values = [block['amount'] for block in extracts]
    sums = [block['sum'] for block in extracts]
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('time')
    ax1.set_ylabel('rain (mm/h)', color=color)
    ax1.plot(times, values, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('total (mm)', color=color)  # we already handled the x-label with ax1
    ax2.plot(times, sums, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


if __name__ == "__main__":
    rain = []
    running_sum = 0
    limit_hours = 24

    print "Get the forecast for Deel Bridge"
    weather = loc_forecast(DEEL_BRIDGE)

    root = ET.fromstring(weather)


    for time_block in root.findall('./product/time'):
        if len(rain) <= limit_hours:
            precip = time_block.findall('./location/precipitation')
            if precip:
                # This block of the forecast has rain information
                from_dt = datetime.strptime(time_block.attrib['from'], '%Y-%m-%dT%H:%M:%SZ')
                to_dt = datetime.strptime(time_block.attrib['to'], '%Y-%m-%dT%H:%M:%SZ')
                elapsed = to_dt - from_dt
                if elapsed.seconds == 3600:
                    # this block of the forcast has information by the hour

                    # Keep a running sum for the length of the forecast
                    running_sum += float(precip[0].attrib['value'])
                    p = {"from": from_dt,
                         "to": to_dt,
                         "amount": precip[0].attrib['value'],
                         "sum": running_sum
                         }
                    rain.append(p)
        else:
            break


    draw_graph(rain)
