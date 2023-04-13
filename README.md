# Airflow for local/production use

## Features
* [local development](https://github.com/frankhereford/airflow#local-setup) with a high quality DX
  * you get a full, local airflow stack
    * so you can trigger it as if in airflow, via [the UI](http://localhost:8080/home)
      * stack traces available in UI
  * you can run the ETL in a terminal and get full `stdout` from the program and also color-coded print-out of the DAG's interactions with the airflow orchestration
    * attach to a worker `docker exec -it airflow-airflow-worker-1 bash`
    * run your dag with `airflow dags test weather-checker`, for example
    * continue to make changes to the code outside of running container and they will show up in airflow as you save
* [onepassword secrets](https://github.com/frankhereford/airflow/blob/main/dags/weather.py#L26-L39)
  * built in, zero-config. You give it the secret name in 1Password, it gives you the value, right in the DAG
* [working CI](https://github.com/frankhereford/airflow/blob/main/.github/workflows/production_deployment.yml), [via webhook](https://github.com/frankhereford/airflow/blob/main/webhook/webhook.py#L33-L46), secured using 1Password secrets
  * Automatically pulls from `production` when PRs are merged into it
  * You can rotate the secret by opening 1Password, editing [the entry](https://github.com/frankhereford/airflow/blob/main/webhook/webhook.py#L13), generating a new password, and saving it. 🏁
* support for picking [environment based secrets](https://github.com/frankhereford/airflow/blob/main/dags/weather.py#L21-L24) based on local/production
  * zero-config in DAG, based out of `.env`
* [production environment](https://airflow.fyi) which runs on a `t3a.xlarge` class instance comfortably
  * full control over [production server configuration](https://github.com/frankhereford/airflow/blob/main/airflow.cfg), yet remaining with perks of docker stack
* [customizable python environment](https://github.com/frankhereford/airflow/blob/main/requirements.txt) for DAGs, including [external, binary libraries](https://github.com/frankhereford/airflow/blob/main/Dockerfile#L1414-L1415) built right into the container
  * based on bog standard `requirements.txt`
* access to the [server's docker service](https://github.com/frankhereford/airflow/blob/main/docker-compose.yaml#L90)
  * On worker containers and available for DAGs
* [flexible reverse proxy](https://github.com/frankhereford/airflow/blob/main/haproxy/haproxy.cfg#L35-L54) to distribute requests over stack
* [very minimal production deployment changes](https://github.com/frankhereford/airflow/pull/22/files)
  * server is EC2's vanilla Ubuntu LTS AMI

## Local Setup
* `.env` file:
```
AIRFLOW_UID=<the numeric output of the following command: id -u>
ENVIRONMENT=<development|production>
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=<pick your initial admin pw here>
OP_API_TOKEN=<Get from 1Password here: 'name TBD'>
OP_CONNECT=<URL of the 1Password Connect install>
```
* `docker compose build`
* `docker compose up -d`
* Airflow is available at http://localhost:8080
* The test weather DAG output at http://localhost:8081
* The webhook flask app at http://localhost:8082

## Production Setup
* GitHub key pair
  * Public key installed on GitHub
  * Private key in `private_key_for_github` at the top of the repo
    * Starts and ends with 
      * `-----BEGIN OPENSSH PRIVATE KEY-----`
      * `-----END OPENSSH PRIVATE KEY-----` or similar
  * This could be eliminated if we commit to never pushing from the production install again
    * We could change the checkout on the production machine to a `HTTPS` instead of `ssh` based git origin
* `.env` file
  * See above

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
* fix UID being applied by `webhook` image on `git pull`
* Create remote worker image example
  * Use `docker compose` new `profile` support
* Add slack integration?

## Example DAGs
* You can turn on [this field](https://github.com/frankhereford/airflow/blob/main/docker-compose.yaml#L65) to get about 50 example DAGs of various complexity to borrow from