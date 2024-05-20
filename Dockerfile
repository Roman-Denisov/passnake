FROM python:3.10

#RUN apk --update add bash nano vim gcc g++  musl-dev linux-headers  # something really old, left here 'just in case'
COPY ./project/requirements.txt /var/www/requirements.txt
# TODO CHANGE THIS TO ONE LAYER 
RUN pip install uWSGI
RUN pip install -r /var/www/requirements.txt

WORKDIR /app
COPY ./project/ /app/project/
COPY .keys /app/.keys
COPY ./wsgi.py /app

CMD ["uwsgi","--socket","0.0.0.0:5000", "--protocol=http","-w","wsgi:app"]


