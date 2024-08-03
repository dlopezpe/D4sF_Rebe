# DS4F Manager

## High level design for DS4F (Data Smart For Farming 2.0)

### Manager

 Will consist of a process:
* DS4FManager: REST application that interfaces with the DB.

## Use cases flows

### New information DS4F

Manager:
Products Data smart for farming. The DB is a PostgresSQL with use image Docker. 
Necessary software https://trac.osgeo.org/osgeo4w/
And create a secret Key Django for PRODUCTION generate by https://djecrety.ir/


## Tecnologies


List of tecnologies used for the DS4FManager (not complete, probably will need more):

 Software                                                                                                                                  | Version | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
-------------------------------------------------------------------------------------------------------------------------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
 Docker                                                                                                                                    | 1.29.2  | Create images for Postgres.  Docker Compose is a tool for running multi-container applications on Docker defined using the Compose file format. A Compose file is used to define how the one or more containers that make up your application are configured. Once you have a Compose file, you can create and start your application with a single command: docker-compose up.                                                                                     |
 Python                                                                                                                                    | 3.11.4  | Code to implametetion.                                                                                                                                                                                                                                                                                                                                                                                                                                              |
 Psycopg2                                                                                                                                  | 2.9.6   | Connection/framework to DB for Postgres. Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Its main features are the complete implementation of the Python DB API 2.0 specification and the thread safety (several threads can share the same connection). It was designed for heavily multi-threaded applications that create and destroy lots of cursors and make a large number of concurrent “INSERT”s or “UPDATE”s. |
 | |         | Psycopg 2 is mostly implemented in C as a libpq wrapper, resulting in being both efficient and secure. It features client-side and server-side cursors, asynchronous communication and notifications, “COPY TO/COPY FROM” support. Many Python types are supported out-of-the-box and adapted to matching PostgreSQL data types; adaptation can be extended and customized thanks to a flexible objects adaptation system. |
 Pyway                                                                                                                                     | 0.3.16  | Pyway is a database versioning and migration tool inspired by Flyway.                                                                                                                                                                                                                                                                                                                                                                                               |
 Requests                                                                                                                                      | 3.0.1   | PyPDF2 is a free and open-source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files. It can also add custom data, viewing options, and passwords to PDF files. PyPDF2 can retrieve text and metadata from PDFs as well.                                                                                                                                                                                       |
                                                                                                                          | 8.9.0   | Elasticsearch is a distributed, RESTful search and analytics engine capable of addressing a growing number of use cases.                                                                                                                                                                                                                                                                                                                                            |

## Installation

Use the package devops by environment [dev/prod/test] to install docker and migrate DB.

```bash

$ chmod 770 ./devops/launch.sh
$ ./devops/launch.sh [dev/prod/test]
```

## Migrate scripts DB

With FlyWay (PyWay in Python) it's necessary launch command  pyway migrate

```bash
$ pyway migrate
PyWay 0.3.16
Starting migration process
Migrating --> V02_01__add_trigger_all_tables_update_column_modified_at.sql
V02_01__add_trigger_all_tables_update_column_modified_at.sql SUCCESS

Migration completed.
```

### Important format scripts DB

```bash
 V{major}_{minor}__{description}.sql
```


## Generate executable for Windows
```bash
$ pip install pyinstaller 
$ pyinstaller --onefile app/d4sFManagerApp.py

```
When finish process log:

```bash
15920 INFO: Building EXE from EXE-00.toc completed successfully.

```
build/DS4FManagerApp.exe


* Start app Django in IDE (Pycharm)


## Links importants!

[PyWay](https://pypi.org/project/pyway/0.3.16/)

[ENCRYPTION_KEY](https://seanwasere.com/generate-random-hex/)

[Expresiones regulares](https://es.wikipedia.org/wiki/Expresi%C3%B3n_regular#El_punto_%22.%22)