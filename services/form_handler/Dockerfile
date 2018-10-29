# Base image
FROM python:3.6.5-alpine

# Set working directory
RUN mkdir /usr/app
WORKDIR /usr/app

# Add and install requirements
COPY ./requirements.txt /usr/app/requirements.txt
RUN pip install -r requirements.txt

# Add app
COPY . /usr/app

# Run server
CMD python manage.py run -h 0.0.0.0