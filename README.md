# PLMDataChallenge

This repository holds my submission for the PLM data engineering challenge, using Python Dash and Postgres. It is structured as follows: ```app.py``` is the main dash entrypoint, and takes a single command-line argument, ```-d``` or ```--docker``` to tell the app how it should try to reach the database. It assembles the components that are defined in a dataclass in the ```plm_dash_components``` module.

The ```plm_dash_components``` module is where the bootstrap components that make up the dashboard are instantiated, and is where the front and back ends of the dashboard meet.

The backend is defined in the ```plmdata``` module, and encapsulates all the code that is used for connecting to the database. The front end in ```plm_dash_components``` obtains data via wrapper functions provided by the ```Backend``` class.

```EDA.ipynb``` and ```Experiments.ipynb``` are where the exploratory analyses took place. There are functions within them that allow for easy visualizations of the data. (```EDA.ipynb``` was written before the ```Backend``` class, so doesn't leverage it. ```Experiments.ipynb``` does.)

To run the code, clone the repo and create a .env file in the top-level directory with these keys: ```POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_DATABASE, POSTGRES_HOST```. Once this is in place, the containers can be built with ```docker-compose build``` and deployed with ```docker-compose up```. 

As written, the site won't work until the database is populated (I didn't get to error handling / tests yet), so it's better to use ```docker-compose up database``` to start the database first, then, once the database is up, use the script file in ```plmdata``` that loads the provided csv files into the database, ```populate_postgres.py```, to load the data. It assumes the files exist in a directory: ```plmdata/raw/user*.csv```. Once the database is populated, ```docker-compose up dash``` will bring up the site on port 80. 
