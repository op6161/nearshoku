# gunicorn

FROM python:3.10
WORKDIR /usr/src/app

## install packages
COPY requirements.txt ./
RUN pip install -r requirements.txt

## copy all src files
COPY . .

## run the apps on the port 8080
EXPOSE 8000

## gunicorn run server on the port 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "nearshoku.wsgi:application"]

# # # Since the ssl setting, the container created with this image only works in https server
# # # It can use runserver local with
# python manage.py runsslserver --certificate django.crt --key django.key