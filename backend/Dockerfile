# Base Image
FROM python:3.12.6-slim

# Setting the workdir
WORKDIR /app

# Copy the requirements
COPY requirements.txt /app/

# Installing the dependencies
RUN python -m pip install -r /app/requirements.txt

COPY . /app/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]


# ! NEXT STEPS
# RUN docker compose exec djangoapp python manage.py migrate