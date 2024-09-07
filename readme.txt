Background:

Standalone localised solution to manage asynchrnous workflows using a producer process and a consumer process, with a SQLite database as the intermediatary queue.
The database is transient and thrown away after each execution.

The workflow is managed using a single docker-compose file

The docker compose command starts the prodcuer and consumer services. The producer creates and inserts a new execution "run" in the runs 
table and then inserts jobs in the SQL lite jobs table in pending state. When all jobs have been submitted the producer marks the "run" 
as complete to tell the consumer there are no more jobs coming, (the queue could be empty but we might have more jobs pending).
At this point the consumer container exits

The consumer waits for the "run" to be inserted and then starts polling for jobs in the pending state, generates a response for each job and marks the 
job as complete. It periodically checks whether the overall "run" is marked as complete, if so, when the queye becomes empty, the consumer writes all
the output of all jobs to csv file and then exits the container. At this point the docker-compose process exits and the workflow is complete

Run the following command from the root directory of the project;

== build the base image
docker build -f deployment/base/Dockerfile -t mattua/tmp-base .

docker-compose -f deployment/docker-compose.yml up --build

MacOS:
docker compose -f deployment/docker-compose.yml up --build


-- build base image with dependencies
docker build -f deployment/base/Dockerfile -t tmp-base .



pipenv
-------------
pip3 install pipenv
pipenv install requests - will install venv

--activate the venv
pipenv shell



https://pipenv.pypa.io/en/stable/docker.html

--installs from piplock not pipfile
pipenv install --ignore-pipfile

-- generate reuirements.txt from pipenv
pipenv run pip freeze > requirements.txt


----get shell inside the base image
docker run -it --entrypoint '/bin/sh' mattua/tmp-base