# stuff to make the airflow, 1PW integration work
import os
import pendulum
from datetime import timedelta
from airflow.decorators import dag, task
from onepasswordconnectsdk.client import Client, new_client
import onepasswordconnectsdk

# libs for the dag portion, not the boilerplate
import json
import urllib.request

DEPLOYMENT_ENVIRONMENT = os.getenv("ENVIRONMENT") # our current environment from ['production', 'development']
ONEPASSWORD_CONNECT_TOKEN = os.getenv("OP_API_TOKEN") # where we get our secrets
ONEPASSWORD_CONNECT_HOST = os.getenv("OP_CONNECT") # our secret to get secrets 🤐
VAULT_ID = "quvhrzaatbj2wotsjrumx3f62a"  # FLH personal Discovery Day vault - not a secret, per se ..

# this section could be collapsed into a single execution branch if we 
# used a rigid naming scheme in 1PW. I don't think it's as readable
# though as what's below in saying what we're actually up to.
if DEPLOYMENT_ENVIRONMENT == "production":
    SECRET_NAME = "airflow.fyi production secret" # as found in 1pw
else:
    SECRET_NAME = "airflow.fyi development secret" # as found in 1pw

# here is where you define what secrets you want pulled for the DAG
# you can have as many as you need
REQUIRED_SECRETS = {
    "secret_value": { # you pick the key you want to store the value into,
        "opitem": SECRET_NAME, # and you give it the these three items to define the secret uniquely in 1PW
        "opfield": ".password",
        "opvault": VAULT_ID,
    },
}

# instantiate a 1PW client
client: Client = new_client(ONEPASSWORD_CONNECT_HOST, ONEPASSWORD_CONNECT_TOKEN)
# get the requested secrets from 1PW
SECRETS = onepasswordconnectsdk.load_dict(client, REQUIRED_SECRETS)

# define the parameters of the DAG
@dag(
    dag_id="weather-checker",
    description="A DAG which checks the weather and writes out an HTML file",
    schedule="0/5 * * * *",
    start_date=pendulum.datetime(2023, 4, 10, tz="UTC"),
    catchup=False,
    tags=["weather"],
)

# 🥘 Boilerplate ends here; the rest is the DAG itself

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
                    background-color: darkred;
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
                    <p class='smaller'>{DEPLOYMENT_ENVIRONMENT} secret: {SECRETS["secret_value"]}</p>
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


