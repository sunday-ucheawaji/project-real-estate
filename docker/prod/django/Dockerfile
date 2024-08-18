###########
# BUILDER #
###########

# pull official base image
FROM python:3.10.0-slim-buster as builder

ENV APP_HOME=/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles

# set work directory
WORKDIR $APP_HOME

LABEL maintainer="sundayucheawaji@gmail.com"
LABEL description="Production image for Real Estate Project"

# prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Ensure python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && apt-get install -y gettext \
    && apt-get install -y netcat gcc postgresql \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# lint 
RUN pip3 install --upgrade pip
COPY . /app

# install python dependencies
COPY ./requirements.txt  /app/requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

#########
# FINAL #
#########

FROM python:3.10.0-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && apt-get install -y gettext \
    && apt-get install -y netcat gcc postgresql \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint
COPY ./docker/prod/django/entrypoint .
RUN sed -i 's/\r$//g' /home/app/web/entrypoint
RUN chmod +x /home/app/web/entrypoint

# copy start
COPY ./docker/prod/django/start .
RUN sed -i 's/\r$//g' /home/app/web/start
RUN chmod +x /home/app/web/start

# copy start-celeryworker
COPY ./docker/prod/django/celery/worker/start /home/app/web/start-celeryworker
RUN sed -i 's/\r$//g' /home/app/web/start-celeryworker
RUN chmod +x /home/app/web/start-celeryworker

# copy start-flower
COPY ./docker/prod/django/celery/flower/start /home/app/web/start-flower
RUN sed -i 's/\r$//g' /home/app/web/start-flower
RUN chmod +x /home/app/web/start-flower

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint
ENTRYPOINT ["/home/app/web/entrypoint"]