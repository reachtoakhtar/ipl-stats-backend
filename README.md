# ipl-stats-backend

## Steps to run:

0. Make sure docker and Postgres is installed in your machine. 

1. cd to the directory which contains docker-compose.yml file and then run
    
    #### $ docker-compose up
    
2. Once the setup is ready, open a new terminal window and run the following (while being in the same directory):
    
    #### $ docker-compose exec web python manage.py migrate

3. Open Postman and make a POST request to the following url to populate the 
    database (no headers, parameters need to be passed).
    
    #### http://localhost:8000/ipl_stat/lookups/
    
    Wait for a couple of minutes for the request to complete.

4   You are good to go. Now you can start the frontend app. Clone the repository 
    by using the below link and the follow the instructions given in README.md file:
    
    https://github.com/reachtoakhtar/ipl-stats-frontend.git
