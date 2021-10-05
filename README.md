# NBA Fantasy App
this is a forked project that delivers nba data via rest api.

## setting up the enviroment
- make sure you have python 3.8+ (newest version)
- create a new virtual environment, prefered in the project directory under name **.venv**
    ```
    python -m venv .venv
    ```
- activate the virtual environment
    ```
    source .venv/bin/activate
    ```
- run command to install required libs and frameworks
    ```
    pip install -r requirements.txt
    ```

## setting up the database
- create a Postgres database with login user
- the connection string of the database should like below
    ```
    postgresql://<user>:<password>@<db-host>:<port>/<database>
    ```

## setting up environment variables
- create in the root directory **.env** file
- open **.env.example** file, copy all variables names and paste them in the **.env** file
- fill the variables names with their values to match your development environment, like the database uri, paste in it the connection string

## database migrations
- make sure you are in the project directory
- make sure you have the **DATABASE_URI** in **.env** has value
- make sure the virtual environment activated
- run these cmds:
    ```
    ./bootstrap.sh init
    ./bootstrap.sh migrate
    ./bootstrap.sh upgrade
    ```

## filling database with data
- put the file inside data folder inside root directory- run command
    ``` 
     ./bootstrap.sh sync-games --season=<yyyy-yy> --start-date=<mm/dd/yyyy> --end-date=<mm/dd/yyyy>
    ```
- this command will get teams and players stats data from a given season
- season start and end date is to face any break during the process because nba stats api endpoint may break, so you can re-run the cmd by mofiying the enddate where it was stopped

## Why SQL database
A lot of the operations done with Pandas can be done more easily with SQL, this includes filtering a dataset, selecting specific columns for display, applying a function to a values, and so on, plus SQL has the advantage of having an optimizer and data persistence.

## Flask app
- ***Comming Soon***