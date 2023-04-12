# airflow

## intents
* works as the production instance
* works for local development with good DX

## useful commands
```
docker exec -u root -it airflow-airflow-scheduler-1 bash
```

## ideas
* make it disable all dags on start locally (default / main) so it fails to safe
* local docker
* wipe the database command
* dev v production env variable indicator