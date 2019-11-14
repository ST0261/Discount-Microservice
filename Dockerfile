FROM python:3.6

MAINTAINER Juan Gonzalo Quiroz Cadavid

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]