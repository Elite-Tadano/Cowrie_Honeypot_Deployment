import json
import os
import plotly.express as px
import pandas as pd
import requests

OUTPUT_HTML = "output/visual_report.html"

def get_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response['status'] == 'success':
            return {
                'ip': ip,
                'country': response['country'],
                'lat': response['lat'],
                'lon': response['lon']
            }
    except:
        pass
    return {'ip': ip, 'country': 'Unknown', 'lat': 0, 'lon': 0}

def generate_visual_report(report_data, ip_list):
    geo_data = [get_geolocation(ip) for ip in ip_list]
    df = pd.DataFrame(geo_data)

    fig = px.scatter_geo(
        df, lat='lat', lon='lon', text='ip', color='country',
        title='Attacker IP Geolocation'
    )

    os.makedirs("output", exist_ok=True)
    fig.write_html(OUTPUT_HTML)
    with open("output/ip_geolocation.json", 'w') as geo_json:
        json.dump(geo_data, geo_json, indent=2)
