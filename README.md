# airflow

## intents
* works as the production instance
* works for local development with good DX

## useful commands
```
docker exec -u root -it airflow-airflow-scheduler-1 bash

# get a shell on a worker
docker exec -it airflow-airflow-worker-1 bash

# stop all containers and execute this to reset your local database
# ⛔️ do not run in production unless you feel really great about your backups
# ⛔️ this will reset the history of your dag runs and switch states
docker compose down --volumes --remove-orphans



```

## ideas
* make it disable all dags on start locally (default / main) so it fails to safe
* local docker
* dev v production env variable indicator

## features
* control over production environment
* local development with a high quality DX
* onepassword secrets