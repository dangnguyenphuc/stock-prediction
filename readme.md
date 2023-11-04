# DATA ENGINEERING
## Start timescaleDB
```
docker run -d --name timescaledb -p 0.0.0.0:5432:5432 \
-e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg14
```