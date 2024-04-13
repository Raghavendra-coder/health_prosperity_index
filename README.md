**Constructing a Health and Prosperity Index for US States**

**Part - 1**
1. All the points mentioned in the review has been fixed.
2. Special Fix : The effect child mortality rate and poverty rate will now be inverse in calculating the final index. That is, increase in these rates will affect inversely to the final index.

**Part 2: How to run the project**
1. Clone the project in your local using git clone https://github.com/Raghavendra-coder/health_prosperity_index.git
2. Start your docker server.
3. Open your terminal in the path where the "manage.py" file is located. (manage.py is just inside health_prosperity_index, health_prosperity_index --> manage.py)
4. So if you are in the health_prosperity_index directory then you are ok else change the directory to health_prosperity_index.
5. run docker-compose up --build in the terminal.(with the docker server already running)
6. When the build will be completed (you will see )
7. After that open 0.0.0.0:8502(the port used by main streamlit).
8. If the data is not updated, you will see it getting updated; if it is already updated you will see the health-prosperity-index every year.
9. If you want to run the project on your local system then : 
  I) Change the directory to health_prosperity_index.
  II) Create python virtual environment (command : python -m venv <name_of_env>) and activate it.
  II) run the command "pip3 install -r requirements.txt"
  III) In settings.py change the variable "LOCAL" to True (for docker it should be False and for local it should be True).
  IV) In settings.py change the configurations :
       
          CELERY_BROKER_URL = 'redis://localhost:6360/0'
          CELERY_RESULT_BACKEND = 'redis://localhost:6360/0'

  V) run "python manage.py runserver"
  VI)  then run the command "streamlit run streamlit_file.py" which will direct you to the streamlit server and will open the Index Graph and data table.
  VII) Start the redis server on port 6360 (redis-server --port 6360)
  VIII) Start celery : celery -A health_prosperity_index worker --loglevel=info
  IX)  Start celery beats : celery -A health_prosperity_index beat -l info


**What is done in this project**
1. Used the API endpoints to get the required data from datausa.io. (**part-2 point 1 covered here**)
2. Refine and take the needed data from all the data. (using pandas and numpy)
3. Updating the final data in the database.
4. Fetching the data from the database and calculating the health prosperity index. (**part-2 point 2 covered here**)
5. An asynchronous task has been set up that will update the data in the database every 24 hours at 00:00 UTC. This ensures that you pick up any changes that the data 
USA may make in their datasets. (**part-2 point 3 covered here**)
6. Showing the resulting chart using Streamlit. (**part-2 point 4 covered here**)
7. Asynchronous tasks have been set up using celery, celery beats, and redis.
8. And finally everything is dockerized.



**Technologies used in this project**
1. python
2. Database Designing
3. Django
4. REST API
5. API Testing
6. Docker
7. Github
8. Bash
9. Celery
10. Celery Beats(for async tasks)
11. Streamlit
12. sqlite3 database(with django ORMs)

