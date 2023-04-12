# airflow

## features
* control over production deployment configuration
* endlessly customizable python environment, including external, binary libraries built right into the container
* local development with a high quality DX
  * you get a full local airflow stack, so you can trigger it as if in airflow
  * you can run the command in a terminal and get full STDOUT from the program, but also color coded print-out of the interactions with the airflow orchestration
  * ~fail to safe~
* onepassword secrets
  * built in, zero-config. You give it the secret name in 1PW, it gives you the value
* support for picking secrets based on local/production

## intents
* works as the production instance
* works for local development with good DX

## useful commands
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

## ideas
* make it disable all dags on start locally (default / main) so it fails to safe
* local docker

