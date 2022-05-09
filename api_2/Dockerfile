FROM python:3.9

RUN pip3 install djangorestframework
RUN pip3 install django-cors-headers

WORKDIR /usr/src/app

COPY . .

CMD ["python3", "manage.py", "runserver", "0:8000", "--noreload"]

EXPOSE 8000
