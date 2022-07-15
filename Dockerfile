FROM python:3.9-slim-buster
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]

