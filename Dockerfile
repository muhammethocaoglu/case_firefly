FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

# Creating working directory
RUN mkdir /customer
COPY . /customer
WORKDIR /customer

RUN pip install -r requirements.txt

RUN ls

CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000