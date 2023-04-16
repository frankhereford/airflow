# stuff to make the airflow, 1Password integration work
import os
import pendulum
import docker
import onepasswordconnectsdk
from airflow.decorators import dag, task
from onepasswordconnectsdk.client import Client, new_client

# libs for the dag portion, not the boilerplate
import json
import urllib.request

DEPLOYMENT_ENVIRONMENT = os.getenv("ENVIRONMENT")     # our current environment from ['production', 'development']
ONEPASSWORD_CONNECT_TOKEN = os.getenv("OP_API_TOKEN") # our secret to get secrets 🤐
ONEPASSWORD_CONNECT_HOST = os.getenv("OP_CONNECT")    # where we get our secrets
VAULT_ID = "quvhrzaatbj2wotsjrumx3f62a"               # FLH personal Discovery Day vault - not a secret, per se ..

# These secret names are entry titles in our 1Password secret vault.
if DEPLOYMENT_ENVIRONMENT == "production":
    SECRET_NAME = "airflow.fyi production secret"
else:
    SECRET_NAME = "airflow.fyi development secret"

# here is where you define what secrets you want pulled for the DAG
# you can have as many as you need
REQUIRED_SECRETS = {
    "secret_value": {          # you pick the key you want to store the value into,
        "opitem": SECRET_NAME, # and you give it the these three items to define the secret uniquely in 1Password
        "opfield": ".password",
        "opvault": VAULT_ID,
    },
}

# instantiate a 1Password client
client: Client = new_client(ONEPASSWORD_CONNECT_HOST, ONEPASSWORD_CONNECT_TOKEN)
# get the requested secrets from 1Password
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

    # An extract task which pulls the weather forecast from the NOAA API
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
    def write_out_html_file(forecast: str, time: str, logs: str):
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
                img {{
                    justify-content: center;
                    margin: 0 20px 0 20px;
                }}
                </style>
            </head>
            <body>
                    <img src='annotated-image.jpg' alt='image manipulated with docker' />
                <div>
                    <p class="weather">{forecast}</p>
                    <p class="smaller">{time}</p>
                    <p class='smaller'>{DEPLOYMENT_ENVIRONMENT} secret: {SECRETS["secret_value"]}</p>
                </div>
            </body>
            </html>
        """)
        f.close()

    @task()
    def download_image_and_annotate_with_docker():
        client = docker.from_env()
        client.images.pull("frankinaustin/signal-annotate")
        logs = client.containers.run(
            image="signal-annotate", 
            volumes=['/Users/frank/Development/airflow/weather:/opt/weather']
            )
        return str(logs)

    # the following lines are defining input and output of the tasks
    # which is also used to define the DAG graph. This works well for
    # simple DAGs, but the more complex it gets, the more you'll want to
    # dive into the bitwise operators and the explicit methods used to 
    # define graph edges.

    time = get_time_in_austin_tx()
    weather = get_weather()
    forecast = get_forecast(weather)
    logs = download_image_and_annotate_with_docker()
    write_out_html_file(forecast=forecast, time=time, logs=logs)

etl_weather()
