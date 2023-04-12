# Airflow

## Features
* local development with a high quality DX
  * you get a full, local airflow stack
    * so you can trigger it as if in airflow, via the UI
  * you can run the command in a terminal and get full STDOUT from the program, but also color coded print-out of the interactions with the airflow orchestration
* onepassword secrets
  * built in, zero-config in DAG. You give it the secret name in 1PW, it gives you the value, right in the DAG
* working CI, secured using 1PW secrets
  * Pull on merge into production
* support for picking secrets based on local/production
  * zero-config in DAG, based out of `.env`
* full control over production server configuration, yet remaining with perks of docker stack
* endlessly customizable python environment, including external, binary libraries built right into the container
  * based on bog standard `requirements.txt`
* very minimal deployment settings
  * [PR #22 lists them](https://github.com/frankhereford/airflow/pull/22/files)

## Local Setup
* GitHub key pair
  * Public installed on GitHub
  * Private in `private_key_for_github` at the top of the repo
    * Starts and ends with 
      * `-----BEGIN OPENSSH PRIVATE KEY-----`
      * `-----END OPENSSH PRIVATE KEY-----` or similar
* `.env` file in the form of:
```
AIRFLOW_UID=<the numeric output of the following command: id -u>
ENVIRONMENT=<development|production>
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=<pick your initial admin pw here>
OP_API_TOKEN=<Get from 1PW here: 'name TBD'>
OP_CONNECT=<URL of the 1PW Connect install>
```
* Execute `docker compose build`
* Execute `docker compose up -d`
* Aiflow is available at http://localhost:8080
* The test weather DAG output at http://localhost:8081
* The webhook flask app at http://localhost:8082

## Useful Commands
```
# 🐚 get a root shell on the scheduler, for example

docker exec -u root -it airflow-airflow-scheduler-1 bash
```

```
# 🐚 get a shell on a worker, for example

docker exec -it airflow-airflow-worker-1 bash
```

```
# stop all containers and execute this to reset your local database
# ⛔️ do not run in production unless you feel really great about your backups
# ⛔️ this will reset the history of your dag runs and switch states

docker compose down --volumes --remove-orphans
```

## Ideas
* make it disable all dags on start locally (default / main) so it fails to safe
* local docker socket pass down
* fix UID being applied by `webhook` image on `git pull`
* CI to block `no-merge` merges

## Example DAGs
* You can turn on [this field](https://github.com/frankhereford/airflow/blob/main/docker-compose.yaml#L65) to get about 50 example DAGs of various complexity to borrow from