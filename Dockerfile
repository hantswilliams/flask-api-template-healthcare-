FROM python:3.11.6-alpine3.18
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD [ "python", "healthcare-template-app/app.py" ]

# build command: docker build -t flaskhealth .
# run command: docker run -p 5005:5000 flaskhealth
# should then be able to see it on `http://localhost:5005` in the browser
