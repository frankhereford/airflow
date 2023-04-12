import json
import pendulum
import urllib.request
from datetime import timedelta
from airflow.decorators import dag, task

@dag(
    dag_id="weather-checker",
    description="A DAG which checks the weather and writes out an HTML file",
    schedule="0/5 * * * *",
    start_date=pendulum.datetime(2023, 4, 10, tz="UTC"),
    catchup=False,
    tags=["weather"],
)

def etl_weather():

    # An extract task to get the time in Austin
    @task()
    def get_time_in_austin_tx():
        current_time = pendulum.now("America/Chicago") 
        return current_time.strftime("%m/%d/%Y, %H:%M:%S")

    # A extract task which pulls the weather from the NOAA API
    @task()
    def get_weather():
        # open a URL and parse the JSON it returns
        with urllib.request.urlopen("https://api.weather.gov/gridpoints/EWX/156,91/forecast") as url:
            data = json.loads(url.read().decode())
            return data

    # A transform task which formats the weather forecast
    @task()
    def get_forecast(weather: dict):
        details = weather["properties"]["periods"][0]["detailedForecast"]
        period = weather["properties"]["periods"][0]["name"]
        return(f"{period}: {details}")

    # A load task which writes the forecast to an HTML file
    @task()
    def write_out_html_file(forecast: str, time: str):
        f = open("/opt/airflow/weather/index.html", "w")
        f.write(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ATX Weather Report</title>
                <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: lightblue;
                }}
                .weather {{
                    font-weight: bold;
                    font-size: 24px;
                }}
                .date {{
                    font-size: 16px;
                    margin-top: 24px; /* equal to the height of the first p element */
                    text-align: right;
                    
                }}
                </style>
            </head>
            <body>
                <div>
                    <p class="weather">{forecast}</p>
                    <p class="smaller">{time}</p>
                </div>
            </body>
            </html>
        """)
        f.close()


    time = get_time_in_austin_tx()
    weather = get_weather()
    forecast = get_forecast(weather)
    write_out_html_file(forecast, time)

etl_weather()


