FROM python:3.9

WORKDIR /app/build

ENV PYTHONPATH /app/build/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

#CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "settings.wsgi:application", "--bind 0.0.0.0:8000", "--workers 10", "--threads 2", "--log-level info",\
     "--max-requests 1000", "--timeout 10"]
