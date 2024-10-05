# Base Image
FROM python:3.12.6-slim

# Setting the workdir
WORKDIR /app

# Copy the requirements
COPY requirements.txt /app/

# Installing the dependencies
RUN python -m pip install -r /app/requirements.txt

COPY . /app/

# Leave the container alive, while creating the databases in pgadmin
CMD [ "tail", "-f", "/dev/null" ]

# ! NEXT STEPS
# RUN docker compose exec djangoapp python manage.py migrate
# RUN docker compose exec djangoapp python manage.py seed -Ft Saber11
# RUN docker compose exec djangoapp python manage.py seed -Ft SaberPro
# RUN docker compose exec djangoapp rm -rf /app/data
# RUN docker compose exec djangoapp python manage.py runserver 0.0.0.0:8000