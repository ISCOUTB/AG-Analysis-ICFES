FROM python:3.12.6-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

# docker compose exec djangoapp python manage.py migrate
# docker compose exec djangoapp python manage.py seed -Ft Saber11
# docker compose exec djangoapp python manage.py seed -Ft SaberPro