#Base image for the Flask application
FROM python:3.10
#Working Directory for the flask application
WORKDIR /flask
#It will copy the Flask application files and the requirements.txt file
COPY . /flask
#It will install the dependencies for the Flask application
RUN pip install -r requirements.txt
#It starts the Flask application on Port 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]