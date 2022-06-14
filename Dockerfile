FROM python:3.8.6
RUN apt-get update \
&& apt-get install -y postgresql postgresql-contrib libpq-dev python3-dev
RUN pip install --upgrade pip
COPY ./todo/ ./
RUN pip install -r requirements.txt
COPY wait-for-postgres.sh .
RUN chmod +x wait-for-postgres.sh
RUN pip install gunicorn
