# currywurst-machine

This repository contains the code and design files for a  Currywurst Machine. A Currywurst Machine is a device that automates the cooking and preparation of Currywurst, a popular street food in Germany. With this machine, you can easily make Currywurst at home or at events without the need for a dedicated chef.

## Requirements

Have docker with docker compose installed

## Structure
This repo is structured in two main services.

### currywurst_machine_api
Responsible to offer an API that calculates the change according to the money added for the user and in the end of the operation, send to a Redis queue the history of the transaction.
To access the API please go to:

```
http://localhost:3003
```

### transactions_history_manager
Responsible for receiving the Redis queue logs and store the history of transactions.


## Usage

### Running the project:
Simply run

```
docker compose up --build -d
```

### Reading data in the tables

To check what is inside the table type:
```
sqlite3 data/mydb.sqlite
```
And next:

```
select * from currywurst_machine_logs;
```

If for some reason the user cannot read the table due to permission , simply perform the command below:
```
sudo chmod a+r data/mydb.sqlite
```

## Interpretation details

The problem description said that the machine can only return coins. That create limitations to the solution because if an error is raised we can not return back the exact amount the user added. So, to respect the description I returned None.

## Comments

- Ideally I would create two different repositories and use docker images from a registry in the docker-compose.yml instead of build the repos locally. However, for presentation purposes, I decided to do in this way.