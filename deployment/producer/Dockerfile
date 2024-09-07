FROM python:slim

COPY ../src /src
COPY ../requirements.txt /requirements.txt
#RUN pipenv install --deploy --ignore-pipfile
RUN pip install -r requirements.txt
CMD python /src/producer.py
#CMD pipenv run python /src/producer.py