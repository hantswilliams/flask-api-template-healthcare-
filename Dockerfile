FROM python:3.11.6-alpine3.18

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /app/healthcare-template-app/

RUN python init_db.py

EXPOSE 5005

CMD [ "python", "app.py" ]

# build command: docker build -t flaskhealth .
# run command: docker run -p 5005:5005 flaskhealth
# should then be able to see it on `http://localhost:5005` in the browser
