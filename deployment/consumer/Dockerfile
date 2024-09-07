FROM python:slim

COPY ../src /src
COPY ../requirements.txt /requirements.txt
#RUN pipenv install --deploy --ignore-pipfile
RUN pip install -r requirements.txt
CMD python /src/consumer.py