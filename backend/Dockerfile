# Base Image
FROM python:3.12.6-slim

# Setting the workdir
WORKDIR /app

# Copy the requirements
COPY requirements.txt /app/

# Installing the dependencies
RUN python -m pip install -r /app/requirements.txt

COPY . /app/

EXPOSE 8000

CMD [ "python", "manage.py", "runserver" ]

# docker compose exec djangoapp python manage.py migrate
# docker compose exec djangoapp python manage.py seed -Ft Saber11
# docker compose exec djangoapp python manage.py seed -Ft SaberPro