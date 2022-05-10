# PostgreSQL / Elasticsearch sample data generator

## Setup

### PostgreSQL

Create user and database:

```
$ sudo su postgres
$ psql
> CREATE DATABASE ds_playground;
> CREATE USER ds_playground WITH PASSWORD 'ds_playground';
> GRANT ALL ON DATABASE ds_playground TO ds_playground;
```

Make sure you can log in with user/pass. In `/var/lib/pgsql/data/pg_hba.conf` add:

```
host ds_playground ds_playground 127.0.0.1/32 md5
host ds_playground ds_playground ::1/128 md5
```

### Elasticsearch

```
$ docker run -d -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.3
```

## Run

This will take a while. You'll need python3 and psycopg2.

```
$ python3 generate.py
```
