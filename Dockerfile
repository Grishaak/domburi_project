FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app/domburi_django_app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY domburi .

CMD ["gunicorn", "domburi.wsgi:application", "--bind", "0.0.0.0:8000"]
